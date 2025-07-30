import os
import glob
import io
import requests
import logging
import warnings
import statistics
import math
from pathlib import Path
from importlib import resources
import concurrent.futures as confu 

import numpy as np
import pandas as pnd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator



def task_rawdata_collect(args):
    logger, file, pms, replicates, discarding = args
    
    strain = Path(file).stem

    res_df = []
    excel_file = pnd.ExcelFile(file, engine='openpyxl')
    for time in range(len(excel_file.sheet_names)):
        df = excel_file.parse(f'T{time}')
        for pm in pms.split(','):
            for od in ['590', '750']:
                for replicate in replicates.split(','):
                    readout = f'{pm} {od} {replicate}'
                    if strain + ' ' + readout in discarding:   # discard these samples
                        logger.debug(f"Discarding readout as requested: '{strain}', PM '{pm}', OD '{od}', replicate '{replicate}', time 'T{time}'.")
                        continue 


                    # find boolean mask where value matches
                    mask = df == readout
                    # get the integer positions (row and column indices)
                    indices = list(zip(*mask.to_numpy().nonzero()))
                    # get the only result
                    try: result = indices[0]
                    except: 
                        logger.debug(f"Expected readout not found: strain '{strain}', PM '{pm}', OD '{od}', replicate '{replicate}', time 'T{time}'.")
                        continue


                    # adjust indices
                    row_i = result[0] + 2
                    col_i = result[1] + 1
                    for pm_row_i, pm_row in enumerate([r for r in 'ABCDEFGH']):
                        for pm_col_i, pm_col in enumerate([c +1 for c in range(12)]):
                            # get proper well name
                            pm_col = str(pm_col)
                            if len(pm_col) == 1: pm_col = '0' + pm_col
                            well = f'{pm_row}{pm_col}'
                            # get proper plate name
                            plate = pm
                            if plate == 'PM1': pass
                            if plate == 'PM2': plate = 'PM2A'
                            if plate == 'PM3': plate = 'PM3B'
                            if plate == 'PM4': plate = 'PM4A'
                            # read value
                            value = df.iloc[row_i + pm_row_i, col_i + pm_col_i]
                            res_df.append({
                                'index_col': f"{plate}_{time}_{od}_{replicate}_{well}",
                                'pm': plate, 'time': time, 'od': od, 'replicate': replicate, 'well': well, 'value': value})                     
    res_df = pnd.DataFrame.from_records(res_df)
    res_df = res_df.set_index('index_col', drop=True, verify_integrity=True)


    # verbose logging
    logger.debug(f"Strain '{strain}' has {len(res_df['pm'].unique())} plates, {len(res_df['replicate'].unique())} replicates, and {len(res_df['time'].unique())} time points.")  
    
    return (strain, res_df)


def task_wavelength_subtraction(args):
    logger, strain, df = args
    logger.debug(f"Processing strain '{strain}'...")
        
    df['value_norm'] = None   
    for index, row in df.iterrows(): 
        if row['od'] == '590':
            index_750 = f"{row['pm']}_{row['time']}_750_{row['replicate']}_{row['well']}"
            df.loc[index, 'value_norm'] = df.loc[index, 'value'] - df.loc[index_750, 'value']
    df = df[df['value_norm'].isna()==False]
    df = df.drop(columns=['od', 'value'])
    df.index = [f"{row['pm']}_{row['time']}_{row['replicate']}_{row['well']}" for index, row in df.iterrows()]
    
    return (strain, df)
        
            
def task_blank_subtraction(args):
    logger, strain, df = args
    logger.debug(f"Processing strain '{strain}'...")

    for index, row in df.iterrows():
        # get the well of the blank
        if row['pm'] in ['PM1', 'PM2A', 'PM3B']:
            well_black = 'A01'
        else:  # PM4A is both for P and S
            if row['well'][0] in ['A','B','C','D','E']:
                well_black = 'A01'  # P
            else: well_black = 'F01'  # S
        # get the index of the blank
        index_blank = f"{row['pm']}_{row['time']}_{row['replicate']}_{well_black}"
        df.loc[index, 'value_norm'] = df.loc[index, 'value_norm'] - df.loc[index_blank, 'value_norm']
        if df.loc[index_blank, 'value_norm'] < 0: 
            df.loc[index_blank, 'value_norm'] = 0
            
    return (strain, df)


def task_T0_subtraction(args):
    logger, strain, df = args
    logger.debug(f"Processing strain '{strain}'...")
        
    for index, row in df.iterrows():
        index_T0 = f"{row['pm']}_0_{row['replicate']}_{row['well']}"
        df.loc[index, 'value_norm'] = df.loc[index, 'value_norm'] - df.loc[index_T0, 'value_norm']
        if df.loc[index, 'value_norm'] < 0: 
            df.loc[index, 'value_norm'] = 0
            
    return (strain, df)


def task_mean_sem(args):
    logger, strain, df, output_folder = args
    logger.debug(f"Processing strain '{strain}'...")
        
    found_reps = list(df['replicate'].unique())
    df['value_mean'] = None   # dedicated column
    df['value_sem'] = None   # dedicated column
    for index, row in df.iterrows():
        values = []
        for rep in found_reps:
            index_rep = f"{row['pm']}_{row['time']}_{rep}_{row['well']}"
            try: value = df.loc[index_rep, 'value_norm']
            except: continue  # replicate missing for some reason
            values.append(value)
        if len(values) > 1:
            # get the # standard error of the mean (standard deviation)
            std_dev = statistics.stdev(values)
            sem = std_dev / math.sqrt(len(values))
            df.loc[index, 'value_mean'] = statistics.mean(values)
            df.loc[index, 'value_sem'] = sem
        else:  # no replicates
            df.loc[index, 'value_mean'] = df.loc[index, 'value_norm']
            df.loc[index, 'value_sem'] = 0
    df = df.drop(columns=['replicate', 'value_norm'])
    df = df.drop_duplicates()
    df.index = [f"{row['pm']}_{row['time']}_{row['well']}" for index, row in df.iterrows()]
    
    # save long tables
    df.to_excel(f'{output_folder}/tables/preproc_{strain}.xlsx')
    logger.info(f"'{output_folder}/tables/preproc_{strain}.xlsx' created!")
    
    return (strain, df)



def collect_raw_data(logger, cores, input_folder, pms, replicates, discarding):
    logger.info(f"Collecting raw data...")
    
    
    # check file presence
    files = glob.glob(f'{input_folder}/*.xlsx')
    if len(files) == 0:
        logger.error(f"No .xlsx file found in the provided directory ('--input {input_folder}').")
        return 1
    
    
    # format discarding: 
    formatted_discarding = []
    for d in discarding.split(','):
        try: 
            strain, pm, replicate = d.split('-')
            formatted_discarding.append(f"{strain} {pm} 590 {replicate}")
            formatted_discarding.append(f"{strain} {pm} 750 {replicate}")
        except:
            logger.error(f"Invalid syntax found ('--discarding {discarding}').")
            return 1
    discarding = formatted_discarding
            
    
    # each strain has its own xlsx file: 
    strain_to_df = {}
    with confu.ProcessPoolExecutor(max_workers=cores) as executor:  
        futures = []
        for file in files:
            future = executor.submit(task_rawdata_collect, (logger, file, pms, replicates, discarding))
            futures.append(future)
        confu.wait(futures)  # block until all futures are done
        for future in futures:
            (strain, df) = future.result()
            strain_to_df[strain] = df
        
        
    logger.info(f"Found {len(strain_to_df)} strains in input.")
    return strain_to_df

                    
def data_preprocessing(logger, cores, strain_to_df, output_folder):
    os.makedirs(f'{output_folder}/tables/', exist_ok=True)
    
    
    
    # step 1: OD590 - OD750:
    logger.info(f"Substracting wavelengths...")
    with confu.ProcessPoolExecutor(max_workers=cores) as executor:  
        futures = []
        for i, strain in enumerate(strain_to_df.keys()):
            future = executor.submit(task_wavelength_subtraction, (logger, strain, strain_to_df[strain]))
            futures.append(future)
        confu.wait(futures)  # block until all futures are done
        for future in futures:
            (strain, df) = future.result()
            strain_to_df[strain] = df

        
        
    # step 2: subtraction of the blank
    logger.info(f"Substracting negative controls...")
    with confu.ProcessPoolExecutor(max_workers=cores) as executor:        
        futures = []
        for i, strain in enumerate(strain_to_df.keys()):
            future = executor.submit(task_blank_subtraction, (logger, strain, strain_to_df[strain]))
            futures.append(future)
        confu.wait(futures)  # block until all futures are done
        for future in futures:
            (strain, df) = future.result()
            strain_to_df[strain] = df


        
    # step 3: substraction of T0
    logger.info(f"Substracting T0...")
    with confu.ProcessPoolExecutor(max_workers=cores) as executor:        
        futures = []
        for i, strain in enumerate(strain_to_df.keys()):
            future = executor.submit(task_T0_subtraction, (logger, strain, strain_to_df[strain]))
            futures.append(future)
        confu.wait(futures)  # block until all futures are done
        for future in futures:
            (strain, df) = future.result()
            strain_to_df[strain] = df


    
    # step 4: get mean +- sem given replicates
    logger.info(f"Computing mean and SEM...")
    with confu.ProcessPoolExecutor(max_workers=cores) as executor:        
        futures = []
        for i, strain in enumerate(strain_to_df.keys()):
            future = executor.submit(task_mean_sem, (logger, strain, strain_to_df[strain], output_folder))
            futures.append(future)
        confu.wait(futures)  # block until all futures are done
        for future in futures:
            (strain, df) = future.result()
            strain_to_df[strain] = df
        
        
        
    return strain_to_df

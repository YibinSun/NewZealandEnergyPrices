import argparse

# Create the parser
parser = argparse.ArgumentParser()
# Add a string argument
parser.add_argument('-p','--poc', type=str, help="PoC", default='')
# Parse the arguments
args = parser.parse_args()

# Set First Date
first_day = (1, 11, 2022)
# Set Last Date
# Do not use the current date since it is not available until the next day
last_day = (15, 10, 2024)

# list of required PoCs
pocs = [args.poc]

# list of abstract targets (mean or median)
ts = ['Avg$PerMWHr', 'Med$PerMWHr']

# list of required amount of delays, each unit 30 mins
delay = [
    1,  ## 30 mins delay
    8,  ## 4 hrs delay
    12,  ## 6 hrs delay
    48,  ## 24 hrs delay
    ]

# set to True if ARFF files are also required
arff_option = True

# ======================================================================================================================
import pandas as pd
from datetime import datetime
# import matplotlib.pyplot as pl
import numpy as np
import warnings
import os

warnings.filterwarnings("ignore")

target = 'DollarsPerMegawattHour'
boolean_dict = {'Y': 1, 'N': 0}
island_dict = {'NI': 1, 'SI': 0}

import pandas as pd
import time


def read_csv_with_retry(url, retries=3, delay=0.5):
    """
    Attempts to read a CSV file from a URL with retry mechanism on ConnectionResetError.

    :param url: The URL of the CSV file.
    :param retries: Number of retries before giving up.
    :param delay: Time (in seconds) to wait between retries.
    :return: A DataFrame if successful, None if it fails.
    """
    attempt = 0
    while attempt < retries:
        try:
            # Try to read the CSV file
            df = pd.read_csv(url)
            print(f"Successful.")
            return df
        except ConnectionResetError:
            attempt += 1
            print(f"ConnectionResetError encountered. Retrying {attempt}/{retries}...")
            time.sleep(delay)
        except Exception as e:
            # Handle other potential exceptions
            print(f"An error occurred: {e}")
            return None
    print(f"Failed to read CSV after {retries} attempts.")
    return None


def read_energy_csv(filename, PoC=None):
    print(f'Reading {filename} {PoC}')
    df = read_csv_with_retry(filename, retries=3, delay=0.5)
    if df is None: # can't read remote csv. give up
        return None
    if PoC != None:
        df = df[df['PointOfConnection'] == PoC]
        df = df.drop(columns=['PointOfConnection'])
    df['DateTime'] = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000%z") for date in df['PublishDateTime']]
    df['IsProxyPriceFlag'] = [boolean_dict[c] for c in df['IsProxyPriceFlag']]
    df['Date'] = [p.date() for p in df['DateTime']]
    df['Time'] = [p.time() for p in df['DateTime']]
    df['IntTime'] = [t.hour * 3600 + t.minute * 60 + t.second for t in df['Time']]
    df['Year'] = [d.year for d in df['Date']]
    df['Month'] = [d.month for d in df['Date']]
    df['Day'] = [d.day for d in df['Date']]
    df = df.drop(columns=['Island', 'Date', 'Time'])
    return df


def num_string(x, length=2):
    string = str(x)
    while len(string) < length:
        string = "0" + string
    return string


def date_string(day, month, year, length=2):
    return (num_string(year, length) +
            num_string(month, length) +
            num_string(day, length))


def make_url(day, month, year=2023):
    year_string = date_string(day, month, year)
    s = "https://www.emi.ea.govt.nz/Wholesale/Datasets/DispatchAndPricing/DispatchEnergyPrices/"
    s = s + str(year) + "/" + year_string + "_DispatchEnergyPrices.csv"
    return s


seconds_in_a_day = 86400


def cyclic_encoder(x, min=0, max=seconds_in_a_day):
    lambd = [2 * np.pi * (n - min) / (max - min) for n in x]
    sin_x = [np.sin(n) for n in lambd]
    cos_x = [np.cos(n) for n in lambd]
    return (sin_x, cos_x)


def csv_to_arff(csv_file_path, arff_file_path, relation_name='relation'):
    df = pd.read_csv(csv_file_path)

    # Open the ARFF file for writing
    with open(arff_file_path, 'w') as f:
        # Write the relation name
        f.write(f"@relation {relation_name}\n\n")

        # Write attribute names and types
        for col in df.columns:
            if df[col].dtype == 'object':
                f.write(f"@attribute {col} nominal\n")
            elif df[col].dtype == 'int64':
                f.write(f"@attribute {col} numeric\n")
            elif df[col].dtype == 'float64':
                f.write(f"@attribute {col} numeric\n")
            else:
                f.write(f"@attribute {col} unknown\n")

        f.write("\n@data\n")

        # Write the data
        for index, row in df.iterrows():
            f.write(','.join(map(str, row.values)) + '\n')


def make_targets_with_delay(dict, delay: int = 1, target='Avg$PerMWHr'):
    not_target = 'Med$PerMWHr' if target == 'Avg$PerMWHr' else 'Avg$PerMWHr'
    target_col = dict['Avg$PerMWHr']
    previous_tar_str = 'Prev' + target
    previous_not_tar_str = 'Prev' + not_target
    targets = dict[target]
    previous_col = list(dict[previous_tar_str])
    previous_other_col = list(dict[previous_not_tar_str])
    for i in range(delay - 1):
        previous_col.insert(0, 0)
        previous_col.pop()
        previous_other_col.insert(0, 0)
        previous_other_col.pop()
    df = dict.drop(columns=target)
    df = dict.drop(columns=not_target)
    df[target] = targets
    df[previous_tar_str] = previous_col
    df[previous_not_tar_str] = previous_other_col

    # re-order the columns to put the target at the end
    column_to_move = target
    cols = [col for col in df.columns if col != column_to_move]
    re_ordered = cols + [column_to_move]
    df = df[re_ordered]

    df = df.iloc[delay - 1:]

    return df


month_date_dict = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                   7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

dates = [first_day]

while dates[-1] != last_day:
    last_date = dates[-1]
    date = (last_date[0] + 1, last_date[1], last_date[2])
    if date[0] > month_date_dict[date[1]]:
        date = (1, date[1] + 1, date[2])
    if date[1] > 12:
        date = (1, 1, date[2] + 1)
    dates.append(date)

# ======================================================================================================================

for p in pocs:
    dfs = []
    poc = p
    for day, month, year in dates:
        url = make_url(day, month, year)
        df = read_energy_csv(url, PoC=poc)
        if df is None: # cant read remote csv skip
            continue
        dfs.append(df)

    dfs_loaded = [df.copy() for df in dfs]
    dfs_transformed = []

    for df in dfs:
        df_t = df.copy()
        avg = df_t.groupby(["TradingPeriod"]).mean(numeric_only=True)['DollarsPerMegawattHour']
        df_t = df_t.groupby(["TradingPeriod"]).median(numeric_only=True)
        df_t['Avg$PerMWHr'] = avg
        dfs_transformed.append(df_t)

    full_data = pd.concat(dfs_transformed)
    full_data.columns = full_data.columns.str.replace('DollarsPerMegawattHour',
                                                      'Med$PerMWHr')

    avgs = [a for a in full_data['Avg$PerMWHr']]
    meds = [m for m in full_data['Med$PerMWHr']]
    avgs.insert(0, avgs[0])
    avgs.pop()
    meds.insert(0, meds[0])
    meds.pop()
    full_data['PrevAvg$PerMWHr'] = avgs
    full_data['PrevMed$PerMWHr'] = meds

    full_data = full_data.drop(columns='IntTime')
    full_data['SinPeriod'], full_data['CosPeriod'] = cyclic_encoder(full_data.index, max=48)
    date_col = []
    for day, month, period in zip(full_data['Day'], full_data['Month'], full_data.index):
        value = day + (period - 1) / 48
        for m in range(1, int(month)):
            value += month_date_dict[m]
        date_col.append(value)
    full_data['SinDate'], full_data['CosDate'] = cyclic_encoder(date_col, max=365)

    for column in full_data.columns:
        full_data[column] = [round(d, 8) for d in full_data[column]]

    filename = "all_" + poc + "_data.csv"

    if not os.path.exists('./full_data'):
        os.makedirs('./full_data')

    full_data.to_csv('./full_data/' + filename)

    if not os.path.exists('./datasets'):
        os.makedirs('./datasets')

    for t in ts:
        for d in delay:
            if not os.path.exists(f'./datasets/{poc}'):
                os.makedirs(f'./datasets/{poc}')
            delay_in_hour = f"{(d / 2):.0f}" if (d / 2).is_integer() else f"{(d / 2):.1f}"
            df = make_targets_with_delay(pd.read_csv(f'./full_data/all_{p}_data.csv'), delay=d, target=t)
            df.to_csv(
                f'./datasets/{poc}/{poc}_{t[:3].lower()}_{delay_in_hour}hr.csv', index=False
            )
            print(f'File witten: ./datasets/{poc}/{poc}_{t[:3].lower()}_{delay_in_hour}hr.csv')
            if arff_option:
                csv_to_arff(
                    f'./datasets/{poc}/{poc}_{t[:3].lower()}_{delay_in_hour}hr.csv',
                    f'./datasets/{poc}/{poc}_{t[:3].lower()}_{delay_in_hour}hr.arff',
                    relation_name=f'relation: PoC: {poc}; Target: {t}; Delay: {delay_in_hour}hr'
                )



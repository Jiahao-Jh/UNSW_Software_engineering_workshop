'''
File: dataset.py
File Created: Tuesday, 15th March 2022 1:08:01 pm
Author: Hu Shuhao (hu.shuhao@outlook.com)
'''
import pandas as pd


def parse_dataset(location, county, date):
    df = pd.read_csv('covid_19_data.csv')
    if location == '':
        res = df[df['ObservationDate'] == date].groupby(
            by='Country/Region').sum()
        if county not in df['Country/Region'].values:
            return -1
        return {
            "Confirmed": int(res.loc[county, 'Confirmed']),
            "Recovered": int(res.loc[county, 'Recovered']),
            "Deaths": int(res.loc[county, 'Deaths'])
        }
    else:
        res = df[df['ObservationDate'] == date]
        res = res[res['Province/State'] == location]
        res = res[res['Country/Region'] == county]
        if len(res) == 0:
            # indicate no result found
            return -1
        return {
            "Confirmed": int(res.iloc[0]['Confirmed']),
            "Recovered": int(res.iloc[0]['Recovered']),
            "Deaths": int(res.iloc[0]['Deaths'])
        }


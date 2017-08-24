from correlate import plot_correlations
import pandas as pd
import numpy as np


def plot_corellations_from_data(data, file_name, plot_title=None):
    corr = data.corr()
    corr = corr.drop('Unnamed: 0', axis=1)
    corr = corr.ix[1:, ]
    columns = list(data.columns.values)
    del columns[0]
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    plot_correlations(corr, file_name, columns, columns, mask=mask, plot_title=plot_title)


if __name__ == '__main__':
    data = pd.read_csv('data/responses-norm.csv')
    data = data.drop('lecture', axis=1)
    plot_corellations_from_data(data, "correlations-raw.png")
    plot_corellations_from_data(data[data['in_15x4'] == 0].drop('in_15x4', axis=1), "correlations-raw-out.png", "Не участники")
    plot_corellations_from_data(data[data['in_15x4'] == 1].drop('in_15x4', axis=1), "correlations-raw-in.png", "Участники")

from scipy.stats import pearsonr, spearmanr


def dataset_overview(dataset):
    print(dataset.head())
    print(dataset.describe(include='all'))
    print(dataset.skew(0))


def print_correlation(dataset, correlation='Pearsons', key1='pm1', key2='wind_speed'):
    if correlation == 'Pearsons':
        corr, _ = pearsonr(dataset[key1].tolist(), dataset[key2].tolist())
    if correlation == 'Spearman':
        corr, _ = spearmanr(dataset[key1].tolist(), dataset[key2].tolist())
    print(correlation, 'correlation', key1, 'vs', key2, ': %.3f\t' % corr)


def dataset_correlations(dataset):
    # Direct correlation pm VS time doesn't work, because it's high, then low, then high
    # So I tried shifting it by 18 hours, so it's high then low
    # Works a bit, but we should search a better method
    # ls = list(map(lambda x: (x + 18) % 24, dataset['time_from'].tolist()))
    # print(len(ls))
    # corr, _ = pearsonr(dataset['pm10'].tolist(), ls)
    # print('Pearsons correlation: %.3f' % corr)
    # corr, _ = spearmanr(dataset['pm10'].tolist(), ls)
    # print('Spearman correlation: %.3f' % corr)
    print_correlation(dataset, 'Pearsons', 'pm10', 'pressure')
    print_correlation(dataset, 'Pearsons', 'pm10', 'humidity')
    print_correlation(dataset, 'Pearsons', 'pm10', 'temperature')
    print_correlation(dataset, 'Pearsons', 'pm10', 'wind_speed')
    print_correlation(dataset, 'Spearman', 'pm10', 'pressure')
    print_correlation(dataset, 'Spearman', 'pm10', 'humidity')
    print_correlation(dataset, 'Spearman', 'pm10', 'temperature')
    print_correlation(dataset, 'Spearman', 'pm10', 'wind_speed')
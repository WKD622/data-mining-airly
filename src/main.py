from src.helpers.database import perform_select_and_save_to_csv
from pandas import read_csv
from pandas.plotting import scatter_matrix
from src.helpers.consts import OUTPUT_DATA_FOLDER_NAME
from matplotlib import pyplot
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
    #Direct correlation pm VS time doesn't work, because it's high, then low, then high
    #So I tried shifting it by 18 hours, so it's high then low
    #Works a bit, but we should search a better method
    #ls = list(map(lambda x: (x + 18) % 24, dataset['time_from'].tolist()))
    #print(len(ls))
    #corr, _ = pearsonr(dataset['pm10'].tolist(), ls)
    #print('Pearsons correlation: %.3f' % corr)
    #corr, _ = spearmanr(dataset['pm10'].tolist(), ls)
    #print('Spearman correlation: %.3f' % corr)
    print_correlation(dataset, 'Pearsons', 'pm10', 'pressure')
    print_correlation(dataset, 'Pearsons', 'pm10', 'humidity')
    print_correlation(dataset, 'Pearsons', 'pm10', 'temperature')
    print_correlation(dataset, 'Pearsons', 'pm10', 'wind_speed')
    print_correlation(dataset, 'Spearman', 'pm10', 'pressure')
    print_correlation(dataset, 'Spearman', 'pm10', 'humidity')
    print_correlation(dataset, 'Spearman', 'pm10', 'temperature')
    print_correlation(dataset, 'Spearman', 'pm10', 'wind_speed')

data_filename = 'result.csv'
output_columns = ['sensor_id','datetime_from','datetime_to','pm1','pm25','pm10','pressure','humidity','temperature','wind_speed','wind_bearing']
output_columns_string = ','.join(output_columns)
command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL")
perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns)
dataset = read_csv(OUTPUT_DATA_FOLDER_NAME+'/'+data_filename)
dataset_overview(dataset)
dataset_correlations(dataset)

#Example of all vs all scatter_matrix
scatter_matrix(dataset[['pm1','pm25','pm10','time_from','pressure','humidity','temperature','wind_speed','wind_bearing']],figsize=(19.2,10.8),s=5)
pyplot.savefig(OUTPUT_DATA_FOLDER_NAME+'/'+'scatter_matrix_all_vs_all.png')

#Example of 3-feature scatter: humidity vs windspeed vs pm10 (color)
dataset.plot.scatter(x='humidity', y='wind_speed', c='pm10', colormap='Reds', s=3,figsize=(19.2,10.8))
pyplot.savefig(OUTPUT_DATA_FOLDER_NAME+'/'+'color_scatter_pm10_humidity_vs_windspeed.png')


#Example of history plot: average pm10 from all sensors per hour
output_columns = ['datetime_from','avg(pm1)','avg(pm25)','avg(pm10)','avg(pressure)','avg(humidity)','avg(temperature)','avg(wind_speed)','avg(wind_bearing)']
output_columns_string = ','.join(output_columns)
command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL GROUP BY datetime_from")
perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns, convert_datetime=False)
dataset = read_csv(OUTPUT_DATA_FOLDER_NAME+'/'+data_filename)
dataset.plot.line(x='datetime_from', y='avg(pm10)', figsize=(19.2,10.8))
pyplot.xticks(rotation=90)
pyplot.savefig(OUTPUT_DATA_FOLDER_NAME+'/'+'history_avg(pm10)_all_sensors_per_hour.png')

#Example of history plot: average pm10, humidity and wind speed from all sensors per day
output_columns = ['DATE(datetime_from)','avg(pm1)','avg(pm25)','avg(pm10)','avg(pressure)','avg(humidity)','avg(temperature)','avg(wind_speed)','avg(wind_bearing)']
output_columns_string = ','.join(output_columns)
command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL GROUP BY DATE(datetime_from)")
perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns, convert_datetime=False)
dataset = read_csv(OUTPUT_DATA_FOLDER_NAME+'/'+data_filename)
dataset.plot.line(x='DATE(datetime_from)', y=['avg(pm10)', 'avg(humidity)', 'avg(wind_speed)'], figsize=(19.2,10.8))
pyplot.xticks(rotation=90)
pyplot.savefig(OUTPUT_DATA_FOLDER_NAME+'/'+'history_avg(pm10)_avg(humidity)_avg(wind_speed)_all_sensors_per_day.png')

#Example of history plot: pm10 from each sensor per day
output_columns = ['sensor_id', 'DATE(datetime_from)','avg(pm1)','avg(pm25)','avg(pm10)','avg(pressure)','avg(humidity)','avg(temperature)','avg(wind_speed)','avg(wind_bearing)']
output_columns_string = ','.join(output_columns)
command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL GROUP BY DATE(datetime_from), sensor_id")
perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns, convert_datetime=False)
dataset = read_csv(OUTPUT_DATA_FOLDER_NAME+'/'+data_filename)
dataset=dataset.pivot(index='DATE(datetime_from)', columns='sensor_id', values='avg(pm10)')
dataset.plot(figsize=(19.2,10.8))
pyplot.xticks(rotation=90)
pyplot.savefig(OUTPUT_DATA_FOLDER_NAME+'/'+'history_pm10_per_day.png')

#Example of timeline plot: average pm10 from each sensor (not working properly)
output_columns = ['sensor_id', 'TIME(datetime_from)','avg(pm1)','avg(pm25)','avg(pm10)','avg(pressure)','avg(humidity)','avg(temperature)','avg(wind_speed)','avg(wind_bearing)']
output_columns_string = ','.join(output_columns)
command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL GROUP BY TIME(datetime_from), sensor_id")
perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns, convert_datetime=False)
dataset = read_csv(OUTPUT_DATA_FOLDER_NAME+'/'+data_filename)
dataset=dataset.pivot(index='TIME(datetime_from)', columns='sensor_id', values='avg(pm10)')
dataset.plot(figsize=(19.2,10.8))
pyplot.xticks(rotation=90)
pyplot.savefig(OUTPUT_DATA_FOLDER_NAME+'/'+'timeline_avg(pm10)_whole_day.png')
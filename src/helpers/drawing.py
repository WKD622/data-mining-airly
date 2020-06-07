from matplotlib import pyplot
from pandas import read_csv
from pandas.plotting import scatter_matrix

from src.helpers.consts import OUTPUT_DATA_FOLDER_NAME
from src.helpers.database import perform_select_and_save_to_csv
from src.helpers.drawing_helpers import dataset_overview, dataset_correlations


def all_vs_all_scatter_matrix(data_filename):
    output_columns = ['sensor_id', 'datetime_from', 'datetime_to', 'pm1', 'pm25', 'pm10', 'pressure', 'humidity',
                      'temperature', 'wind_speed', 'wind_bearing']
    output_columns_string = ','.join(output_columns)
    command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset_overview(dataset)
    dataset_correlations(dataset)
    scatter_matrix(
        dataset[
            ['pm1', 'pm25', 'pm10', 'time_from', 'pressure', 'humidity', 'temperature', 'wind_speed', 'wind_bearing']],
        figsize=(19.2, 10.8), s=5)
    pyplot.savefig(OUTPUT_DATA_FOLDER_NAME + '/' + 'scatter_matrix_all_vs_all.png')


def average_pm10_from_all_sensors_per_hour(data_filename):
    output_columns = ['datetime_from', 'avg(pm10)']
    output_columns_string = ','.join(output_columns)
    command = (
        f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL GROUP BY datetime_from")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                                   convert_datetime=False)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset.plot.line(x='datetime_from', y='avg(pm10)', figsize=(19.2, 10.8))
    pyplot.xticks(rotation=90)
    pyplot.ylabel('average pm10')
    pyplot.savefig(OUTPUT_DATA_FOLDER_NAME + '/' + 'history_avg(pm10)_all_sensors_per_hour.png')


def average_pm10_humidity_and_wind_speed_from_all_sensors_per_day(data_filename):
    output_columns = ['DATE(datetime_from)', 'avg(pm1)', 'avg(pm25)', 'avg(pm10)', 'avg(pressure)', 'avg(humidity)',
                      'avg(temperature)', 'avg(wind_speed)', 'avg(wind_bearing)']
    output_columns_string = ','.join(output_columns)
    command = (
        f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND sensor_id in (239, 10051, 329, 2545) AND pressure IS NOT NULL GROUP BY DATE(datetime_from)")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                                   convert_datetime=False)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset.plot.line(x='DATE(datetime_from)', y=['avg(pressure)'],
                      figsize=(19.2, 10.8))
    pyplot.xticks(rotation=90)
    pyplot.savefig(
        OUTPUT_DATA_FOLDER_NAME + '/' + 'history_avg(pm10)_avg(humidity)_avg(wind_speed)_all_sensors_per_day.png')


def pm10_from_each_sensor_per_day(data_filename):
    output_columns = ['sensor_id', 'DATE(datetime_from)', 'avg(pm1)', 'avg(pm25)', 'avg(pm10)', 'avg(pressure)',
                      'avg(humidity)', 'avg(temperature)', 'avg(wind_speed)', 'avg(wind_bearing)']
    output_columns_string = ','.join(output_columns)
    command = (
        f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL GROUP BY DATE(datetime_from), sensor_id")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                                   convert_datetime=False)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset = dataset.pivot(index='DATE(datetime_from)', columns='sensor_id', values='avg(pm10)')
    dataset.plot(figsize=(19.2, 10.8))
    pyplot.xticks(rotation=90)
    pyplot.ylabel('average pm10')
    pyplot.savefig(OUTPUT_DATA_FOLDER_NAME + '/' + 'history_pm10_per_day.png')


def average_pm10_from_each_sensor_not_working_properly(data_filename):
    output_columns = ['sensor_id', 'TIME(datetime_from)', 'avg(pm1)', 'avg(pm25)', 'avg(pm10)', 'avg(pressure)',
                      'avg(humidity)', 'avg(temperature)', 'avg(wind_speed)', 'avg(wind_bearing)']
    output_columns_string = ','.join(output_columns)
    command = (
        f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL GROUP BY TIME(datetime_from), sensor_id")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                                   convert_datetime=False)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset = dataset.pivot(index='TIME(datetime_from)', columns='sensor_id', values='avg(pm10)')
    dataset.plot(figsize=(19.2, 10.8))
    pyplot.xticks(rotation=90)
    pyplot.ylabel('average pm10')
    pyplot.savefig(OUTPUT_DATA_FOLDER_NAME + '/' + 'timeline_avg(pm10)_whole_day.png')


def humidity_vs_wind_speed_vs_pm10(data_filename):
    output_columns = ['sensor_id', 'datetime_from', 'datetime_to', 'pm1', 'pm25', 'pm10', 'pressure', 'humidity',
                      'temperature', 'wind_speed', 'wind_bearing']
    output_columns_string = ','.join(output_columns)
    command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset.plot.scatter(x='humidity', y='wind_speed', c='pm10', colormap='Reds', s=3, figsize=(19.2, 10.8))
    pyplot.savefig(OUTPUT_DATA_FOLDER_NAME + '/' + 'color_scatter_pm10_humidity_vs_windspeed.png')


def scatter_pm10_wind_speed(data_filename):
    output_columns = ['sensor_id', 'datetime_from', 'datetime_to', 'pm1', 'pm25', 'pm10', 'pressure', 'humidity',
                      'temperature', 'wind_speed', 'wind_bearing']
    output_columns_string = ','.join(output_columns)
    command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset.plot.scatter(x='pm10', y='wind_speed', s=2, figsize=(19.2, 10.8))
    pyplot.savefig(OUTPUT_DATA_FOLDER_NAME + '/' + 'color_scatter_pm10_wind_speed.png')


def pm10_humidity_and_wind_speed(data_filename):
    output_columns = ['DATE(datetime_from)', 'pm1', 'pm25', 'pm10', 'pressure', 'humidity',
                      'temperature', 'wind_speed', 'wind_bearing']
    output_columns_string = ','.join(output_columns)
    command = (
        f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL AND sensor_id=239")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                                   convert_datetime=False)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset.plot.line(x='DATE(datetime_from)', y=['pm10', 'wind_speed'],
                      figsize=(19.2, 10.8))
    pyplot.xticks(rotation=90)
    pyplot.savefig(
        OUTPUT_DATA_FOLDER_NAME + '/' + 'history_(pm10)_wind_speed_all_sensors_per_day.png')


def wind_bearing(data_filename):
    output_columns = ['DATE(datetime_from)', 'pm1', 'pm25', 'pm10', 'pressure', 'humidity',
                      'temperature', 'wind_speed', 'wind_bearing']
    output_columns_string = ','.join(output_columns)
    command = (
        f"SELECT {output_columns_string} FROM measurements WHERE wind_bearing IS NOT NULL AND sensor_id=239")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                                   convert_datetime=False)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset.plot.line(x='DATE(datetime_from)', y=['wind_bearing', 'wind_speed'],
                      figsize=(19.2, 10.8))
    pyplot.xticks(rotation=90)
    pyplot.savefig(
        OUTPUT_DATA_FOLDER_NAME + '/' + 'wind_bearing.png')


def pm10_for_6649(data_filename):
    output_columns = ['DATE(datetime_from)', 'pm1', 'pm25', 'pm10', 'pressure', 'humidity',
                      'temperature', 'wind_speed', 'wind_bearing']
    output_columns_string = ','.join(output_columns)
    command = (
        f"SELECT {output_columns_string} FROM measurements WHERE sensor_id=6649 AND datetime_from > '2020-03-23' AND datetime_from < '2020-03-27'")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                                   convert_datetime=False)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset.plot.line(x='DATE(datetime_from)', y=['pm10', 'wind_bearing', 'wind_speed'],
                      figsize=(19.2, 10.8))
    pyplot.xticks(rotation=90)
    pyplot.savefig(
        OUTPUT_DATA_FOLDER_NAME + '/' + 'pm10_6649.png')


def pm10_for_10048(data_filename):
    output_columns = ['DATE(datetime_from)', 'pm1', 'pm25', 'pm10', 'pressure', 'humidity',
                      'temperature', 'wind_speed', 'wind_bearing']
    output_columns_string = ','.join(output_columns)
    command = (
        f"SELECT {output_columns_string} FROM measurements WHERE sensor_id=10048 AND datetime_from > '2020-03-23' AND datetime_from < '2020-03-27'")
    perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                                   convert_datetime=False)
    dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)
    dataset.plot.line(x='DATE(datetime_from)', y=['pm10'],
                      figsize=(19.2, 10.8))
    pyplot.xticks(rotation=90)
    pyplot.savefig(
        OUTPUT_DATA_FOLDER_NAME + '/' + 'pm10_10048.png')

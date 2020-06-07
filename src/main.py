from src.helpers.drawing import average_pm10_from_all_sensors_per_hour, \
    average_pm10_humidity_and_wind_speed_from_all_sensors_per_day, pm10_from_each_sensor_per_day, \
    average_pm10_from_each_sensor_not_working_properly, humidity_vs_wind_speed_vs_pm10, all_vs_all_scatter_matrix, \
    scatter_pm10_wind_speed, pm10_humidity_and_wind_speed, wind_bearing, pm10_for_6649, pm10_for_10048

data_filename = 'result.csv'
# all_vs_all_scatter_matrix(data_filename)
# humidity_vs_wind_speed_vs_pm10(data_filename)
average_pm10_from_all_sensors_per_hour(data_filename)
# average_pm10_humidity_and_wind_speed_from_all_sensors_per_day(data_filename)
# pm10_from_each_sensor_per_day(data_filename)
# average_pm10_from_each_sensor_not_working_properly(data_filename)
# scatter_pm10_wind_speed(data_filename)
# pm10_humidity_and_wind_speed(data_filename)
# wind_bearing(data_filename)
# pm10_for_6649(data_filename)
# pm10_for_10048(data_filename)
from src.helpers.database import perform_select_and_save_to_csv
from pandas import read_csv
from pandas.plotting import scatter_matrix
from src.helpers.consts import OUTPUT_DATA_FOLDER_NAME
from matplotlib import pyplot
output_columns = ['sensor_id','datetime_from','datetime_to','pm1','pm25','pm10','pressure','humidity','temperature','wind_speed','wind_bearing']
output_columns_string = ','.join(output_columns)

command = (f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL")
data_filename = 'result.csv'

perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns)

dataset = read_csv(OUTPUT_DATA_FOLDER_NAME+'/'+data_filename)
print(dataset.describe(include='all'))
print(dataset.head())
print(dataset.skew(0))
print(dataset.groupby("sensor_id").size())
scatter_matrix(dataset[['pm1','pm25','pm10','time_from','pressure','humidity','temperature','wind_speed','wind_bearing']],figsize=(19.2,10.8),s=5)
pyplot.savefig(OUTPUT_DATA_FOLDER_NAME+'/'+'data_drawn.png')
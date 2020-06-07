from pandas import read_csv
import pandas as pd
from src.helpers.consts import OUTPUT_DATA_FOLDER_NAME
from src.helpers.database import perform_select_and_save_to_csv
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import statsmodels.api as sm

data_filename = 'result.csv'
output_columns = ['datetime_from', 'avg(pm10)', 'avg(humidity)']
output_columns_string = ','.join(output_columns)
command = (
    f"SELECT {output_columns_string} FROM measurements WHERE pm1 IS NOT NULL AND pressure IS NOT NULL GROUP BY datetime_from")
perform_select_and_save_to_csv(select_command=command, output_filename=data_filename, columns=output_columns,
                               convert_datetime=False)
dataset = read_csv(OUTPUT_DATA_FOLDER_NAME + '/' + data_filename)

dataset_for_prediction = dataset.copy()
dataset_for_prediction['actual'] = dataset_for_prediction['avg(pm10)'].shift(-1)

dataset_for_prediction['datetime_from'] = pd.to_datetime(dataset_for_prediction['datetime_from'])
dataset_for_prediction.index = dataset_for_prediction['datetime_from']

dataset_for_prediction['avg(pm10)'].plot(color='green', figsize=(15, 2))
plt.show()
dataset_for_prediction['avg(humidity)'].plot(color='blue', figsize=(15, 2))
plt.show()

sc_in = MinMaxScaler(feature_range=(0, 1))
scaled_input = sc_in.fit_transform(dataset_for_prediction[['avg(pm10)', 'avg(humidity)']])
scaled_input = pd.DataFrame(scaled_input)
X = scaled_input

sc_out = MinMaxScaler(feature_range=(0, 1))
scaler_output = sc_out.fit_transform(dataset_for_prediction[['actual']])
scaler_output = pd.DataFrame(scaler_output)
y = scaler_output

X.rename(columns={0: 'pm10', 1: 'humidity'}, inplace=True)
y.rename(columns={0: 'pm10 prediction'}, inplace=True)

train_size = int(len(dataset) * 0.7)
test_size = int(len(dataset)) - train_size

train_X, train_y = X[:train_size].dropna(), y[:train_size].dropna()
test_X, test_y = X[train_size:].dropna(), y[train_size:].dropna()

# dataset.plot.line(x='datetime_from', y='avg(pm10)', figsize=(19.2, 10.8))
# pyplot.xticks(rotation=90)
# pyplot.ylabel('average pm10')
# pyplot.savefig(OUTPUT_DATA_FOLDER_NAME + '/' + 'history_avg(pm10)_all_sensors_per_hour.png')

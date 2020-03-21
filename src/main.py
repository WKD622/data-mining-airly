from src.helpers.database import perform_select_and_save_to_csv

output_columns = ['sensor_id', 'pm10']

command = (f"SELECT sensor_id, sum(pm10) FROM measurements WHERE sensor_id=239 group by sensor_id")
output_filename = 'result.csv'

perform_select_and_save_to_csv(select_command=command, output_filename=output_filename, columns=output_columns)

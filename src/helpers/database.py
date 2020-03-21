import os
import mysql.connector

from src.helpers.consts import OUTPUT_DATA_FOLDER_NAME, DATABASE_CONFIG


def get_csv_line_from_response_row(row, datetime_from_index, datetime_to_index):
    data = []
    for index, field in enumerate(row):
        if index == datetime_to_index or index == datetime_from_index:
            data.append(str(field.date()))
            data.append(str(field.time().hour))
        else:
            data.append(str(field))
    return ','.join(data) + '\n'


def get_file_header(columns):
    header = []
    for name in columns:
        if name == 'datetime_from':
            header.append('date_from')
            header.append('time_from')
        elif name == 'datetime_to':
            header.append('date_to')
            header.append('time_to')
        else:
            header.append(name)
    return ','.join(header) + '\n'


def save_data_to_csv(data, filename, columns):
    try:
        datetime_from_index = columns.index('datetime_from')
    except:
        datetime_from_index = None
    try:
        datetime_to_index = columns.index('datetime_to')
    except:
        datetime_to_index = None

    file = open(filename, 'w')
    file.write(get_file_header(columns))
    for row in data:
        line = get_csv_line_from_response_row(row=row,
                                              datetime_from_index=datetime_from_index,
                                              datetime_to_index=datetime_to_index)
        file.write(line)
    file.close()
    print('Saved to: ' + filename)


def execute(database, select_command):
    my_cursor = database.cursor()
    try:
        my_cursor.execute(select_command)
        print('\nData fetched successfully.')
        return my_cursor.fetchall()
    except Exception as error:
        database.rollback()
        print(error)


def perform_select_and_save_to_csv(select_command, output_filename, columns):
    try:
        os.mkdir(OUTPUT_DATA_FOLDER_NAME)
    except OSError:
        pass

    filepath = os.path.join(OUTPUT_DATA_FOLDER_NAME, output_filename)

    my_db = mysql.connector.connect(**DATABASE_CONFIG)

    data = execute(database=my_db, select_command=select_command)
    save_data_to_csv(data, filepath, columns)

    my_db.close()

import requests, gzip, shutil, os, schedule, time
from csv import writer, reader
from slugify import slugify
from api.response import format_city

def add_column_in_csv(input_file, output_file, transform_row):
    with open(input_file, 'r') as read_obj, open(output_file, 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
        for row in csv_reader:
            transform_row(row, csv_reader.line_num)
            csv_writer.writerow(row)

def get_csv_cases_states():
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
    req = requests.get(url).content

    with open('database/cases-brazil-states.csv', 'wb') as f:
        f.write(req)
        f.close()

    print('states finished')

def get_csv_cases_cities():
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv.gz"
    req = requests.get(url).content

    file_gz_path = 'cases-brazil-cities-time.csv.gz'
    start_file = 'database/cases-brazil-cities-time-slug.csv'
    end_file = 'database/cases-brazil-cities-time.csv'

    with open(file_gz_path, 'wb') as f:
        f.write(req)
        f.close()

    print('cities downloaded')

    with gzip.open(file_gz_path, 'rb') as f_in:
        with open(start_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            f_out.close()
        f_in.close()

    print('cities unzip')

    if os.path.exists(file_gz_path):
        os.remove(file_gz_path)
    
    header_of_new_col = 'slug'
    add_column_in_csv(start_file, end_file, lambda row, line_num: row.append(header_of_new_col) if line_num == 1 else row.append(slugify(format_city(row[4]))))

    if os.path.exists(start_file):
        os.remove(start_file)

    print('cities finished')


def job():
    get_csv_cases_states()
    get_csv_cases_cities()

schedule.every().day.at("02:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
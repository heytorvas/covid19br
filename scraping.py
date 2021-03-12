import requests, gzip, shutil, os, schedule, time

def get_csv_cases_states():
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
    req = requests.get(url).content

    with open('database/cases-brazil-states.csv', 'wb') as f:
        f.write(req)
        f.close()

def get_csv_cases_cities():
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv.gz"
    req = requests.get(url).content

    file_gz_path = 'cases-brazil-cities-time.csv.gz'

    with open(file_gz_path, 'wb') as f:
        f.write(req)
        f.close()

    with gzip.open(file_gz_path, 'rb') as f_in:
        with open('database/cases-brazil-cities-time.csv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            f_out.close()
        f_in.close()

    if os.path.exists(file_gz_path):
        os.remove(file_gz_path)

def job():
    get_csv_cases_states()
    get_csv_cases_cities()

schedule.every().day.at("02:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
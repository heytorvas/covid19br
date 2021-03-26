import pandas, json
from datetime import datetime
from slugify import slugify

def get_data_pandas(path):
    return pandas.read_csv(path)

def format_city(city):
    return city.split('/')[0]

def convert_df_json(df):
    list_dict = []
    for index, row in list(df.iterrows()):
        row['date'] = row['date'].__str__()
        list_dict.append(dict(row))
    
    return json.dumps(list_dict, ensure_ascii=False)

def get_general_cases(state, args):
    df = get_data_pandas('database/cases-brazil-states.csv')
    df['date'] = pandas.to_datetime(df['date'])
    
    if args[0] == None or args[1] == None:
        mask = (df['state'] == state)
        return df.loc[mask]

    else:
        mask = (df['date'] >= datetime.strptime(args[0], '%Y-%m-%d')) & (df['date'] <= datetime.strptime(args[1], '%Y-%m-%d')) & (df['state'] == state)
        return df.loc[mask]

def get_cities_cases(state, city, args):
    df = get_data_pandas('database/cases-brazil-cities-time.csv')
    df['date'] = pandas.to_datetime(df['date'])
    df['city'] = df['city'].apply(lambda x : format_city(x))

    if args[0] == None or args[1] == None:
        mask = (df['state'] == state) & (df['slug'] == slugify(city))
        return df.loc[mask]
    
    else:
        mask = (df['state'] == state) & (df['slug'] == slugify(city)) & (df['date'] >= datetime.strptime(args[0], '%Y-%m-%d')) & (df['date'] <= datetime.strptime(args[1], '%Y-%m-%d'))
        return df.loc[mask]
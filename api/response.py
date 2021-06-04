import pandas, json, csv
from datetime import datetime
from slugify import slugify
from json2xml import json2xml
from json2xml.utils import readfromstring

def convert_df_csv(toCSV):
    keys = toCSV[0].keys()
    with open('api/result.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

def get_json_cities_state(state):
    df = get_data_pandas('database/cases-brazil-cities-time.csv')
    mask = (df['state'] == state)
    df_mask = df.loc[mask]
    return get_cities_state(df_mask['city'].unique().tolist())

def get_json_cities_brazil():
    df = get_data_pandas('database/cases-brazil-cities-time.csv')
    return get_cities_state(df['city'].unique().tolist())

def get_cities_state(df_city):
    city_list = []
    df_city = sorted(df_city)
    for city in df_city:
        if 'CASO' in city or 'TOTAL' in city:
            pass
        else:
            city_list.append({
                'slug': slugify(city.split('/')[0].strip()),
                'city': city.split('/')[0].strip(),
                'state': city.split('/')[1].strip()
            })
    return json.dumps(city_list, ensure_ascii=False)

def get_data_pandas(path):
    return pandas.read_csv(path)

def format_city(city):
    return city.split('/')[0]

def set_limit_response(df, args):
    limit = len(df.index)
    if args is not None:
        return int(args)
    else:
        return limit

def convert_df_xml(df):
    list_dict = []
    for index, row in list(df.iterrows()):
        row['date'] = row['date'].__str__()
        list_dict.append(dict(row))
    json_dict = readfromstring(str(json.dumps(list_dict, ensure_ascii=False)))
    return json2xml.Json2xml(json_dict, wrapper="all", pretty=True).to_xml()

def convert_df_json(df):
    list_dict = []
    for index, row in list(df.iterrows()):
        row['date'] = row['date'].__str__()
        list_dict.append(dict(row))
    
    return json.dumps(list_dict, ensure_ascii=False)

def convert_df_dict(df):
    list_dict = []
    for index, row in list(df.iterrows()):
        row['date'] = row['date'].__str__()
        list_dict.append(dict(row))

    return list_dict

def get_general_cases(state, args):
    df = get_data_pandas('database/cases-brazil-states.csv')
    df['date'] = pandas.to_datetime(df['date'])

    limit = set_limit_response(df, args[2])
    
    if args[0] == None or args[1] == None:
        mask = (df['state'] == state)
        df_mask = df.loc[mask]
        return df_mask.tail(limit)

    else:
        mask = (df['date'] >= datetime.strptime(args[0], '%Y-%m-%d')) & (df['date'] <= datetime.strptime(args[1], '%Y-%m-%d')) & (df['state'] == state)
        df_mask = df.loc[mask]
        return df_mask.tail(limit)

def get_cities_cases(state, city, args):
    df = get_data_pandas('database/cases-brazil-cities-time.csv')
    df['date'] = pandas.to_datetime(df['date'])
    df['city'] = df['city'].apply(lambda x : format_city(x))
    limit = set_limit_response(df, args[2])

    if args[0] == None or args[1] == None:
        mask = (df['state'] == state) & (df['slug'] == slugify(city))
        df_mask = df.loc[mask]
        return df_mask.tail(limit)
    
    else:
        mask = (df['state'] == state) & (df['slug'] == slugify(city)) & (df['date'] >= datetime.strptime(args[0], '%Y-%m-%d')) & (df['date'] <= datetime.strptime(args[1], '%Y-%m-%d'))
        df_mask = df.loc[mask]
        return df_mask.tail(limit)
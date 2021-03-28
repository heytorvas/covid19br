import pandas, json
from datetime import datetime
from slugify import slugify

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

def convert_df_json(df):
    list_dict = []
    for index, row in list(df.iterrows()):
        row['date'] = row['date'].__str__()
        list_dict.append(dict(row))
    
    return json.dumps(list_dict, ensure_ascii=False)

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
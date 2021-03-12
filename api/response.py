import pandas, json

def get_data_pandas(path):
    return pandas.read_csv(path)

def convert_df_json(df):
    list_dict = []
    for index, row in list(df.iterrows()):
        list_dict.append(dict(row))
    
    return json.dumps(list_dict)

def get_general_cases(state):
    df = get_data_pandas('database/cases-brazil-states.csv')
    # df['date'] = pandas.to_datetime(df['date'])
    # mask = (df['date'] > str(args[0])) & (df['date'] <= str(args[1])) & (df['state'] == state)
    # df['date'] = df['date'].astype(str)
    return df.loc[df['state'] == state]
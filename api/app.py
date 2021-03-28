from flask import Flask
from flask import request
from response import *

app = Flask(__name__)

def query_string():
    args_list = []
    args_list.append(request.args.get('start'))
    args_list.append(request.args.get('end'))
    args_list.append(request.args.get('limit'))
    return args_list

@app.route("/api/brazil/")
def brazil():
    args = query_string()
    df = get_general_cases('TOTAL', args)
    return convert_df_json(df)

@app.route("/api/brazil/<state>/")
def by_state(state):
    args = query_string()
    df = get_general_cases(state.upper(), args)
    return convert_df_json(df)

@app.route("/api/brazil/<state>/<city>/")
def by_city(state, city):
    args = query_string()
    df = get_cities_cases(state.upper(), city, args)
    return convert_df_json(df)

if __name__ == "__main__":
    app.run()
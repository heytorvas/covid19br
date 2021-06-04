from response import convert_df_dict, convert_df_csv, convert_df_json, convert_df_xml
from flask import Flask, Response, request, send_file
from response import *
import json, csv, os

app = Flask(__name__)

def query_string():
    args_list = []
    args_list.append(request.args.get('start'))
    args_list.append(request.args.get('end'))
    args_list.append(request.args.get('limit'))
    args_list.append(request.args.get('format'))
    return args_list

def set_return_by_args(args, df):
    if args[3] == 'csv':
        json = convert_df_dict(df)
        convert_df_csv(json)
        return send_file(os.path.join('', 'result.csv'), as_attachment=True)
    elif args[3] == 'xml':
        return Response(convert_df_xml(df), mimetype='application/xml')
    else:
        return convert_df_json(df)

@app.route("/api/brazil/")
def brazil():
    args = query_string()
    df = get_general_cases('TOTAL', args)
    return set_return_by_args(args, df)

@app.route("/api/brazil/cities/")
def get_cities_from_brazil():
    return get_json_cities_brazil()

@app.route("/api/brazil/states/")
def get_states_from_brazil():
    f = open(('api/states.json'))
    data = json.load(f)
    return json.dumps(data, ensure_ascii=False)

@app.route("/api/brazil/<state>/")
def by_state(state):
    args = query_string()
    df = get_general_cases(state.upper(), args)
    return set_return_by_args(args, df)

@app.route("/api/brazil/<state>/<city>/")
def by_city(state, city):
    args = query_string()
    df = get_cities_cases(state.upper(), city, args)
    return set_return_by_args(args, df)

@app.route("/api/brazil/<state>/cities/")
def get_cities_from_state(state):
    return get_json_cities_state(state.upper())

if __name__ == "__main__":
    app.run()
from pandas_datapackage_reader import read_datapackage
from datetime import datetime

from flask import Flask, Response, request
app = Flask(__name__)

data = read_datapackage("")

def get_paginated_json(df, per_page, page):
    return df[page:page+per_page].to_json(orient='records')

@app.route('/')
@app.route('/api')
def api():
    try:
        per_page = int(request.args.get('per_page', 10))
    except:
        per_page = 1000

    try:
        page = (int(request.args.get('page', 1))-1)*per_page
    except:
        page = 1

    df = data.copy()["de-vaccinations"]
    dpf = []
    for fld in df._metadata['schema']['fields']:
        fn = fld['name']
        try:
            q = request.args.get(fn)
        except:
            q = None
        if q is not None:
            try:
                q = q.strip()
                df = df.loc[df[fn] == q]
                dpf.append({fn:q})
            except:
                pass

    return Response(
        '{"time": "%s","last_update": "2020-12-30T00:00","applied_filter": %s, "per_page": %i, "page": %i,"data": %s}' % (datetime.today().strftime('%Y-%m-%dT%H:%M:%S'),dpf,per_page, page, get_paginated_json(df,per_page,page)),
        mimetype='application/json',
        status=200)
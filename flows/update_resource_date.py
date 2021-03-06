from dataflows import Flow, update_resource
from datetime import datetime, timedelta
from dateutil import parser
import requests

try:
    r = requests.get('https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile')
    date = parser.parse(r.headers["Last-Modified"])
except:
    date = datetime.now()

def flow(parameters, *args):
    return Flow(
        update_resource(resources=parameters["resources"],
                        last_update=datetime.strftime(date - timedelta(1), '%Y-%m-%dT%H:%M')
        ),
        update_resource(resources=parameters["resources"],
                        last_published=datetime.strftime(date, '%Y-%m-%dT%H:%M')
        )
    )

# Entrypoint for running the flow directly, without Datapackage Pipelines
if __name__ == '__main__':
    # Add a printer step and run the flow
    Flow(flow(), printer(num_rows=1, tablefmt='html')).process()
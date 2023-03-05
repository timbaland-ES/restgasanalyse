from datetime import datetime
from random import randint

import time
from restgasanalyse.database import Database

from restgasanalyse.models import Measurement

def mock_sensor_data() -> Measurement:
    return Measurement(
        id = 10,
        value = randint(1, 23),
        timestamp = datetime.now()
    )


def run():
    db = Database(url='postgresql+psycopg2://postgres:password@localhost:5432/grafana')
    while 1:
        data = mock_sensor_data()
        print(data.value)
        db.store(data)

        time.sleep(1)

if __name__ == '__main__':
    run()
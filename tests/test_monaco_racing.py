import os
import pytest
from monaco_racing_flask.app import create_app
from monaco_racing_flask._db import create_test_db, leaderboard
from monaco_racing_flask.config import basedir
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


driver_model_keys = ['name', 'car', 'start', 'end']
drivers_abbr = leaderboard.keys()


@pytest.fixture()
def app():
    app = create_app('test')
    create_test_db()

    yield app

    os.remove(os.path.join(basedir, 'test_monaco_racing.db'))


@pytest.fixture
def client(app):
    return app.test_client()


def test_driver_wrong_id(client):
    with client:
        res = client.get('/api/v1/drivers/foo')
        assert res.status_code == 404


def test_driver_format_json(client):
    with client:
        res = client.get('/api/v1/drivers/DRR?format=json')
        assert res.status_code == 200

        res_driver = res.get_json(force=True)['DRR']
        assert all(key in driver_model_keys for key in res_driver.keys())


def test_driver_format_xml(client):
    with client:
        res = client.get('/api/v1/drivers/DRR?format=xml')
        assert res.status_code == 200

        root = ET.fromstring(res.data)
        res_keys_list = [_.tag for _ in root.find('.DRR')]
        assert all(key in driver_model_keys for key in res_keys_list)


def test_drivers_list_format_json(client):
    with client:
        res = client.get('/api/v1/drivers?format=json')
        assert res.status_code == 200

        res_driver = res.get_json(force=True)
        assert len(res_driver) == len(drivers_abbr)

        res_driver = res_driver.popitem()[1]
        assert all(key in driver_model_keys for key in res_driver.keys())


def test_drivers_list_format_xml(client):
    with client:
        res = client.get('/api/v1/drivers?format=xml')
        assert res.status_code == 200

        root = ET.fromstring(res.data)
        assert len(root) == len(drivers_abbr)

        res_keys_list = [_.tag for _ in root.find('.DRR')]
        assert all(key in driver_model_keys for key in res_keys_list)


def test_leaderboard_format_json(client):
    with client:
        res = client.get('/api/v1/leaderboard?format=json')
        assert res.status_code == 200

        res_drivers_list = res.get_json(force=True)
        assert all(key in drivers_abbr for key in res_drivers_list.keys())


def test_leaderboard_format_xml(client):
    with client:
        res = client.get('/api/v1/leaderboard?format=xml')
        assert res.status_code == 200

        root = ET.fromstring(res.data)
        res_drivers_list = [_.tag for _ in root.find('.')]
        assert all(key in drivers_abbr for key in res_drivers_list)


def test_leaderboard_order_asc(client):
    with client:
        res = client.get('/api/v1/leaderboard?format=json&order=asc')
        assert res.status_code == 200

        res_drivers_list = res.get_json(force=True)

        last_time = None
        for abbr, driver in res_drivers_list.items():
            t = datetime.strptime(driver['time'], '%H:%M:%S.%f')
            race_time = timedelta(hours=t.hour,
                                  minutes=t.minute,
                                  seconds=t.second,
                                  microseconds=t.microsecond)
            if last_time:
                assert race_time > last_time
            last_time = race_time


def test_leaderboard_order_desc(client):
    with client:
        res = client.get('/api/v1/leaderboard?format=json&order=desc')
        assert res.status_code == 200

        res_drivers_list = res.get_json(force=True)

        last_time = None
        for abbr, driver in res_drivers_list.items():
            t = datetime.strptime(driver['time'], '%H:%M:%S.%f')
            race_time = timedelta(hours=t.hour,
                                  minutes=t.minute,
                                  seconds=t.second,
                                  microseconds=t.microsecond)
            if last_time:
                assert race_time < last_time
            last_time = race_time

import os
from monaco_racing import RaceReport
from monaco_racing_flask.model.driver import Driver
from monaco_racing_flask.app import db_wrapper

PROJECT_DIR = os.path.dirname(__file__)
leaderboard = RaceReport(os.path.join(PROJECT_DIR, 'data'))


def create_test_db():
    db_wrapper.database.create_tables([Driver])
    for abbr, driver in leaderboard.items():
        Driver.create(abbr=abbr,
                      name=driver.name,
                      car=driver.car,
                      start=driver.start,
                      end=driver.end)
    db_wrapper.database.close()

from flask_restful import abort, Resource, reqparse
from .custom_encoders.custom_encoders import output_json, output_xml
from ..model.driver import Driver as Driver_Model
from peewee import DoesNotExist as DoesNotExistException


parser = reqparse.RequestParser()
parser.add_argument('format', type=str, default='JSON', help='Response format - JSON or XML')


class Driver(Resource):
    def get(self, driver_abbr):
        """
        Data about specific driver
        ---
        tags:
          - MonacoRacingAPI
        parameters:
          - in: path
            name: driver_abbr
            required: true
            description: The ID of the driver, try DRR!
            type: string
          - in: query
            name: format
            description: output format, by default JSON
            enum:
             - json
             - xml
            schema:
                type: string
        responses:
          200:
            description: Driver data
            schema:
              id: Driver
              properties:
                name:
                  type: string
                car:
                  type: string
                start:
                  type: string
                end:
                  type: string
        produces:
            - application/json
            - application/xml
        """
        args = parser.parse_args()

        try:
            driver = Driver_Model.get(Driver_Model.abbr == driver_abbr)
        except DoesNotExistException:
            abort(404, message="Driver {} doesn't exist".format(driver_abbr))

        driver = {driver.abbr: {'name': driver.name,
                                'car': driver.car,
                                'start': driver.start,
                                'end': driver.end}}

        if args['format'].upper() == 'JSON':
            return output_json(driver,
                               200,
                               {'content-type': 'application/json'})
        elif args['format'].upper() == 'XML':
            return output_xml(driver,
                              200,
                              {'content-type': 'application/xml'})
        else:
            return abort(400, message='format parameter can be json or xml')


class Driverslist(Resource):
    def get(self):
        """
        All drivers data
        ---
        tags:
          - MonacoRacingAPI
        parameters:
          - in: query
            name: format
            description: output format, by default JSON
            enum:
            - json
            - xml
            schema:
                type: string
        responses:
          200:
            description: Driver data
            schema:
                type: array
                items:
                    type: object
                    properties:
                        name:
                          type: string
                        car:
                          type: string
                        start:
                          type: string
                        end:
                          type: string
        produces:
            - application/json
            - application/xml
        """
        args = parser.parse_args()

        drivers = Driver_Model.select()
        drivers = {driver.abbr: {'name': driver.name,
                                 'car': driver.car,
                                 'start': driver.start,
                                 'end': driver.end} for driver in drivers}

        if args['format'].upper() == 'JSON':
            return output_json(drivers,
                               200,
                               {'content-type': 'application/json'})
        elif args['format'].upper() == 'XML':
            return output_xml(drivers,
                              200,
                              {'content-type': 'application/xml'})
        else:
            return abort(400, message='format parameter can be json or xml')

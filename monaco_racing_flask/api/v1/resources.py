from flask import Blueprint
from flask_restful import Api, Resource, abort, reqparse
from ..custom_encoders.custom_encoders import output_json, output_xml
from ..common import parser, Driver, Driverslist
from ...model.driver import Driver as Driver_Model


api_bp = Blueprint('api_v1', __name__)
api = Api(api_bp)
api.representations['application/json'] = output_json
api.representations['application/xml'] = output_xml

parser.add_argument('order', type=str, default='asc')

order = {'asc': False,
         'desc': True}


class Leaderboard(Resource):
    def get(self):
        """
        All drivers data with their race time.
        ---
        tags:
            - MonacoRacingAPI
        parameters:
          - in: query
            name: order
            description: output order
            enum:
                - asc
                - desc
            schema:
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
                type: array
                items:
                    type: object
                    properties:
                        name:
                          type: string
                        car:
                          type: string
                        time:
                          type: string
        produces:
            - application/json
            - application/xml
        """
        args = parser.parse_args()
        if args['order'].lower() not in order.keys():
            return abort(400, message='order  can be asc or desc')

        leaderboard = (Driver_Model
                       .select()
                       .where(Driver_Model.end > Driver_Model.start))

        leaderboard = {driver.abbr: {'name': driver.name,
                                     'car': driver.car,
                                     'time': driver.end-driver.start} for driver in leaderboard}
        leaderboard = dict(sorted(leaderboard.items(), key=lambda k: k[1]['time'], reverse=order[args['order']]))

        if args['format'].upper() == 'JSON':
            return output_json(leaderboard,
                               200,
                               {'content-type': 'application/json'})
        elif args['format'].upper() == 'XML':
            return output_xml(leaderboard,
                              200,
                              {'content-type': 'application/xml'})
        else:
            return abort(400, message='format parameter can be json or xml')


api.add_resource(Driverslist, '/drivers')
api.add_resource(Leaderboard, '/leaderboard')
api.add_resource(Driver, '/drivers/<driver_abbr>')

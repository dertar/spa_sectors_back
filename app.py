from flask import *
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, reqparse
import datetime

parser = reqparse.RequestParser()
parser.add_argument('data', type=object, help='data cannot be converted')
parser.add_argument('token', type=str, help='token cannot be converted')

app = Flask(__name__)
api = Api(app)
mongo = PyMongo(app, uri='mongodb://localhost:27017/sectors')

'''
{
    $id : {
    
    }
}
'''

class Sector(Resource):
    def get(self, id):
        ret =  mongo.db['sectors'].find_one({'id': id})
        del ret['_id']

        if request.args.get('token') == 'token':
            return ret

        return {'status': 'failed', 'error': str(request.args.get('token'))}, 201

    def put(self, id):
        args = parser.parse_args()
        if args['data']:
            old = mongo.db['sectors'].find_one({'id': id})

            if not old:
                return {'status': 'failed'}
            else:
                try: 
                    old.replace_one({'id': id}, args['data'])
                except Exception as e:
                    return {'status': 'failed', 'error': str(e)}, 201

        return {'status': 'ok'}
    
    def post(self, id):
        args = parser.parse_args()

        try: 
            if args.get('token') == 'token':
                mongo.db['sectors'].insert({'id' : id}, args['data']})
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}, 201
        return {'status': 'ok'}


api.add_resource(Sector, '/sector/int:id')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import BucketList

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        if request.method == 'POST':
            name = str(request.data.get('name', ''))
            if name:
                bucketlist = BucketList(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201

                return response
        else:
            bucketlists = BucketList.get_all()
            all_bucketlists = []
            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                all_bucketlists.append(obj)
                response = jsonify(all_bucketlists)
                response.status_code = 200
                return response

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_edit_item(id, **kwargs):
        bucketlist = BucketList.query.filter_by(id=id).first()
        if not bucketlist:
                # raise HTTP 404 response if id not found
            abort(404)
        if request.method == 'DELETE':
            bucketlist.delete()
            return{"message":
                   "bucketlist {} successfully deleted".format(bucketlist.id)}, 200
        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response
        else:
            # if method is GET return specified bucketlist
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

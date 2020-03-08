from app.api import bp
from flask import jsonify, request
from app.models import User
from flask import url_for
from app import db
from app.api.errors import bad_request, error_response

@bp.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def user(id):
    #""" Get a user. """    
    if request.method == 'GET':
        user = User.query.get(id)
        if user is None :
            return error_response(404)
        response = jsonify(user.to_dict())
        response.headers['Location'] = url_for('api.user', id=id)
        return response

    #""" Update user's details. """
    elif request.method == 'PUT':
        response = jsonify({"status": 'user details updated'})
        return response, 204

    #""" Delete a user. """
    elif request.method == 'DELETE':
        user = User.query.get(id)
        if user is None:
            return error_response(404)
        data = user.to_dict()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": 'user deleted'}), 204

    #""" POST method not allowed on this endpoint. """
    elif request.method == 'POST':
        return bad_request("You cannot create user on this end point. Use this for a POST request: "+ url_for('api.users')), 400

    else:
        return bad_request("That's a bad request."), 400


@bp.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    #""" Get All Users. """
    if request.method == 'GET':
        users = User.query.all()
        response = jsonify(
                        {'users': [user.to_dict() for user in users],
                        '_link': url_for('api.users')
                        }
            )
        response.headers['Location'] = url_for('api.users')
        return response

    #""" Create a user. """
    elif request.method == 'POST':
        data = request.get_json() or {}

        if 'username' not in data and 'email' not in data:
            return bad_request('Username and email was missing from the request.')
        if 'username' not in data:
            return bad_request('Username was missing from the request.')
        if 'email' not in data:
            return bad_request('Email was missing from the request.')
        if User.query.filter_by(username=data['username']).first():
            return bad_request('This username is already taken. Please use a different username.')
        if User.query.filter_by(email=data['email']).first():
            return bad_request('This email is already taken. Please use a different email.')

        user = User()
        user.from_dict(data)

        db.session.add(user)
        db.session.commit()
        response = jsonify(user.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.user', id=user.id)
        return response

    #""" PUT method not allowed on this endpoint. """
    elif request.method == 'PUT':
        return bad_request("You cannot update a user on this end point. Use this for a PUT request with an id: "+ url_for('api.user')+"/<id>"), 400

    #""" DELETE method not allowed on this endpoint. """
    elif request.method == 'DELETE':
        return bad_request("You cannot delete a user on this end point. Use this for a DELETE request with an id: "+ url_for('api.user')+"/<id>"), 400

    else:
        return bad_request("That's a bad request."), 400
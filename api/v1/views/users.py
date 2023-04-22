from models.user import User
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def get_users():
    """retrive list of all User objects"""
    if request.method == "GET":
        li_users = []
        my_users = storage.all(User)
        for obj in my_users.values():
            li_users.append(obj.to_dict())
        return jsonify(li_users)

    data_user = request.get_json()
    if not data_user:
        abort(400, "Not a JSON")
    if not data_user.get("email"):
        abort(400, "Missing email")
    if not data_user.get("password"):
        abort(400, "Missing password")
    new_user = User()
    for k, v in data_user.items():
        setattr(new_user, k, v)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_user_by_id(user_id=None):
    """retrive a specific User object matching with id"""
    my_user = storage.get(User, user_id)
    if not my_user:
        abort(404)
    if request.method == "GET":
        return jsonify(my_user.to_dict())
    if request.method == "DELETE":
        storage.delete(my_user)
        storage.save()
        return jsonify({}), 200

    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    for k, v in user_data.items():
        if k in ["id", "name", "created_at", "updated_at"]:
            continue
        setattr(my_user, k, v)
    storage.save()
    return jsonify(my_user.to_dict()), 200

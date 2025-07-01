from flask import Blueprint, jsonify

ping_blueprint = Blueprint("ping", __name__, url_prefix="/ping")


@ping_blueprint.route("/", methods=["GET"])
def ping():
    return jsonify({"message": "ping"}), 200

#!/usr/bin/python3
"""module named index"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/status", methods=["GET"])
def get_data():
    if request.method == "GET":
        res = jsonify({"status": "OK"})
    return res

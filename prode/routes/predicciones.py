from flask import Blueprint, jsonify, request
from prode.db import get_connection

prediccion_bp = Blueprint("predicciones", __name__)

# Endpoints Prediccion
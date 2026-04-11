from flask import Blueprint, jsonify, request
from app_backend.prode.db import get_connection

usuarios_bp = Blueprint("usuarios", __name__)

# Endpoints Usuarios
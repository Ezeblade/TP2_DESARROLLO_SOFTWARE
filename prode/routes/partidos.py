from flask import Blueprint, jsonify, request
from prode.db import get_connection
from prode.services import partidos as partidos_service
# EJEMPLO cuando usen validar o servicios 
#from app_backend.prode.validators.partidos import validar_listado_partidos
#from app_backend.prode.services.partidos import listar_partidos

partidos_bp = Blueprint("partidos", __name__)

# Endpoints Partidos

@partidos_bp.route("/")
def listar_partidos():
    partidos = partidos_service.listar_partidos()
    if not partidos:
        return "", 204
    return jsonify(partidos)

@partidos_bp.route("/<string:id>/resultado", methods=["PUT"])
def cargar_o_actualizar_resultado(id):
    if not id.isdigit() or int(id) < 1:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "El id del partido debe ser un entero positivo",
                "level": "error",
            }]
        }), 400

    id = int(id)
    data = request.get_json(silent=True) or {}
    goles_local = data.get("goles_local")
    goles_visitante = data.get("goles_visitante")

    try:
        gl = int(goles_local)
        gv = int(goles_visitante)

    except (TypeError, ValueError):
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "goles_local y goles_visitante deben ser enteros",
                "level": "error",
            }]
        }), 400

    if gl < 0 or gv < 0:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "Los goles no pueden ser negativos",
                "level": "error",
            }]
        }), 400
    try:
        ok = partidos_service.cargar_o_actualizar_resultado(id, gl, gv)
    except Exception as error:
        print(f"error inesperado al actualizar resultado: {error}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500
    if not ok:
        return jsonify({
            "errors": [{
                "code": "NOT_FOUND",
                "message": "Partido no encontrado",
                "level": "error",
            }]
        }), 404
    return "", 204 


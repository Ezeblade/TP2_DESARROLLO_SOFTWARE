from flask import Blueprint, jsonify, request

from prode.services import predicciones as predicciones_service
from prode.validators import partidos as partidos_validators

prediccion_bp = Blueprint("predicciones", __name__)


@prediccion_bp.route("/<string:id>/prediccion", methods=["POST"])
def registrar_prediccion_para_partido(id):
    error = partidos_validators.validar_id_entero_positivo(id)
    if error:
        return error
    id_partido = int(id)
    data = request.get_json(silent=True) or {}
    id_usuario = data.get("id_usuario")
    local = data.get("goles_local")
    visitante = data.get("goles_visitante")

    if id_usuario is None or local is None or visitante is None:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "id_usuario, goles_local y goles_visitante son obligatorios",
                "level": "error",
            }]
        }), 400

    try:
        id_u = int(id_usuario)
        gl = int(local)
        gv = int(visitante)
    except (TypeError, ValueError):
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "id_usuario, goles_local y goles_visitante deben ser enteros válidos",
                "level": "error",
            }]
        }), 400

    if id_u < 1:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "id_usuario debe ser un entero positivo",
                "level": "error",
            }]
        }), 400

    if gl < 0 or gv < 0:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "Los goles predichos no pueden ser negativos",
                "level": "error",
            }]
        }), 400

    try:
        resultado = predicciones_service.registrar_prediccion(id_partido, id_u, gl, gv)
    except Exception as error:
        print(f"error inesperado al registrar predicción: {str(error)}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500

    if resultado == "NOT_FOUND_PARTIDO":
        return jsonify({
            "errors": [{
                "code": "NOT_FOUND",
                "message": "partido no encontrado",
                "level": "error",
            }]
        }), 404
    if resultado == "NOT_FOUND_USUARIO":
        return jsonify({
            "errors": [{
                "code": "NOT_FOUND",
                "message": "usuario no encontrado",
                "level": "error",
            }]
        }), 404
    if resultado == "PARTIDO_JUGADO":
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "el partido ya tiene resultado cargado",
                "level": "error",
            }]
        }), 400
    if resultado == "DUPLICATE":
        return jsonify({
            "errors": [{
                "code": "CONFLICT",
                "message": "ya existe una predicción para este usuario y partido",
                "level": "error",
            }]
        }), 409

    return "", 201
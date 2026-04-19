import mysql.connector

from prode.db import get_connection


def registrar_prediccion(id_partido: int, id_usuario: int, goles_local: int, goles_visitante: int) -> str:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, goles_local, goles_visitante
            FROM partido
            WHERE id = %s
            """,
            (id_partido,),
        )
        partido = cursor.fetchone()
        if not partido:
            return "NOT_FOUND_PARTIDO"

        if partido["goles_local"] is not None or partido["goles_visitante"] is not None:
            return "PARTIDO_JUGADO"

        cursor.execute("SELECT id FROM usuario WHERE id = %s", (id_usuario,))
        if cursor.fetchone() is None:
            return "NOT_FOUND_USUARIO"

        cursor.execute(
            """
            INSERT INTO prediccion (id_usuario, id_partido, goles_local, goles_visitante)
            VALUES (%s, %s, %s, %s)
            """,
            (id_usuario, id_partido, goles_local, goles_visitante),
        )
        conn.commit()
        return "OK"
    except mysql.connector.errors.IntegrityError as exc:
        conn.rollback()
        if exc.errno == 1062:
            return "DUPLICATE"
        raise
    finally:
        cursor.close()
        conn.close()
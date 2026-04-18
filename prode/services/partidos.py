from prode.db import get_connection

def listar_partidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id,
               el.nombre AS equipo_local,
               ev.nombre AS equipo_visitante,
               p.fecha_partido AS fecha,
               p.fase_torneo AS fase
        FROM partido p
        JOIN equipo el ON p.id_equipo_local = el.id
        JOIN equipo ev ON p.id_equipo_visitante = ev.id
    """)
    partidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return partidos

def cargar_o_actualizar_resultado(id_partido, goles_local, goles_visitante):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE partido 
        SET goles_local = %s, goles_visitante = %s
        WHERE id = %s
        """, 
        (goles_local,goles_visitante,id_partido),
    )
    conn.commit()
    ok = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return ok
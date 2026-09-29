# Carga de datos de prueba tomadas de la foto que nos mandaron 

from werkzeug.security import generate_password_hash

from database import get_connection

PARAMETROS = [
    ("PH", "numerico", None),
    ("TDS", "numerico", "ppm"),
    ("Sabor", "binario", None),
    ("Olor", "binario", None),
    ("Color", "binario", None),
    ("Verificacion de Sello", "binario", None),
]

PUNTOS_MUESTREO = [
    ("Producto Final 5 Galones", "Registro operacional de producto final, presentacion 5 galones"),
    ("Cisterna de almacenamiento", "Tanque de almacenamiento previo a llenado"),
]

LIMITES_EJEMPLO = {
    "PH": (6.0, 6.5),
    "TDS": (0, 300),
    "Sabor": (1, 1),
    "Olor": (1, 1),
    "Color": (1, 1),
    "Verificacion de Sello": (1, 1),
}

# usuarios de prueba 
USUARIOS = [
    ("analista1", "analista123", "Ana Lista", "analista"),
    ("santos", "operador123", "Santos", "operador"),
    ("vargas", "operador123", "Vargas", "operador"),
    ("hernan", "operador123", "Hernan", "operador"),
]

# --- Lecturas reales, transcritas de la hoja fotografiada --------------------
# Formato: (fecha, hora, ph, tds, sabor, olor, color, sello, lote, observaciones, usuario_tecnico)
# sabor/olor/color/sello: 1 = cumple (marca de check en la hoja), 0 = no cumple
LECTURAS = [
    ("2026-09-08", "18:32", 6.20, 230, 1, 1, 1, 1, "25109-26", "", "santos"),
    ("2026-09-08", "20:33", 6.26, 231, 1, 1, 1, 1, "25109-26", "", "vargas"),
    ("2026-09-08", "22:34", 6.29, 231, 1, 1, 1, 1, "25109-26", "", "vargas"),
    ("2026-09-09", "00:34", 6.24, 230, 1, 1, 1, 1, "25207-26", "", "vargas"),
    ("2026-09-09", "02:33", 6.50, 222, 1, 1, 1, 1, "25207-26", "paro a 03:30", "vargas"),
    ("2026-09-09", "04:17", 6.30, 231, 0, 1, 1, 1, "25207-26", "inicio 04:15", "hernan"), 
    ("2026-09-09", "06:15", 6.21, 227, 1, 1, 1, 1, "25207-26", "paro 07:00", "hernan"), 
    ("2026-09-09", "07:37", 6.27, 241, 1, 1, 1, 1, "25207-26", "", "hernan"),
    ("2026-09-09", "09:36", 6.27, 239, 1, 1, 1, 1, "25207-26", "", "hernan"),
    ("2026-09-09", "11:32", 6.11, 231, 1, 1, 1, 1, "25207-26", "paro 12:00", "santos"),
    ("2026-09-09", "12:37", 6.14, 233, 1, 1, 1, 1, "25207-26", "R 12:35", "santos"),
    ("2026-09-09", "14:34", 6.18, 230, 1, 1, 1, 1, "25207-26", "", "santos"),
    ("2026-09-09", "16:32", 6.30, 232, 1, 1, 1, 1, "25207-26", "", "santos"),
    ("2026-09-09", "18:34", 6.14, 233, 1, 1, 1, 1, "25207-26", "", "santos"),
    ("2026-09-09", "20:33", 6.33, 232, 1, 1, 1, 1, "25207-26", "", "vargas"),
    ("2026-09-09", "22:34", 6.41, 232, 1, 1, 1, 1, "25207-26", "", "vargas"),
    ("2026-09-10", "00:33", 6.33, 222, 1, 1, 1, 1, "25309-26", "", "vargas"),
    ("2026-09-10", "02:34", 6.37, 327, 1, 1, 1, 1, "25309-26", "paro 03:30", "vargas"),
    ("2026-09-10", "04:11", 6.26, 243, 1, 1, 1, 1, "25309-26", "inicio 4:10", "hernan"),
    ("2026-09-10", "06:14", 6.21, 237, 1, 1, 1, 1, "25309-26", "paro 07:00", "hernan"),
    ("2026-09-10", "07:36", 6.31, 241, 1, 1, 1, 1, "25309-26", "R 07:05", "hernan")
]

def seed():
    conn = get_connection()
    cur = conn.cursor()
 
    for usuario, password, nombre, rol in USUARIOS:
        cur.execute(
            "INSERT INTO usuarios (usuario, password_hash, nombre_completo, rol) "
            "VALUES (%s, %s, %s, %s)",
            (usuario, generate_password_hash(password), nombre, rol),
        )
 
    for nombre, descripcion in PUNTOS_MUESTREO:
        cur.execute(
            "INSERT INTO puntos_muestreo (nombre, descripcion) VALUES (%s, %s)",
            (nombre, descripcion),
        )
 
    for nombre, tipo, unidad in PARAMETROS:
        cur.execute(
            "INSERT INTO parametros (nombre, tipo, unidad) VALUES (%s, %s, %s)",
            (nombre, tipo, unidad),
        )
 
    conn.commit()
 
    # --- volver a leer los ids que MySQL acaba de asignar (AUTO_INCREMENT) --
    cur.execute("SELECT id, nombre FROM parametros")
    parametro_ids = {row["nombre"]: row["id"] for row in cur.fetchall()}
 
    cur.execute("SELECT id, nombre FROM puntos_muestreo")
    puntos = cur.fetchall()
    punto_producto_final_id = next(p["id"] for p in puntos if p["nombre"] == "Producto Final 5 Galones")
    todos_los_puntos_ids = [p["id"] for p in puntos]
 
    cur.execute("SELECT id, usuario FROM usuarios")
    usuario_ids = {row["usuario"]: row["id"] for row in cur.fetchall()}
 
    # --- limites: mismos valores para todos los puntos de muestreo (ejemplo) --
    for nombre_param, (v_min, v_max) in LIMITES_EJEMPLO.items():
        for punto_id in todos_los_puntos_ids:
            cur.execute(
                "INSERT INTO limites (parametro_id, punto_muestreo_id, valor_min, valor_max) "
                "VALUES (%s, %s, %s, %s)",
                (parametro_ids[nombre_param], punto_id, v_min, v_max),
            )
 
    # --- lecturas reales + sus valores por parametro -------------------------
    for fecha, hora, ph, tds, sabor, olor, color, sello, lote, obs, tecnico_usuario in LECTURAS:
        tecnico_id = usuario_ids[tecnico_usuario]
        valores_por_parametro = {
            "PH": ph,
            "TDS": tds,
            "Sabor": sabor,
            "Olor": olor,
            "Color": color,
            "Verificacion de Sello": sello,
        }
 
        # validacion contra limites, igual que hara la ruta /lecturas/nueva
        lectura_dentro_de_rango = True
        resultados = []
        for nombre_param, valor in valores_por_parametro.items():
            v_min, v_max = LIMITES_EJEMPLO[nombre_param]
            dentro = v_min <= valor <= v_max
            if not dentro:
                lectura_dentro_de_rango = False
            resultados.append((parametro_ids[nombre_param], valor, dentro))
 
        cur.execute(
            "INSERT INTO lecturas "
            "(punto_muestreo_id, tecnico_id, fecha, hora, lote, observaciones, dentro_de_rango) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (punto_producto_final_id, tecnico_id, fecha, hora, lote, obs, int(lectura_dentro_de_rango)),
        )
        lectura_id = cur.lastrowid
 
        for parametro_id, valor, dentro in resultados:
            cur.execute(
                "INSERT INTO lectura_valores (lectura_id, parametro_id, valor, dentro_de_rango) "
                "VALUES (%s, %s, %s, %s)",
                (lectura_id, parametro_id, valor, int(dentro)),
            )
 
    conn.commit()
    conn.close()
 
    print("Datos de prueba cargados: usuarios, puntos de muestreo, parametros, limites y lecturas reales.")
    print(f"  - {len(LECTURAS)} lecturas insertadas (fuente: hoja de registro fisica).")
    print("Usuarios de prueba:")
    for usuario, password, _, rol in USUARIOS:
        print(f"  - {usuario} / {password}  ({rol})")
 
 
if __name__ == "__main__":
    seed()
 
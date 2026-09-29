from flask import Flask, render_template
from database import get_connection

app = Flask(__name__)

@app.route("/")
def index():
    return "Home"

@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute( 
    """
    SELECT 
        l.id, 
        l.fecha, 
        l.hora, 
        l.lote, 
        l.observaciones, 
        l.dentro_de_rango,
        pm.nombre AS punto_muestreo_nombre,
        u.nombre_completo AS tecnico_nombre,
        p.nombre AS parametro_nombre,
        lv.valor, 
        lv.dentro_de_rango AS valor_dentro_de_rango
    FROM lecturas l
    JOIN puntos_muestreo pm ON pm.id = l.punto_muestreo_id
    JOIN usuarios u ON u.id = l.tecnico_id
    LEFT JOIN lectura_valores lv ON lv.lectura_id = l.id
    LEFT JOIN parametros p ON p.id = lv.parametro_id;
    
    """
    )
    lecturas = cur.fetchall()  # una fila por (lectura, parametro)

    lecturas_agrupadas = {}

    for fila in lecturas:
        lectura_id = fila["id"]

        if lectura_id not in lecturas_agrupadas:
            lecturas_agrupadas[lectura_id] = {
                "id": fila["id"],
                "fecha": fila["fecha"],
                "hora": fila["hora"],
                "lote": fila["lote"],
                "punto_de_muestreo": fila["punto_muestreo_nombre"],
                "observaciones": fila["observaciones"],
                "tecnico": fila["tecnico_nombre"],
                "valores": [],
                "dentro_de_rango": fila["dentro_de_rango"]
            }

        lecturas_agrupadas[lectura_id]["valores"].append({
            "parametro": fila["parametro_nombre"],
            "valor": fila["valor"],
            "dentro_de_rango": fila["valor_dentro_de_rango"]
        })

    lista_lecturas = list(lecturas_agrupadas.values())

    return render_template("dashboard.html", lecturas=lista_lecturas)

if __name__ == "__main__":
    app.run(debug=True)
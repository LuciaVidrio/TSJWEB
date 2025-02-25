from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__)

# Cargar base de conocimiento desde el archivo JSON
with open("carreras.json", "r", encoding="utf-8") as file:
    base_conocimiento = json.load(file)

# Preguntas para el usuario
preguntas = [
    {"id": "interes", "pregunta": "¿Cuáles son tus áreas de interés?", "tipo": "texto"},
    {"id": "habilidades", "pregunta": "¿En qué habilidades destacas?", "tipo": "texto"},
    {"id": "conocimientos", "pregunta": "¿Qué conocimientos previos tienes?", "tipo": "texto"},
]

# Motor de inferencia
def inferir_carrera(respuestas_usuario):
    mejores_opciones = []
    respuestas_usuario = {key: respuestas_usuario[key].lower().strip() for key in respuestas_usuario}

    for carrera in base_conocimiento:
        coincidencias = 0
        razon = []

        carrera["areas_interes"] = [area.lower().strip() for area in carrera["areas_interes"]]
        carrera["habilidades"] = [habilidad.lower().strip() for habilidad in carrera["habilidades"]]
        carrera["conocimientos"] = [conocimiento.lower().strip() for conocimiento in carrera["conocimientos"]]

        if any(interes in carrera["areas_interes"] for interes in respuestas_usuario["interes"].split(",")):
            coincidencias += 1
            razon.append("Intereses coinciden")

        if any(habilidad in carrera["habilidades"] for habilidad in respuestas_usuario["habilidades"].split(",")):
            coincidencias += 1
            razon.append("Habilidades coinciden")

        if any(conocimiento in carrera["conocimientos"] for conocimiento in respuestas_usuario["conocimientos"].split(",")):
            coincidencias += 1
            razon.append("Conocimientos coinciden")

        if coincidencias > 0:
            mejores_opciones.append({
                "carrera": carrera["nombre"],
                "descripcion": carrera.get("descripcion", "Descripción no disponible"),  # 📌 Agrega descripción
                "razon": ", ".join(razon)
            })

    return mejores_opciones

@app.route("/")
def index():
    return render_template("index.html", preguntas=preguntas)

@app.route("/recomendar", methods=["POST"])
def recomendar():
    respuestas_usuario = request.json
    recomendaciones = inferir_carrera(respuestas_usuario)
    return jsonify(recomendaciones)

if __name__ == "__main__":
    app.run(debug=True)
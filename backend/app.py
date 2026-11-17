from flask import Flask, request, jsonify
from flask_cors import CORS
from orquestador import compilar_codigo

app = Flask(__name__)
CORS(app)  # Permite que el frontend se comunique con este servidor sin bloqueos

@app.route("/compilar", methods=["POST"])
def endpoint_compilar():
    datos = request.get_json()
    codigo = datos.get("codigo", "")
    resultado = compilar_codigo(codigo)
    return jsonify(resultado)

if __name__ == "__main__":
    print("Servidor del Compilador iniciado en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
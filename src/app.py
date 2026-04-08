# src/app.py
from flask import Flask, request, jsonify
from src.estadisticas import resumen_estadistico, detectar_outliers_iqr

app = Flask(__name__)


@app.route('/estadisticas', methods=['POST'])
def endpoint_estadisticas():
    contenido = request.get_json(silent=True)

    if (
        not contenido or
        'datos' not in contenido or
        not isinstance(contenido['datos'], list)
    ):
        return jsonify({"error":
                        "Se requiere una lista de 'datos' "
                        "en el cuerpo JSON."}), 400

    if len(contenido['datos']) == 0:
        return jsonify({"error": "La lista de datos está vacía."}), 400

    try:
        resultado = resumen_estadistico(contenido['datos'])
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/outliers', methods=['POST'])
def endpoint_outliers():
    contenido = request.get_json(silent=True)

    if (
        not contenido or
        'datos' not in contenido or
        not isinstance(contenido['datos'], list)
    ):
        return jsonify({"error": "Se requiere una lista de 'datos'."}), 400

    try:
        outliers = detectar_outliers_iqr(contenido['datos'])
        return jsonify({"outliers": outliers}), 200
    except Exception:
        return jsonify({"error": "Error al procesar los datos."}), 400


@app.route('/salud', methods=['GET'])
def health_check():
    return jsonify({"estado": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True)

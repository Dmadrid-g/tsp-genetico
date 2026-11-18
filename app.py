import os
from flask import Flask, jsonify, render_template, request
from ga import resolver

app = Flask(__name__)
MIN_CIUDADES, MAX_CIUDADES = 20, 50


@app.get("/")
def index():
    return render_template("index.html", minc=MIN_CIUDADES, maxc=MAX_CIUDADES)


@app.post("/api/resolver")
def api_resolver():
    d = request.get_json(force=True, silent=True) or {}
    try:
        nombres = [str(x) for x in d["nombres"]]
        m = [[float(v) for v in fila] for fila in d["matriz"]]
        n = len(m)
        if not (MIN_CIUDADES <= n <= MAX_CIUDADES):
            raise ValueError(f"El número de ciudades debe estar entre {MIN_CIUDADES} y {MAX_CIUDADES}.")
        if len(nombres) != n or any(len(f) != n for f in m):
            raise ValueError("La matriz debe ser cuadrada y coincidir con los nombres.")
        if any(v < 0 for f in m for v in f):
            raise ValueError("Los costos no pueden ser negativos.")
        p = d.get("params", {})
        res = resolver(
            m,
            pob=max(10, min(int(p.get("pob", 200)), 1000)),
            generaciones=max(10, min(int(p.get("generaciones", 500)), 3000)),
            p_mutacion=max(0.0, min(float(p.get("mutacion", 0.2)), 1.0)),
        )
    except (KeyError, ValueError, TypeError) as e:
        return jsonify(error=str(e)), 400
    res["nombres_ruta"] = [nombres[i] for i in res["ruta"]]
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

# TSP con Algoritmo Genético

Aplicación web (Flask + HTML) que resuelve el **problema del vendedor viajero** con un **algoritmo genético** para 20–50 ciudades.
El usuario ingresa la matriz de costos (distancias) en la interfaz y la app devuelve la ruta óptima encontrada.

## Algoritmo (`ga.py`)
- Representación: permutación de ciudades (ciclo cerrado).
- Selección: torneo. Cruce: Order Crossover (OX). Mutación: inversión/intercambio. Elitismo: 2 mejores.

## Ejecutar local
```bash
pip install -r requirements.txt
python app.py        # http://localhost:5000
```

## Desplegar (Render, gratis)
1. Sube el repo a GitHub.
2. En https://render.com → **New + → Blueprint** (o *Web Service*) y elige el repo.
3. Render lee `render.yaml`: build `pip install -r requirements.txt`, start `gunicorn app:app`.
4. El enlace público `https://<nombre>.onrender.com` es el que entregas.

## Integrantes
- Daniel Madrid Giraldo
- (pareja)

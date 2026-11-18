"""Algoritmo genético para el problema del vendedor viajero (TSP)."""
import random


def costo_ruta(ruta, m):
    """Costo total del ciclo cerrado (regresa a la ciudad de origen)."""
    n = len(ruta)
    return sum(m[ruta[i]][ruta[(i + 1) % n]] for i in range(n))


def cruce_ox(p1, p2, rng):
    """Order Crossover (OX): copia un tramo de p1 y completa con el orden de p2."""
    n = len(p1)
    a, b = sorted(rng.sample(range(n), 2))
    hijo = [None] * n
    hijo[a:b + 1] = p1[a:b + 1]
    usados = set(hijo[a:b + 1])
    resto = [c for c in p2 if c not in usados]
    k = 0
    for i in range(n):
        if hijo[i] is None:
            hijo[i] = resto[k]
            k += 1
    return hijo


def mutar(ruta, rng):
    """Mutación: inversión de un tramo o intercambio de dos ciudades."""
    n = len(ruta)
    i, j = sorted(rng.sample(range(n), 2))
    if rng.random() < 0.5:
        ruta[i:j + 1] = reversed(ruta[i:j + 1])
    else:
        ruta[i], ruta[j] = ruta[j], ruta[i]


def torneo(poblacion, costos, k, rng):
    candidatos = rng.sample(range(len(poblacion)), k)
    mejor = min(candidatos, key=lambda i: costos[i])
    return poblacion[mejor]


def resolver(m, pob=200, generaciones=500, p_cruce=0.9, p_mutacion=0.2,
             elite=2, k_torneo=5, semilla=None):
    """Devuelve la mejor ruta encontrada, su costo y el historial por generación."""
    rng = random.Random(semilla)
    n = len(m)
    base = list(range(n))
    poblacion = []
    for _ in range(pob):
        r = base[:]
        rng.shuffle(r)
        poblacion.append(r)

    historial = []
    mejor_ruta, mejor_costo = None, float("inf")

    for _ in range(generaciones):
        costos = [costo_ruta(r, m) for r in poblacion]
        orden = sorted(range(pob), key=lambda i: costos[i])
        if costos[orden[0]] < mejor_costo:
            mejor_costo = costos[orden[0]]
            mejor_ruta = poblacion[orden[0]][:]
        historial.append(mejor_costo)

        nueva = [poblacion[i][:] for i in orden[:elite]]  # elitismo
        while len(nueva) < pob:
            p1 = torneo(poblacion, costos, k_torneo, rng)
            p2 = torneo(poblacion, costos, k_torneo, rng)
            hijo = cruce_ox(p1, p2, rng) if rng.random() < p_cruce else p1[:]
            if rng.random() < p_mutacion:
                mutar(hijo, rng)
            nueva.append(hijo)
        poblacion = nueva

    # Rotar para que la ruta empiece en la ciudad 0 y cerrar el ciclo
    i0 = mejor_ruta.index(0)
    mejor_ruta = mejor_ruta[i0:] + mejor_ruta[:i0]
    return {"ruta": mejor_ruta, "costo": mejor_costo, "historial": historial}

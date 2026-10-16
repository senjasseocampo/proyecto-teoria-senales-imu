"""Genera señales IMU simuladas para arriba, abajo, izquierda y derecha."""

from pathlib import Path

import numpy as np
import pandas as pd


def crear_movimiento(movimiento, canal, signo, fs=50, duracion=10, semilla=7):
    rng = np.random.default_rng(semilla)
    n = int(fs * duracion)
    t = np.arange(n) / fs
    datos = rng.normal(0, 1.2, size=(n, 3))

    indice = {"x": 0, "y": 1, "z": 2}[canal]
    activo = (t >= 2) & (t <= 8)
    perfil = np.zeros(n)
    fase = (t[activo] - 2) / 6
    perfil[activo] = np.sin(np.pi * fase) ** 2

    datos[:, indice] += signo * 85 * perfil
    secundario = (indice + 1) % 3
    datos[:, secundario] += signo * 6 * perfil

    return pd.DataFrame({
        "tiempo_ms": (t * 1000).astype(int),
        "gx_dps": datos[:, 0],
        "gy_dps": datos[:, 1],
        "gz_dps": datos[:, 2],
        "estado": movimiento,
    })


def main():
    raiz = Path(__file__).resolve().parents[2]
    salida = raiz / "data" / "demo"
    salida.mkdir(parents=True, exist_ok=True)

    casos = [
        ("arriba", "x", 1),
        ("abajo", "x", -1),
        ("izquierda", "y", -1),
        ("derecha", "y", 1),
    ]

    for i, (movimiento, canal, signo) in enumerate(casos):
        archivo = salida / f"DEMO_{movimiento}.csv"
        crear_movimiento(movimiento, canal, signo, semilla=7 + i).to_csv(
            archivo, index=False
        )
        print(f"Generado: {archivo}")

    print("ADVERTENCIA: los datos son simulados y corresponden al segundo corte.")


if __name__ == "__main__":
    main()

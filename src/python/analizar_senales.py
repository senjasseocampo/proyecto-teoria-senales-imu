"""Analiza CSV del MPU6050: gráficas temporales, características, ventanas y FFT."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CANALES = ["gx_dps", "gy_dps", "gz_dps"]
COLORES = {"gx_dps": "#d62728", "gy_dps": "#2ca02c", "gz_dps": "#1f77b4"}


def argumentos():
    parser = argparse.ArgumentParser(description="Análisis inicial de señales MPU6050")
    parser.add_argument("--entrada", type=Path, required=True, help="Carpeta con archivos CSV")
    parser.add_argument("--salida", type=Path, required=True, help="Carpeta para resultados")
    parser.add_argument("--ventana", type=float, default=2.0, help="Ventana en segundos")
    return parser.parse_args()


def validar(df, archivo):
    requeridas = {"tiempo_ms", *CANALES}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"{archivo}: faltan columnas {sorted(faltantes)}")
    if len(df) < 3:
        raise ValueError(f"{archivo}: se requieren al menos tres muestras")


def parametros_tiempo(df):
    t = (df["tiempo_ms"].to_numpy(dtype=float) - float(df["tiempo_ms"].iloc[0])) / 1000
    dt = np.diff(t)
    dt = dt[dt > 0]
    ts = float(np.median(dt)) if len(dt) else np.nan
    fs = 1 / ts if ts > 0 else np.nan
    duracion = float(t[-1] - t[0])
    return t, fs, ts, duracion


def caracterizar(df, archivo, fs, duracion):
    filas = []
    estado = str(df["estado"].iloc[0]) if "estado" in df.columns else archivo.stem
    for canal in CANALES:
        x = df[canal].to_numpy(dtype=float)
        filas.append({
            "archivo": archivo.name,
            "estado": estado,
            "canal": canal,
            "muestras": len(x),
            "duracion_s": duracion,
            "fs_estimada_hz": fs,
            "min_dps": np.min(x),
            "max_dps": np.max(x),
            "media_dps": np.mean(x),
            "desv_est_dps": np.std(x, ddof=1),
            "pico_a_pico_dps": np.ptp(x),
            "abs_max_dps": np.max(np.abs(x)),
            "rms_dps": np.sqrt(np.mean(x**2)),
        })
    return filas


def grafica_temporal(df, t, archivo, salida):
    fig, ax = plt.subplots(figsize=(10, 5))
    for canal in CANALES:
        ax.plot(t, df[canal], label=canal.replace("_dps", ""), color=COLORES[canal], linewidth=1)
    ax.set_title(f"Velocidad angular - {archivo.stem}")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Velocidad angular (°/s)")
    ax.grid(alpha=0.3)
    ax.legend(title="Canal")
    fig.tight_layout()
    fig.savefig(salida / f"temporal_{archivo.stem}.png", dpi=180)
    plt.close(fig)


def grafica_fft(df, fs, archivo, salida):
    if not np.isfinite(fs):
        return
    fig, ax = plt.subplots(figsize=(10, 5))
    for canal in CANALES:
        x = df[canal].to_numpy(dtype=float)
        x = x - np.mean(x)
        ventana = np.hanning(len(x))
        espectro = np.abs(np.fft.rfft(x * ventana))
        frecuencias = np.fft.rfftfreq(len(x), d=1 / fs)
        if espectro.max() > 0:
            espectro = espectro / espectro.max()
        ax.plot(frecuencias, espectro, label=canal.replace("_dps", ""), color=COLORES[canal])
    ax.set_xlim(0, min(15, fs / 2))
    ax.set_title(f"Espectro normalizado - {archivo.stem}")
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Magnitud normalizada")
    ax.grid(alpha=0.3)
    ax.legend(title="Canal")
    fig.tight_layout()
    fig.savefig(salida / f"fft_{archivo.stem}.png", dpi=180)
    plt.close(fig)


def segmentar(df, fs, segundos):
    if not np.isfinite(fs):
        return pd.DataFrame()
    tamano = max(1, int(round(fs * segundos)))
    resultados = []
    for inicio in range(0, len(df) - tamano + 1, tamano):
        bloque = df.iloc[inicio:inicio + tamano]
        fila = {"inicio_muestra": inicio, "fin_muestra": inicio + tamano - 1}
        for canal in CANALES:
            x = bloque[canal].to_numpy(dtype=float)
            fila[f"{canal}_media"] = np.mean(x)
            fila[f"{canal}_std"] = np.std(x, ddof=1)
            fila[f"{canal}_rms"] = np.sqrt(np.mean(x**2))
            fila[f"{canal}_abs_max"] = np.max(np.abs(x))
        resultados.append(fila)
    return pd.DataFrame(resultados)


def main():
    args = argumentos()
    args.salida.mkdir(parents=True, exist_ok=True)
    archivos = sorted(args.entrada.glob("*.csv"))
    if not archivos:
        raise FileNotFoundError(f"No se encontraron CSV en {args.entrada}")

    caracteristicas = []
    for archivo in archivos:
        df = pd.read_csv(archivo)
        validar(df, archivo)
        t, fs, _, duracion = parametros_tiempo(df)
        caracteristicas.extend(caracterizar(df, archivo, fs, duracion))
        grafica_temporal(df, t, archivo, args.salida)
        grafica_fft(df, fs, archivo, args.salida)
        ventanas = segmentar(df, fs, args.ventana)
        ventanas.to_csv(args.salida / f"ventanas_{archivo.stem}.csv", index=False)

    resumen = pd.DataFrame(caracteristicas)
    resumen.to_csv(args.salida / "caracteristicas.csv", index=False)
    print(resumen.round(3).to_string(index=False))
    print(f"\nResultados guardados en: {args.salida.resolve()}")


if __name__ == "__main__":
    main()

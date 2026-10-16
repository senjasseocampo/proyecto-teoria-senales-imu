# Modelo de la señal simulada

La simulación representa tres canales de velocidad angular: `gx`, `gy` y `gz`, expresados en grados por segundo.

Para el canal principal se utiliza una señal suave con amplitud máxima cercana a 85 °/s. La amplitud aumenta y disminuye entre los segundos 2 y 8. El signo de `gx` diferencia arriba y abajo, mientras el signo de `gy` diferencia izquierda y derecha. En un canal secundario se agrega una variación pequeña para representar acoplamiento entre ejes.

Finalmente se añade ruido gaussiano independiente a los tres canales:

```text
n[k] ~ N(0, 1,2²)
```

Antes y después del movimiento, los canales contienen solamente ruido. La simulación no pretende sustituir el comportamiento exacto del MPU6050; se utiliza para validar el flujo de carga, representación, segmentación y caracterización antes de disponer del montaje físico.

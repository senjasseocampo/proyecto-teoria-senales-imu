# Análisis inicial de señales de giro  mediante IMU

**Asignatura:** Teoría de Señales  
**Proyecto:** 7 - Movimiento humano con IMU  
**Integrantes:** Cristian Camilo Marín García y Senjasse Ocampo Ocampo
**Link** https://github.com/senjasseocampo/proyecto-teoria-senales-imu

## 1. Descripción

El proyecto propone identificar cuatro movimientos direccionales de la mano: arriba, abajo, izquierda y derecha. El alcance se limita a estos cuatro movimientos. En el sistema final se utilizará un sensor MPU6050 y cada dirección se indicará mediante un LED diferente.

El propósito es construir una primera implementación reproducible para generar, representar y analizar señales multicanal semejantes a las que entregará el giroscopio. De esta forma se deja preparada la base de procesamiento para incorporar las mediciones reales y los LED en el tercer corte.

## 2. Objetivo

Generar computacionalmente señales de velocidad angular correspondientes a los movimientos de la mano hacia arriba, abajo, izquierda y derecha, documentar su muestreo, representarlas en el dominio temporal, segmentarlas en ventanas y comparar características iniciales.


## 3. Procedencia y modelo de las señales

Las señales utilizadas en esta entrega son **simuladas** y se generan con : src/python/generar_datos_demo.py. No corresponden todavía a mediciones físicas del MPU6050.

Cada archivo contiene:


tiempo_ms,gx_dps,gy_dps,gz_dps,estado


Las unidades de los tres canales son grados por segundo (`°/s`). Para simular un giro, el eje principal recibe una oscilación limitada por una envolvente temporal. Los demás ejes presentan variaciones pequeñas que representan acoplamiento entre ejes. A todos los canales se agrega ruido gaussiano de media cero y desviación estándar aproximada de `1,2 °/s`.

Los cuatro movimientos generados son:

Movimiento  Comportamiento esperado 

Arriba     `gx_dps` positivo 
Abajo      `gx_dps` negativo 
Izquierda  `gy_dps` negativo 
Derecha    `gy_dps` positivo 



## 4. Muestreo

La frecuencia de muestreo utilizada es `fs = 50 Hz`. Por tanto:


Ts = 1/fs = 1/50 = 0,02 s = 20 ms


Cada señal dura 10 segundos y contiene 500 muestras. La frecuencia de 50 Hz es suficiente para esta primera simulación de movimientos manuales.


## 5. Representación temporal e interpretación

El programa genera una gráfica por estado con los canales `gx`, `gy` y `gz` respecto al tiempo.

- En el movimiento hacia arriba, `gx` presenta valores positivos.
- En el movimiento hacia abajo, `gx` presenta valores negativos.
- En el movimiento hacia la izquierda, `gy` presenta valores negativos.
- En el movimiento hacia la derecha, `gy` presenta valores positivos.
- Entre aproximadamente 2 y 8 segundos se encuentra el movimiento simulado; antes y después la señal permanece cerca de cero.

En los movimientos verticales, el canal `gx` presenta la mayor variación; en los movimientos laterales domina `gy`. El signo permite diferenciar las direcciones opuestas. El canal `gz` conserva principalmente ruido y pequeñas variaciones secundarias.

## 6. Caracterización inicial

Para cada archivo y canal se calculan el número de muestras, duración, frecuencia de muestreo estimada, mínimo, máximo, media, desviación estándar, amplitud pico a pico, máximo absoluto y RMS.

La tabla se guarda en : results/demo/caracteristicas.csv. En el canal asociado con cada movimiento se esperan valores de RMS y máximo absoluto superiores a los observados en los otros canales. La media y el signo de la señal ayudan a diferenciar arriba de abajo e izquierda de derecha.


## 7. Ruido y degradación

La simulación incorpora ruido gaussiano de media cero y desviación estándar de `1,2 °/s`. Este ruido representa de manera simplificada fluctuaciones electrónicas y pequeñas vibraciones que podrían aparecer en el sensor real.

En la implementación física también pueden presentarse desviación de cero, variaciones en el intervalo de muestreo, movimientos involuntarios y giros simultáneos sobre varios ejes. Estos efectos se medirán durante el tercer corte.

## 8. Análisis frecuencial inicial

El programa calcula una FFT de cada canal después de retirar su valor medio y aplicar una ventana de Hann. El eje horizontal representa la frecuencia en hercios y el eje vertical la magnitud normalizada.

Esta visualización es exploratoria. Los movimientos simulados son lentos, por lo que la energía del canal principal se concentra en las bajas frecuencias. El espectro se interpreta como una descripción de la distribución de energía y no como una frecuencia única exacta.


## 9. Resultados actuales

La implementación genera cuatro archivos CSV de señales simuladas y consolida los resultados en un archivo general de características con 12 registros (results/demo/caracteristicas.csv), correspondientes a la evaluación independiente de los tres canales (g_x, g_y, g_z) para cada uno de los cuatro movimientos. Adicionalmente, se exportan las respectivas gráficas temporales y espectrales, así como el desglose de ventanas temporales. Los resultados permiten distinguir visual y numéricamente arriba, abajo, izquierda y derecha mediante el análisis del canal dominante y el signo de la señal. Con ello se cumple la evidencia mínima de disponer de señales IMU estructuradas, documentar los ejes y la frecuencia de muestreo, comparar más de dos movimientos y segmentar ventanas para obtener características temporales.


## 10 Prueba de Concepto en Tinkercad:https://www.tinkercad.com/things/09uKnNxbo6n-sensor-de-movimiento?sharecode=yr9WnxWgo57r_TvEsSH8rz5syVb3sUC91LICWIlytBA


Como propuesta inicial y soporte al desarrollo del proyecto, se diseñó un montaje preliminar en Tinkercad para validar la lógica básica de detección de movimiento mediante un sensor infrarrojo pasivo PIR y la activación de indicadores visualesLED.

Componentes Utilizados:

Arduino UNO
Sensor de Movimiento PIR (Conectado al pin digital 4)
Diodo LED e Indicador Visual (Conectado al pin digital 5)
Resistencia de Protección (330 Ω)
Protoboard y Cableado

Evidencia de funcionamiento:

Estado de Reposo (Sin Movimiento):Sensor PIR en estado de espera y LED apagado  
Detección de Movimiento (Simulación):Detección de presencia/movimiento y activación del LED.


## 11. Referencias

- InvenSense. (2013). *MPU-6000 and MPU-6050 Product Specification, Revision 3.4*. TDK InvenSense. https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf

- Ben-Sadoun, G., Michel, E., Annweiler, C., & Sacco, G. (2022).Human Fall Detection Using Passive Infrared Sensors with Low Resolution: A Systematic Review. Clinical Interventions in Aging, 17, 35–53. https://doi.org/10.2147/CIA.S329668

- Erman, Z. (2017). Kontrol Keseimbangan Dengan Menggunakan Sensor MPU 6050 Berbasis Arduino. http://eprints.polsri.ac.id/id/eprint/4653

- Romero, J. P., & Pérez, M. A. (2021). Caracterización de señales inerciales y estimación de movimiento mediante IMU. Universidad Politécnica de Madrid (TFG / Documento técnico)

- PrograMate. (2020, agosto 20). Sensor de Movimiento PIR en Arduino - Simulación en TINKERCAD

- ElectroLabEducativaEle ctrónica. (2025, septiembre 2). Transformada Rápida de Fourier (FFT): Espectro de Frecuencia, Ondas y Ruido Blanco. YouTube. https://youtu.be/MNUSVadSwgk
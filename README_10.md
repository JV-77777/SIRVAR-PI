# SIVAR-PI 0.10 · Cruces rápidos y arranque con cámara IP

Actualización para SIVAR-PI 0.9 en Raspberry Pi. El instalador respalda los archivos de código que reemplaza. Las cuentas, cámaras IP guardadas, zonas, evidencias y variables de configuración se conservan en la instalación existente.

## Instalar en la Raspberry

Descarga `SIVAR_PI_Ritmo_10.zip` en Windows. Si tu laptop ya llega a la Raspberry por la red, desde **CMD** copia el paquete con este comando:

```bat
scp "%USERPROFILE%\Downloads\SIVAR_PI_Ritmo_10.zip" calep@SIVAR-PI.local:/home/calep/
```

Desde la consola de la Raspberry, detén SIVAR con **Ctrl+C**. Con el ZIP en tu carpeta personal, ejecuta:

```bash
cd ~/sivar-pi
source .venv/bin/activate
python -m zipfile -e ~/SIVAR_PI_Ritmo_10.zip ~/sivar-pi-actualizacion-10
python ~/sivar-pi-actualizacion-10/instalar_actualizacion.py --destino ~/sivar-pi
python iniciar.py
```

Abre el sitio de SIVAR y recarga con **Ctrl+F5**. El pie de página debe mostrar `0.10.0`.

En **Cámaras**, pulsa **Usar esta cámara** para seleccionar `INGRESO HS` si aún figura seleccionada otra fuente. La fuente que queda seleccionada se recupera al reiniciar. SIVAR consulta las capacidades de video de la USB antes de abrirla. Si la USB seleccionada falta, el visor indica que está esperando y permite elegir la cámara IP.

## Probar INGRESO HS

1. Dibuja la zona sobre la trayectoria real de paso. Procura que una parte considerable del cuerpo pueda estar dentro durante el cruce. En la imagen original, el rectángulo estaba a la derecha. Si la trayectoria cruza por la puerta izquierda, mueve o amplía la zona hacia esa trayectoria.
2. Con la vigilancia pausada, entra en **Ajustes → Modo de análisis** y elige **Cruce rápido**.
3. Usa como punto de partida **35 %** para parte de la persona dentro, **5 %** para área visible en la zona y **1,5 %** para movimiento dentro de la zona. Guarda los ajustes. Los porcentajes se ajustan por separado del modo.
4. Activa la vigilancia y mantén la zona vacía mientras el estado del fondo cambia a **Preparado**.
5. Haz varias pasadas normales y rápidas. Deja más de tres segundos entre registros al probar el modo rápido. Comprueba en **Historial** cuántas pasadas produjeron una evidencia y si la cámara y la zona son las esperadas.

## Qué cambia en el análisis

| Parámetro | Equilibrado con valores iniciales | Cruce rápido |
|---|---:|---:|
| Intervalo mínimo entre comienzos | 1 s | 0,4 s |
| Descanso mínimo tras procesar una imagen | 0,6 s | 0,1 s |
| Confianza mínima del modelo | 65 % | 55 % |
| Confirmación | Dos muestras válidas entre las últimas tres | Una muestra válida |
| Separación mínima entre registros | 10 s | 3 s |
| Región que recibe el modelo | Fotograma completo | Zona con un margen alrededor |

Equilibrado toma sus tiempos y confianza de la configuración existente. El modo elegido y los tres porcentajes se guardan en Ajustes y aplican a la cámara que estés vigilando. Cada cámara conserva su propia zona.

El intervalo de 0,4 s es un mínimo, y el tiempo real también incluye la inferencia y su descanso. En **Equipo** puedes comparar **Análisis por segundo**, **Duración del último análisis**, temperatura y CPU. El detector toma una imagen reciente por análisis. Si una persona cruza entre dos muestras, queda fuera de la zona o aparece demasiado pequeña u oculta, puede faltar el registro. Dos personas que pasan dentro de los tres segundos de separación pueden quedar en una sola incidencia.

Una sola confirmación y una confianza más baja pueden producir más avisos erróneos. Si ocurre, ajusta los porcentajes y repite las pasadas, o vuelve a Equilibrado. Prueba también el lugar vacío con su iluminación habitual para comprobar el efecto de reflejos y sombras.

El visor reutiliza el JPEG producido por la captura RTSP. El detector sigue decodificando la imagen que analiza. Esta separación evita trabajo repetido en el video que se muestra continuamente.

## Leer el código comentado

| Archivo | Qué explica |
|---|---|
| `app/devices.py` | Cómo se distingue una webcam USB con captura de video de otros dispositivos V4L2. |
| `app/camera.py` | Cómo espera una USB y cómo publica el último JPEG de una cámara IP. |
| `app/camera_control.py` | Cómo recupera la fuente seleccionada al arrancar y guarda la zona de cada cámara. |
| `app/network_worker.py` y `app/network_capture.py` | Cómo se lee RTSP y se envía el JPEG junto con sus dimensiones. |
| `app/settings.py` | Los tiempos y la confirmación que usa cada modo. |
| `app/detection.py` | Cómo se recorta la imagen alrededor de la zona, se ejecuta MobileNet-SSD y se transforman los recuadros al fotograma completo. |
| `app/motion.py` | Cómo se comprueba el movimiento y se limita la frecuencia de registros. |
| `app/storage.py` | Cómo se recuperan los ajustes anteriores y se guarda el criterio que confirmó cada evento. |

El instalador muestra dónde guardó el respaldo. Si necesitas restaurar el código anterior, detén SIVAR y ejecuta `python ~/sivar-pi-actualizacion-10/instalar_actualizacion.py --restaurar RUTA_DEL_RESPALDO --destino ~/sivar-pi`, sustituyendo `RUTA_DEL_RESPALDO` por la ruta que apareció en la consola.

La verificación se realiza con pruebas locales y un flujo RTSP H.264 de prueba. La cadencia, la temperatura y la detección de personas en el lugar deben comprobarse con la Raspberry Pi y el canal de INGRESO HS.

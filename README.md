# SIVAR-PI 0.8.0 · Capturas, historial y correo manual

Actualización para la instalación 0.7.0. Conserva el diseño UAB y las condiciones
calibradas del detector. Añade captura temporal al abrir la comprobación manual,
gestión individual o múltiple del historial y correo revisado antes del envío.

## Instalar

Descarga `SIVAR_PI_Gestion_08.zip` a Descargas. Detén Python con Ctrl+C en la
consola SSH donde está ejecutándose la aplicación. En CMD de Windows:

```bat
scp "%USERPROFILE%\Downloads\SIVAR_PI_Gestion_08.zip" calep@SIVAR-PI.local:/home/calep/
```

En la consola SSH de la Raspberry:

```bash
python3 -m zipfile -e ~/SIVAR_PI_Gestion_08.zip ~/sivar-pi-actualizacion-08
python3 ~/sivar-pi-actualizacion-08/instalar_actualizacion.py --destino ~/sivar-pi
cd ~/sivar-pi
source .venv/bin/activate
python iniciar.py
```

Abre `http://sivar-pi.local:8080/` y recarga con Ctrl+F5. Debe aparecer 0.8.0.
No necesitas instalar dependencias nuevas. El envío SMTP utiliza la biblioteca
estándar de Python.

El instalador respalda código y recursos. Conserva `.env`, `.venv`, `data`, `logs`
y modelos existentes. La migración de SQLite añade columnas y tablas, sin borrar
incidencias anteriores. La vigilancia comienza pausada al iniciar, como antes.

## Captura de prueba: elegir la imagen antes de escribir

1. Pulsa **Captura de prueba** en Vigilancia.
2. El servidor conserva el JPEG reciente de ese momento y muestra una vista
   previa congelada con fecha, hora, cámara y zona originales.
3. Escribe una nota si lo necesitas. El video general puede seguir cambiando.
4. Pulsa **Guardar captura** para crear definitivamente el registro y la foto.

**Cancelar**, cerrar la ventana o Esc descartan la captura temporal. No se crea
un registro ni se guarda una fotografía en disco antes de confirmar. **Volver a
capturar** reemplaza la imagen temporal de manera explícita.

La captura temporal dura hasta 20 minutos, permanece en memoria y se pierde si
reinicias el proceso. Si caduca, toma otra. El límite evita acumular imágenes de
ventanas abandonadas. La hora mostrada es la del JPEG del servidor; puede diferir
ligeramente del clic por la cadencia de la cámara y la latencia de la red.

Si otra persona cambia la cámara mientras completas la nota, una captura ya
preparada conserva su cámara y zona originales. La foto final se rotula con su
hora de captura. La fecha del registro corresponde a la confirmación; en **Ver
foto**, el correo y el CSV se pueden consultar ambas horas.

Repetir la confirmación del mismo borrador tras un corte de conexión recupera el
mismo evento y evita duplicarlo.

## Historial y papelera

- **Borrar** en una fila abre la revisión del registro antes de moverlo a la papelera.
- Las casillas permiten seleccionar varios registros. La casilla del encabezado
  selecciona la página visible; la selección puede incluir otras páginas, hasta
  200 registros por operación. El contador muestra cuántos se han seleccionado.
- **Limpiar selección** desmarca los registros.
- **Papelera** muestra los registros retirados. Puedes **Restaurar** uno o varios.
- **Eliminar definitivamente** confirma la eliminación del registro y de su
  fotografía. Esta segunda acción libera espacio y no tiene restauración.

Mover a la papelera conserva los archivos para permitir recuperarlos. No hay
borrado permanente programado: el usuario decide cuándo eliminarlos. Los eventos
en la papelera no se incluyen en el historial activo, reportes o correos nuevos.
Si una fotografía no puede borrarse por un problema de escritura, su limpieza
queda pendiente y se reintenta al reiniciar; la interfaz informa de esa condición.

Una revisión de borrado caduca o se invalida si otro cliente cambia el historial.
La selección se vuelve a comprobar al confirmar. Los IDs no se reutilizan.

Un reporte generado antes de borrar o restaurar registros queda pendiente de
actualización. Pulsa **Generar reporte** otra vez para exportar los datos actuales.
Los archivos descargados previamente son copias que conservas fuera del sistema.

## Correo manual

Puedes iniciar un correo desde:

- **Correo** en una fila de Historial.
- **Enviar correo** con uno o varios eventos seleccionados.
- **Enviar por correo** al consultar una fotografía.
- **Enviar reporte por correo** en un reporte ya generado.

El flujo es **destinatarios → asunto y texto adicional → Revisar correo → Enviar
correo**. La vista previa muestra destinatarios, contenido y archivos. Si editas
el mensaje, debes revisarlo nuevamente antes de enviarlo.

Los detalles se incluyen en el cuerpo del mensaje: ID, tipo, fecha de registro,
hora de captura, cámara, zona, descripción y enlace a la evidencia. También se
adjuntan un reporte HTML y un CSV con todos los registros de la selección o del
reporte, incluidas sus distintas páginas.

Las fotografías son opcionales. Se admiten hasta 5 destinatarios, 200 eventos
seleccionados o 500 registros de un reporte, hasta 10 fotos y 8 MiB por correo.
Reduce el rango o desmarca las fotografías si superas esos límites. Los enlaces
a fotos requieren acceso al SIVAR-PI; los adjuntos permiten recibir una copia.

**Descargar borrador .eml** conserva el mensaje preparado con sus adjuntos para
abrirlo en un cliente compatible. Descargarlo no envía nada. Algunos clientes
abren EML como mensaje recibido y requieren copiarlo a un correo nuevo para
editar o enviar.

El sistema solo contacta al servidor SMTP cuando se pulsa **Enviar correo**.
No envía alertas ni reportes automáticamente. Si el servidor acepta el mensaje,
la interfaz informa de esa aceptación; la recepción final depende del servicio
de correo y de sus filtros. Si solo acepta algunos destinatarios, se muestra
cuáles aceptó y cuáles rechazó.

Si se corta la conexión durante el envío, utiliza **Consultar estado**. No se
reenvía automáticamente: un corte puede ocurrir después de que el servidor haya
aceptado el mensaje. Se conserva un estado del intento para evitar repetir ese
mismo envío al pulsar otra vez. Reiniciar durante un envío puede dejarlo pendiente
de confirmación; comprueba el destinatario o el servicio antes de preparar otro.

Un borrador de correo dura 15 minutos. Si los registros se borran, restauran o
cambian mientras lo revisas, vuelve a prepararlo. El archivo EML también se valida
contra el estado actual del historial antes de descargarlo.

## Configurar el envío SMTP

La aplicación permite preparar y descargar borradores sin credenciales. Para
habilitar **Enviar correo** necesitas una cuenta SMTP del proveedor que uses.
Los datos se guardan en `.env` de la Raspberry, no en los campos del navegador.

1. Detén Python con Ctrl+C.
2. Abre el archivo existente:

```bash
nano ~/sivar-pi/.env
```

3. Añade los campos SMTP. Para una cuenta Gmail que admita contraseñas de aplicación:

```dotenv
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURITY=starttls
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=
```

Completa `SMTP_USER` con tu dirección completa, `SMTP_FROM` con el remitente
permitido por tu proveedor y `SMTP_PASSWORD` con la contraseña de aplicación.
En Gmail, crea esa clave desde tu cuenta con verificación en dos pasos habilitada,
si la opción está disponible. No uses la contraseña normal de Gmail. Las cuentas
institucionales pueden requerir configuración o autorización de su administrador.

Para otro proveedor, usa su host, puerto y credenciales. Se admiten `starttls`
y `ssl`; el modo `ssl` suele utilizar 465. El sistema exige una conexión cifrada.

4. En nano guarda con Ctrl+O, Enter y sal con Ctrl+X.
5. Reinicia la aplicación:

```bash
cd ~/sivar-pi
source .venv/bin/activate
python iniciar.py
```

Al abrir el correo, la interfaz indica si faltan campos o si el envío está
configurado. Una configuración completa no garantiza que el proveedor acepte
las credenciales; eso se comprueba al realizar un envío manual. La contraseña no
se devuelve al navegador ni se incluye en el borrador descargable.

Documentación del proveedor:

- Puertos y cifrado Gmail: https://developers.google.com/workspace/gmail/imap/imap-smtp
- Contraseñas de aplicación: https://support.google.com/accounts/answer/185833

## Ventilación del equipo

Las capturas compartidas mostraron 75,2 °C con tapa y 70,9 °C sin tapa, con CPU de
23,6% y 19,8% respectivamente. La disminución coincide con quitar la tapa, aunque
la carga y el tiempo también variaron; no es una medición aislada de la carcasa.

Para usar la Pi 3B encerrada de manera continua, conviene proporcionar entrada y
salida de aire y un ventilador compatible que mueva aire sobre los disipadores.
La documentación de Raspberry Pi indica reducción progresiva de frecuencia entre
80 y 85 °C. No se modifican los límites térmicos ni la frecuencia de análisis en
esta actualización.

Referencia: https://www.raspberrypi.com/documentation/computers/config_txt.html

## Mantener y volver atrás

El motor, filtros, descanso de análisis, captura compartida, selección de cámara
y valores calibrados se conservan. Los reportes y el visor en pantalla completa
siguen disponibles. Los avisos intermitentes de la webcam anteriores siguen
pendientes de diagnóstico.

Para restaurar código anterior, detén la aplicación y usa la ruta del respaldo
que imprimió el instalador:

```bash
python3 ~/sivar-pi-actualizacion-08/instalar_actualizacion.py --restaurar RUTA_DEL_RESPALDO --destino ~/sivar-pi
```

El respaldo restaura código, no recupera registros eliminados definitivamente.
La versión 0.7 no interpreta la papelera: al volver a ella puede mostrar registros
movidos a la papelera de 0.8. Mantén la cámara que corresponda a su configuración.

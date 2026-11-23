# Validación de SIVAR-PI 0.8.0

## Pruebas locales

87 pruebas satisfactorias con pytest, incluidas las 69 existentes. Se verificó:

- La captura temporal no escribe evidencias ni eventos; conserva los píxeles
  aunque la cámara cambie después. Acepta confirmación posterior a cinco segundos,
  mantiene cámara y zona originales, permite cancelar y caduca sin guardar.
- Confirmaciones repetidas recuperan el mismo evento y no duplican fotografías.
- Borrado individual o múltiple a papelera, restauración y eliminación definitiva.
  Las fotos solo se eliminan en esta última acción. Los fallos de limpieza quedan
  en una cola y se reintentan sin volver a borrar registros.
- Cambios concurrentes invalidan revisiones del historial y reportes congelados.
  Los IDs siguen creciendo aunque se elimine el mayor registro.
- El correo preparado contiene notas, metadatos, detalle completo y fotos opcionales;
  preparar, descargar y cancelar no llaman al transporte SMTP.
- El envío repetido o concurrente del mismo borrador no duplica el intento.
  Un resultado incierto no activa reintentos automáticos. La aceptación parcial
  informa de destinatarios aceptados y rechazados.
- TLS antes de autenticar, modo SSL, errores de credenciales sin revelar la clave,
  rechazo de inyección de encabezados y bloqueo de envío de eventos retirados.
- Reportes de correo con más de una página conservan todos sus registros.
- Se mantienen las pruebas del motor, modelo, almacenamiento, cámaras, reportes,
  instalación, respaldo y restauración.

## Navegador

Flask real, SQLite temporal, cámara y servidor de correo simulados, Chromium:

- Captura congelada comprobada tras 6,1 s y un cambio visible de la imagen en vivo.
  La fotografía guardada conserva los píxeles de la captura inicial.
- Cancelación sin registro, repetición explícita de captura y guardado desde
  pantalla completa.
- Revisión de correo, descarga EML, cancelación sin envío y un envío simulado;
  consultar estado no vuelve a enviar.
- Selección múltiple, cancelación del borrado, papelera, restauración y borrado
  definitivo con comprobación física de la eliminación de la foto temporal.
- Invalida el reporte anterior y vuelve a calcular totales tras borrar incidencias.
- Correo de un reporte completo con más de 20 registros y adjuntos de reporte.
- Recorridos en 1440, 1280, 768, 390 y 320 píxeles; sin desbordamiento del documento.
  Las tablas mantienen desplazamiento propio. Revisión visual de escritorio y móvil.
- Cero errores de JavaScript y cero fallos HTTP inesperados. Se comprueba también
  la caducidad HTTP 410 de un borrador y la conservación del texto al editarlo.

Las imágenes y mediciones usadas en el navegador son simuladas. No se enviaron
correos reales ni se borraron datos de la Raspberry del usuario.

## Comprobar en la Raspberry

1. Confirma 0.8.0 y que zona, sensibilidad, eventos y fotos anteriores permanecen.
2. Toma una captura de prueba, cambia de posición, escribe una nota y guarda.
   Comprueba que la imagen corresponde al clic inicial.
3. Usa un registro de prueba para moverlo a papelera, restaurarlo y, si ya no lo
   necesitas, eliminarlo definitivamente.
4. Configura SMTP en `.env`, reinicia y revisa un correo dirigido a tu propia cuenta.
   Confirma manualmente y comprueba el mensaje y sus adjuntos.
5. Compara temperatura y FPS durante una sesión con la ventilación que vayas a usar.

El envío mediante un proveedor real y el rendimiento térmico del hardware quedan
pendientes de esa comprobación. La lógica del detector y sus parámetros no se han
modificado.

## Suite opcional

```bash
python -m pytest -q
```

La aplicación no necesita pytest ni Playwright para ejecutarse en la Raspberry.

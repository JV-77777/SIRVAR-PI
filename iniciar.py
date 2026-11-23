"""Arranque manual, un proceso y una sola captura de cámara."""
from logging.handlers import RotatingFileHandler
import logging
import signal
import cv2
from werkzeug.serving import make_server
from app import create_app
from app.camera import Camera
from app.settings import ROOT, Settings


def main():
    for name in ("logs", "data/evidencias"):
        (ROOT / name).mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(ROOT / "logs/aplicacion.log", maxBytes=1_000_000, backupCount=2, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logging.basicConfig(level=logging.INFO, handlers=[handler, logging.StreamHandler()])
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    settings = Settings.from_env()
    cv2.setNumThreads(1)
    camera = Camera(settings)
    application = create_app(settings, camera)
    detector = application.extensions["sivar_detector"]
    # Abrir el puerto antes de iniciar la cámara: si está ocupado, fallar limpiamente.
    server = make_server(settings.host, settings.port, application, threaded=True)

    def shutdown(_signum, _frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, shutdown)
    camera.start()
    detector.start()
    print(f"SIVAR-PI · http://SIVAR-PI.local:{settings.port}/ · Ctrl+C para detener", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo SIVAR-PI…", flush=True)
    finally:
        server.server_close()
        detector.stop()
        camera.stop()


if __name__ == "__main__":
    main()

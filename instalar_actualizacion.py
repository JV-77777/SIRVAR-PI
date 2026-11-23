"""Actualiza el código con respaldo; conserva .env, .venv, data y logs."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import shutil
import tempfile

FILES = (
    "app/__init__.py",
    "app/settings.py",
    "app/devices.py",
    "app/camera.py",
    "app/camera_control.py",
    "app/detection.py",
    "app/motion.py",
    "app/storage.py",
    "app/network_capture.py",
    "app/network_worker.py",
    "app/templates/index.html",
    "app/static/app.js",
    "app/static/style.css",
    "instalar_actualizacion.py",
    "README_10.md",
)


def checked_target(destination, name):
    if name not in FILES:
        raise ValueError("El respaldo contiene un archivo no permitido")
    path = destination / name
    if not path.resolve().is_relative_to(destination):
        raise ValueError("Un enlace sale de la carpeta del proyecto: " + name)
    if path.exists() and not path.is_file():
        raise ValueError("Se esperaba un archivo: " + name)
    return path


def restore(backup, destination):
    backup, destination = Path(backup).resolve(), Path(destination).resolve()
    manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
    if manifest["destination"] != str(destination):
        raise ValueError("El respaldo pertenece a otra carpeta de proyecto")
    targets = {name: checked_target(destination, name) for name in manifest["files"]}
    for name, existed in manifest["files"].items():
        original = backup / "archivos" / name
        if existed and not original.is_file():
            raise ValueError("Falta un archivo del respaldo: " + name)
    for name, existed in manifest["files"].items():
        target = targets[name]
        if existed:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup / "archivos" / name, target)
        else:
            target.unlink(missing_ok=True)


def install(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if source == destination:
        raise ValueError("Extrae la actualización en una carpeta distinta del proyecto")
    if not (destination / "iniciar.py").is_file() or not (destination / "app").is_dir():
        raise ValueError("No se encontró la aplicación existente en " + str(destination))
    # Este paquete actualiza una instalación que ya cuenta con el soporte IP y las cuentas de 0.9.
    for name in ("app/network_routes.py", "app/auth.py"):
        if not (destination / name).is_file():
            raise ValueError("Primero instala SIVAR-PI 0.9 de Raspberry. Falta " + name)
    for name in ("deploy.prototxt", "mobilenet_iter_73000.caffemodel"):
        if not (destination / "models" / name).is_file():
            raise ValueError("Esta actualización requiere el modelo de 0.3.0 ya instalado: falta " + name)
    targets = {name: checked_target(destination, name) for name in FILES}
    for name in FILES:
        if not (source / name).is_file():
            raise ValueError("Paquete incompleto: falta " + name)
    backup = Path(tempfile.mkdtemp(
        prefix="sivar-pi-respaldo-" + datetime.now().strftime("%Y%m%d-%H%M%S-") ,
        dir=destination.parent))
    manifest = {"destination": str(destination), "files": {name: path.exists() for name, path in targets.items()}}
    for name, existed in manifest["files"].items():
        if existed:
            original = backup / "archivos" / name
            original.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(targets[name], original)
    (backup / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    try:
        for name, target in targets.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, target)
    except Exception:
        restore(backup, destination)
        raise
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destino", type=Path, default=Path.home() / "sivar-pi")
    parser.add_argument("--restaurar", type=Path)
    args = parser.parse_args()
    try:
        if args.restaurar:
            restore(args.restaurar, args.destino)
            print("Código anterior restaurado. .env, .venv, data y logs se conservan.")
        else:
            try:
                from cryptography.fernet import Fernet
            except ImportError:
                raise ValueError("Falta python3-cryptography. Instálalo con: sudo apt install python3-cryptography") from None
            backup = install(Path(__file__).parent, args.destino)
            print("Actualización 0.10.0 instalada. Respaldo del código:", backup)
            print("Se conservan .env, .venv, data y logs. Ya puedes iniciar la aplicación.")
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, "No se pudo completar la operación: " + str(error) + "\n")


if __name__ == "__main__":
    main()

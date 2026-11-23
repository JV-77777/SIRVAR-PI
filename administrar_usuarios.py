"""Crear el primer administrador o recuperar una contraseña desde la Raspberry."""
import argparse
from getpass import getpass
from app.auth import AuthStore
from app.settings import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('accion', choices=['crear-admin', 'restablecer'])
    args = parser.parse_args()
    auth = AuthStore(ROOT / 'data')
    try:
        if args.accion == 'crear-admin' and auth.has_users():
            raise ValueError('Ya existen cuentas. Usa Usuarios desde la plataforma o restablecer para recuperar el acceso')
        username = input('Usuario (por ejemplo calep): ').strip()
        name = input('Nombre para mostrar: ').strip() if args.accion=='crear-admin' else None
        password = getpass('Contraseña (mínimo 10 caracteres; no se muestra al escribir): ')
        if password != getpass('Repite la contraseña: '):
            raise ValueError('Las contraseñas no coinciden')
        if args.accion=='crear-admin':
            auth.save(dict(username=username,name=name,role='admin',password=password),bootstrap=True)
        else:
            auth.reset_password(username,password)
        print('Cuenta preparada. Ingresa desde la página de SIVAR-PI.')
    except (ValueError,EOFError,KeyboardInterrupt) as error:
        parser.exit(1, str(error)+'\n')


if __name__=='__main__':
    main()

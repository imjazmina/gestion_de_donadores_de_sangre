from functools import wraps
from flask import session, redirect, url_for, request

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        # Usuario no logueado → verificar si expiró
        if "usuario_id" not in session:
            expired = request.cookies.get('session') is not None
            return redirect(url_for('donaciones_web.login', expired=int(expired)))

        # Usuario logueado → continuar
        return f(*args, **kwargs)

    return wrapper

def rol_required(rol):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "usuario_id" not in session:
                return redirect('/login')

            # si el rol no coincide → redirige
            if session.get("rol") != rol:
                return redirect('/login')

            return f(*args, **kwargs)
        return wrapper
    return decorator

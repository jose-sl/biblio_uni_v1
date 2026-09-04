from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from database import get_connection

from routes.dashboard import dashboard_bp
from routes.usuarios import usuarios_bp
from routes.categorias import categorias_bp
from routes.autores import autores_bp
from routes.libros import libros_bp
from routes.prestamos import prestamos_bp
from routes.devoluciones import devoluciones_bp
from routes.multas import multas_bp

app = Flask(__name__)

app.secret_key = "biblioteca_2026"

BASE_PATH = "/biblioteca"

# ==========================
# BLUEPRINTS
# ==========================

app.register_blueprint(
    dashboard_bp,
    url_prefix=BASE_PATH
)

app.register_blueprint(
    usuarios_bp,
    url_prefix=BASE_PATH
)

app.register_blueprint(
    categorias_bp,
    url_prefix=BASE_PATH
)

app.register_blueprint(
    autores_bp,
    url_prefix=BASE_PATH
)

app.register_blueprint(
    libros_bp,
    url_prefix=BASE_PATH
)

app.register_blueprint(
    prestamos_bp,
    url_prefix=BASE_PATH
)

app.register_blueprint(
    devoluciones_bp,
    url_prefix=BASE_PATH
)

app.register_blueprint(
    multas_bp,
    url_prefix=BASE_PATH
)

# ==========================
# LOGIN
# ==========================

@app.route(
    f"{BASE_PATH}/",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                nombre,
                usuario,
                rol,
                estado
            FROM usuarios
            WHERE usuario=%s
            AND password=%s
            AND estado='Activo'
        """, (
            usuario,
            password
        ))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            session["usuario_id"] = user["id"]
            session["nombre"] = user["nombre"]
            session["usuario"] = user["usuario"]
            session["rol"] = user["rol"]

            return redirect(
                url_for("dashboard.inicio")
            )

        flash(
            "Usuario o contraseña incorrectos",
            "danger"
        )

    return render_template(
        "login.html"
    )

# ==========================
# LOGOUT
# ==========================

@app.route(
    f"{BASE_PATH}/logout"
)
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )

# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5100,
        debug=True
    )
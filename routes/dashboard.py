from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from database import get_connection

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
def inicio():

    if "usuario_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # =====================================
    # TOTAL LIBROS
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) total
        FROM libros
    """)

    total_libros = cursor.fetchone()["total"]

    # =====================================
    # TOTAL USUARIOS
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) total
        FROM usuarios
    """)

    total_usuarios = cursor.fetchone()["total"]

    # =====================================
    # PRÉSTAMOS ACTIVOS
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) total
        FROM prestamos
        WHERE estado='Prestado'
    """)

    prestamos_activos = cursor.fetchone()["total"]

    # =====================================
    # DEVOLUCIONES
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) total
        FROM devoluciones
    """)

    total_devoluciones = cursor.fetchone()["total"]

    # =====================================
    # MULTAS PENDIENTES
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) total
        FROM multas
        WHERE estado='Pendiente'
    """)

    multas_pendientes = cursor.fetchone()["total"]

    # =====================================
    # ÚLTIMOS PRÉSTAMOS
    # =====================================

    cursor.execute("""
        SELECT
            p.id_prestamo,
            l.titulo,
            u.nombre,
            p.fecha_prestamo,
            p.fecha_limite,
            p.estado

        FROM prestamos p

        INNER JOIN usuarios u
            ON p.id_usuario = u.id

        INNER JOIN libros l
            ON p.id_libro = l.id

        ORDER BY p.fecha_prestamo DESC

        LIMIT 10
    """)

    prestamos_recientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",

        nombre=session["nombre"],
        rol=session["rol"],

        total_libros=total_libros,
        total_usuarios=total_usuarios,
        prestamos_activos=prestamos_activos,
        total_devoluciones=total_devoluciones,
        multas_pendientes=multas_pendientes,

        prestamos_recientes=prestamos_recientes
    )
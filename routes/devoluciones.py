from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

devoluciones_bp = Blueprint(
    "devoluciones",
    __name__
)


@devoluciones_bp.route("/devoluciones")
def listar_devoluciones():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            d.id_devolucion,
            d.fecha_devolucion,
            d.observaciones,
            p.id_prestamo,
            l.titulo,
            u.nombre
        FROM devoluciones d
        INNER JOIN prestamos p
            ON d.id_prestamo = p.id_prestamo
        INNER JOIN libros l
            ON p.id_libro = l.id
        INNER JOIN usuarios u
            ON p.id_usuario = u.id
        ORDER BY d.fecha_devolucion DESC
    """)

    devoluciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "devoluciones.html",
        devoluciones=devoluciones
    )


@devoluciones_bp.route(
    "/devoluciones/agregar",
    methods=["GET", "POST"]
)
def agregar_devolucion():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        id_prestamo = request.form["id_prestamo"]
        observaciones = request.form["observaciones"]

        cursor.execute("""
            INSERT INTO devoluciones
            (
                fecha_devolucion,
                observaciones,
                id_prestamo
            )
            VALUES
            (
                NOW(),
                %s,
                %s
            )
        """, (
            observaciones,
            id_prestamo
        ))

        cursor.execute("""
            SELECT id_libro
            FROM prestamos
            WHERE id_prestamo=%s
        """, (id_prestamo,))

        prestamo = cursor.fetchone()

        cursor.execute("""
            UPDATE prestamos
            SET estado='Devuelto'
            WHERE id_prestamo=%s
        """, (id_prestamo,))

        cursor.execute("""
            UPDATE libros
            SET ejemplares_disponibles =
                ejemplares_disponibles + 1
            WHERE id=%s
        """, (
            prestamo["id_libro"],
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("devoluciones.listar_devoluciones")
        )

    cursor.execute("""
        SELECT
            p.id_prestamo,
            l.titulo,
            u.nombre
        FROM prestamos p
        INNER JOIN libros l
            ON p.id_libro=l.id
        INNER JOIN usuarios u
            ON p.id_usuario=u.id
        WHERE p.estado='Prestado'
        ORDER BY p.id_prestamo DESC
    """)

    prestamos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "devoluciones_agregar.html",
        prestamos=prestamos
    )
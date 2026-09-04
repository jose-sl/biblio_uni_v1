from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

multas_bp = Blueprint(
    "multas",
    __name__
)


@multas_bp.route("/multas")
def listar_multas():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.id_multa,
            m.descripcion,
            m.monto,
            m.fecha_registro,
            m.estado,

            u.nombre,

            l.titulo

        FROM multas m

        INNER JOIN prestamos p
            ON m.id_prestamo = p.id_prestamo

        INNER JOIN usuarios u
            ON p.id_usuario = u.id

        INNER JOIN libros l
            ON p.id_libro = l.id

        ORDER BY m.fecha_registro DESC
    """)

    multas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "multas.html",
        multas=multas
    )


@multas_bp.route(
    "/multas/agregar",
    methods=["GET", "POST"]
)
def agregar_multa():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO multas
            (
                descripcion,
                monto,
                fecha_registro,
                estado,
                id_prestamo
            )
            VALUES
            (
                %s,
                %s,
                NOW(),
                %s,
                %s
            )
        """, (
            request.form["descripcion"],
            request.form["monto"],
            request.form["estado"],
            request.form["id_prestamo"]
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("multas.listar_multas")
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
        ORDER BY p.id_prestamo DESC
    """)

    prestamos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "multas_agregar.html",
        prestamos=prestamos
    )


@multas_bp.route(
    "/multas/pagar/<int:id>"
)
def pagar_multa(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE multas
        SET estado='Pagada'
        WHERE id_multa=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("multas.listar_multas")
    )
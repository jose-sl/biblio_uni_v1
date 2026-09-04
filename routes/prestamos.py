from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

prestamos_bp = Blueprint(
    "prestamos",
    __name__
)


@prestamos_bp.route("/prestamos")
def listar_prestamos():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_prestamo,
            p.fecha_prestamo,
            p.fecha_limite,
            p.estado,

            u.nombre AS usuario,

            l.titulo AS libro

        FROM prestamos p

        INNER JOIN usuarios u
            ON p.id_usuario = u.id

        INNER JOIN libros l
            ON p.id_libro = l.id

        ORDER BY p.fecha_prestamo DESC
    """)

    prestamos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "prestamos.html",
        prestamos=prestamos
    )


@prestamos_bp.route(
    "/prestamos/agregar",
    methods=["GET", "POST"]
)
def agregar_prestamo():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        id_usuario = request.form["id_usuario"]
        id_libro = request.form["id_libro"]
        fecha_limite = request.form["fecha_limite"]

        cursor.execute("""
            INSERT INTO prestamos
            (
                fecha_prestamo,
                fecha_limite,
                estado,
                id_usuario,
                id_libro
            )
            VALUES
            (
                NOW(),
                %s,
                'Prestado',
                %s,
                %s
            )
        """, (
            fecha_limite,
            id_usuario,
            id_libro
        ))

        cursor.execute("""
            UPDATE libros
            SET ejemplares_disponibles =
                ejemplares_disponibles - 1
            WHERE id=%s
        """, (id_libro,))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("prestamos.listar_prestamos")
        )

    cursor.execute("""
        SELECT
            id,
            nombre
        FROM usuarios
        WHERE estado='Activo'
        ORDER BY nombre
    """)

    usuarios = cursor.fetchall()

    cursor.execute("""
        SELECT
            id,
            titulo
        FROM libros
        WHERE ejemplares_disponibles > 0
        ORDER BY titulo
    """)

    libros = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "prestamos_agregar.html",
        usuarios=usuarios,
        libros=libros
    )


@prestamos_bp.route(
    "/prestamos/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar_prestamo(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        cursor.execute("""
            UPDATE prestamos
            SET
                fecha_limite=%s,
                estado=%s
            WHERE id_prestamo=%s
        """, (
            request.form["fecha_limite"],
            request.form["estado"],
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("prestamos.listar_prestamos")
        )

    cursor.execute("""
        SELECT *
        FROM prestamos
        WHERE id_prestamo=%s
    """, (id,))

    prestamo = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "prestamos_editar.html",
        prestamo=prestamo
    )


@prestamos_bp.route(
    "/prestamos/eliminar/<int:id>"
)
def eliminar_prestamo(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_libro
        FROM prestamos
        WHERE id_prestamo=%s
    """, (id,))

    prestamo = cursor.fetchone()

    if prestamo:

        cursor.execute("""
            UPDATE libros
            SET ejemplares_disponibles =
                ejemplares_disponibles + 1
            WHERE id=%s
        """, (
            prestamo["id_libro"],
        ))

        cursor.execute("""
            DELETE FROM prestamos
            WHERE id_prestamo=%s
        """, (id,))

        conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("prestamos.listar_prestamos")
    )
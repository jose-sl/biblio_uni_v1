from flask import Blueprint, render_template, request, redirect, url_for

from database import get_connection

libros_bp = Blueprint(
    "libros",
    __name__
)


@libros_bp.route("/libros")
def listar_libros():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            l.id,
            l.isbn,
            l.titulo,
            l.editorial,
            l.anio_publicacion,
            l.ejemplares_totales,
            l.ejemplares_disponibles,
            l.ubicacion,
            l.estado,
            CONCAT(
                a.nombres,
                ' ',
                a.apellidos
            ) AS autor,
            c.nombre AS categoria
        FROM libros l
        INNER JOIN autores a
            ON l.id_autor = a.id
        INNER JOIN categorias c
            ON l.id_categoria = c.id
        ORDER BY l.titulo
    """)

    libros = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "libros.html",
        libros=libros
    )


@libros_bp.route("/libros/agregar", methods=["GET", "POST"])
def agregar_libro():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO libros
            (
                isbn,
                titulo,
                editorial,
                anio_publicacion,
                ejemplares_totales,
                ejemplares_disponibles,
                ubicacion,
                estado,
                id_categoria,
                id_autor
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
        """, (
            request.form["isbn"],
            request.form["titulo"],
            request.form["editorial"],
            request.form["anio_publicacion"],
            request.form["ejemplares_totales"],
            request.form["ejemplares_disponibles"],
            request.form["ubicacion"],
            request.form["estado"],
            request.form["id_categoria"],
            request.form["id_autor"]
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("libros.listar_libros")
        )

    cursor.execute("""
        SELECT id,
               nombre
        FROM categorias
        ORDER BY nombre
    """)
    categorias = cursor.fetchall()

    cursor.execute("""
        SELECT
            id,
            CONCAT(nombres,' ',apellidos) nombre
        FROM autores
        ORDER BY apellidos
    """)
    autores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "libros_agregar.html",
        categorias=categorias,
        autores=autores
    )


@libros_bp.route("/libros/editar/<int:id>", methods=["GET", "POST"])
def editar_libro(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        cursor.execute("""
            UPDATE libros
            SET
                isbn=%s,
                titulo=%s,
                editorial=%s,
                anio_publicacion=%s,
                ejemplares_totales=%s,
                ejemplares_disponibles=%s,
                ubicacion=%s,
                estado=%s,
                id_categoria=%s,
                id_autor=%s
            WHERE id=%s
        """, (
            request.form["isbn"],
            request.form["titulo"],
            request.form["editorial"],
            request.form["anio_publicacion"],
            request.form["ejemplares_totales"],
            request.form["ejemplares_disponibles"],
            request.form["ubicacion"],
            request.form["estado"],
            request.form["id_categoria"],
            request.form["id_autor"],
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("libros.listar_libros")
        )

    cursor.execute("""
        SELECT *
        FROM libros
        WHERE id=%s
    """, (id,))

    libro = cursor.fetchone()

    cursor.execute("""
        SELECT id, nombre
        FROM categorias
        ORDER BY nombre
    """)
    categorias = cursor.fetchall()

    cursor.execute("""
        SELECT
            id,
            CONCAT(nombres,' ',apellidos) nombre
        FROM autores
        ORDER BY apellidos
    """)
    autores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "libros_editar.html",
        libro=libro,
        categorias=categorias,
        autores=autores
    )


@libros_bp.route("/libros/eliminar/<int:id>")
def eliminar_libro(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM libros
        WHERE id=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("libros.listar_libros")
    )
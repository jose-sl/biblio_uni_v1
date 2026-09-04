from flask import Blueprint, render_template, request, redirect, url_for

from database import get_connection

categorias_bp = Blueprint(
    "categorias",
    __name__
)


@categorias_bp.route("/categorias")
def listar_categorias():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nombre,
            descripcion
        FROM categorias
        ORDER BY nombre
    """)

    categorias = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "categorias.html",
        categorias=categorias
    )


@categorias_bp.route("/categorias/agregar", methods=["GET", "POST"])
def agregar_categoria():

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO categorias
            (
                nombre,
                descripcion
            )
            VALUES
            (
                %s,
                %s
            )
        """, (
            request.form["nombre"],
            request.form["descripcion"]
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("categorias.listar_categorias")
        )

    return render_template(
        "categorias_agregar.html"
    )


@categorias_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
def editar_categoria(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        cursor.execute("""
            UPDATE categorias
            SET
                nombre=%s,
                descripcion=%s
            WHERE id=%s
        """, (
            request.form["nombre"],
            request.form["descripcion"],
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("categorias.listar_categorias")
        )

    cursor.execute("""
        SELECT *
        FROM categorias
        WHERE id=%s
    """, (id,))

    categoria = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "categorias_editar.html",
        categoria=categoria
    )


@categorias_bp.route("/categorias/eliminar/<int:id>")
def eliminar_categoria(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM categorias
        WHERE id=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("categorias.listar_categorias")
    )
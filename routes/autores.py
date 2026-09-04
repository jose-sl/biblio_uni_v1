from flask import Blueprint, render_template, request, redirect, url_for

from database import get_connection

autores_bp = Blueprint(
    "autores",
    __name__
)


@autores_bp.route("/autores")
def listar_autores():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nombres,
            apellidos,
            nacionalidad
        FROM autores
        ORDER BY apellidos, nombres
    """)

    autores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "autores.html",
        autores=autores
    )


@autores_bp.route("/autores/agregar", methods=["GET", "POST"])
def agregar_autor():

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO autores
            (
                nombres,
                apellidos,
                nacionalidad
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
        """, (
            request.form["nombres"],
            request.form["apellidos"],
            request.form["nacionalidad"]
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("autores.listar_autores")
        )

    return render_template(
        "autores_agregar.html"
    )


@autores_bp.route("/autores/editar/<int:id>", methods=["GET", "POST"])
def editar_autor(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        cursor.execute("""
            UPDATE autores
            SET
                nombres=%s,
                apellidos=%s,
                nacionalidad=%s
            WHERE id=%s
        """, (
            request.form["nombres"],
            request.form["apellidos"],
            request.form["nacionalidad"],
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("autores.listar_autores")
        )

    cursor.execute("""
        SELECT *
        FROM autores
        WHERE id=%s
    """, (id,))

    autor = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "autores_editar.html",
        autor=autor
    )


@autores_bp.route("/autores/eliminar/<int:id>")
def eliminar_autor(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM autores
        WHERE id=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("autores.listar_autores")
    )
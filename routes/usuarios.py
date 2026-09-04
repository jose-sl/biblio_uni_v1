from flask import Blueprint, render_template, request, redirect, url_for

from database import get_connection

usuarios_bp = Blueprint(
    "usuarios",
    __name__
)


@usuarios_bp.route("/usuarios")
def listar_usuarios():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nombre,
            carnet,
            correo,
            telefono,
            usuario,
            rol,
            estado
        FROM usuarios
        ORDER BY nombre
    """)

    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )


@usuarios_bp.route("/usuarios/agregar", methods=["GET", "POST"])
def agregar_usuario():

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios
            (
                nombre,
                carnet,
                correo,
                telefono,
                usuario,
                password,
                rol,
                estado
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s
            )
        """, (
            request.form["nombre"],
            request.form["carnet"],
            request.form["correo"],
            request.form["telefono"],
            request.form["usuario"],
            request.form["password"],
            request.form["rol"],
            request.form["estado"]
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("usuarios.listar_usuarios")
        )

    return render_template(
        "usuarios_agregar.html"
    )


@usuarios_bp.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        password = request.form["password"]

        if password:

            cursor.execute("""
                UPDATE usuarios
                SET
                    nombre=%s,
                    carnet=%s,
                    correo=%s,
                    telefono=%s,
                    usuario=%s,
                    password=%s,
                    rol=%s,
                    estado=%s
                WHERE id=%s
            """, (
                request.form["nombre"],
                request.form["carnet"],
                request.form["correo"],
                request.form["telefono"],
                request.form["usuario"],
                password,
                request.form["rol"],
                request.form["estado"],
                id
            ))

        else:

            cursor.execute("""
                UPDATE usuarios
                SET
                    nombre=%s,
                    carnet=%s,
                    correo=%s,
                    telefono=%s,
                    usuario=%s,
                    rol=%s,
                    estado=%s
                WHERE id=%s
            """, (
                request.form["nombre"],
                request.form["carnet"],
                request.form["correo"],
                request.form["telefono"],
                request.form["usuario"],
                request.form["rol"],
                request.form["estado"],
                id
            ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(
            url_for("usuarios.listar_usuarios")
        )

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE id=%s
    """, (id,))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "usuarios_editar.html",
        usuario=usuario
    )


@usuarios_bp.route("/usuarios/eliminar/<int:id>")
def eliminar_usuario(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("usuarios.listar_usuarios")
    )
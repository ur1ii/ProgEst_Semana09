import os
from uuid import uuid4

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from stack import Stack


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY",
    "clave-local-solo-para-desarrollo",
)

DEFAULT_CAPACITY = 5

# Almacenamiento temporal de las pilas de cada sesión.
stacks = {}


def get_current_stack():
    """Obtiene la pila asociada a la sesión actual."""

    stack_id = session.get("stack_id")

    if stack_id is None:
        stack_id = str(uuid4())
        session["stack_id"] = stack_id

    if stack_id not in stacks:
        stacks[stack_id] = Stack(DEFAULT_CAPACITY)

    return stacks[stack_id]


def parse_positive_integer(value, field_name):
    """Valida que un valor recibido sea un entero positivo."""

    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"{field_name} debe ser un número entero."
        ) from None

    if number <= 0:
        raise ValueError(
            f"{field_name} debe ser mayor que cero."
        )

    return number


@app.route("/", methods=["GET"])
def index():
    """Muestra la interfaz principal."""

    stack = get_current_stack()

    return render_template(
        "index.html",
        stack_items=list(reversed(stack.items)),
        capacity=stack.capacity,
        size=stack.size,
        is_empty=stack.is_empty,
        is_full=stack.is_full,
        top_item=None if stack.is_empty else stack.peek(),
    )


@app.route("/push", methods=["POST"])
def push():
    """Agrega un elemento a la pila."""

    stack = get_current_stack()
    item = request.form.get("item", "").strip()

    if not item:
        flash("Escribe un valor antes de apilar.", "warning")
        return redirect(url_for("index"))

    if len(item) > 100:
        flash(
            "El elemento no puede superar los 100 caracteres.",
            "warning",
        )
        return redirect(url_for("index"))

    if stack.is_full:
        flash("La pila está llena.", "danger")
        return redirect(url_for("index"))

    stack.push(item)

    flash(f"Elemento «{item}» apilado correctamente.", "success")

    return redirect(url_for("index"))


@app.route("/pop", methods=["POST"])
def pop():
    """Elimina el elemento del tope."""

    stack = get_current_stack()

    if stack.is_empty:
        flash("No puedes desapilar: la pila está vacía.", "warning")
        return redirect(url_for("index"))

    item = stack.pop()

    flash(f"Elemento «{item}» desapilado.", "success")

    return redirect(url_for("index"))


@app.route("/peek", methods=["POST"])
def peek():
    """Consulta el elemento del tope."""

    stack = get_current_stack()

    if stack.is_empty:
        flash("La pila está vacía.", "warning")
    else:
        flash(f"El elemento del tope es: {stack.peek()}", "info")

    return redirect(url_for("index"))


@app.route("/clear", methods=["POST"])
def clear():
    """Vacía la pila."""

    stack = get_current_stack()
    stack.clear()

    flash("La pila se ha vaciado correctamente.", "success")

    return redirect(url_for("index"))


@app.route("/capacity", methods=["POST"])
def change_capacity():
    """Modifica la capacidad máxima de la pila."""

    stack = get_current_stack()

    try:
        new_capacity = parse_positive_integer(
            request.form.get("capacity"),
            "La capacidad",
        )

        stack.set_capacity(new_capacity)

    except (ValueError, TypeError) as error:
        flash(str(error), "danger")
        return redirect(url_for("index"))

    flash(
        f"Capacidad actualizada a {new_capacity}.",
        "success",
    )

    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    """Muestra un mensaje para rutas inexistentes."""

    return "Página no encontrada.", 404


if __name__ == "__main__":
    app.run(debug=True)
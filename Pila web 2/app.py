
import os
import uuid
from pathlib import Path

import cv2
import numpy as np
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

import photoStack


# --------------------------------------------------
# Configuración de la aplicación
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
RESULT_DIR = BASE_DIR / "static" / "results"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB por solicitud

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGES = 30


def allowed_file(filename):
    """Comprueba que el archivo tenga una extensión permitida."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def load_image(file_path):
    """Lee una fotografía y la convierte al formato BGR de OpenCV."""
    image = cv2.imread(str(file_path))

    if image is None:
        raise ValueError(f"No se pudo leer la imagen: {file_path.name}")

    return image


def process_stack(image_paths, output_path):
    """
    Integra photoStack.py.

    Contrato esperado:
        photoStack.stack_images(images)

    Debe recibir una lista de imágenes OpenCV (arrays NumPy)
    y devolver la imagen final como array NumPy.
    """
    images = [load_image(path) for path in image_paths]

    if len(images) < 2:
        raise ValueError("Se necesitan al menos dos fotografías.")

    # Llamada al módulo que ya tienes.
    result = photoStack.stack_images(images)

    if result is None or not isinstance(result, np.ndarray):
        raise ValueError(
            "photoStack.stack_images() debe devolver una imagen "
            "como array de NumPy."
        )

    if result.size == 0:
        raise ValueError("El procesamiento produjo una imagen vacía.")

    success = cv2.imwrite(str(output_path), result)

    if not success:
        raise ValueError("No se pudo guardar la imagen procesada.")

    return result


# --------------------------------------------------
# Página principal
# --------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------
# Recepción y procesamiento de fotografías
# --------------------------------------------------

@app.route("/process", methods=["POST"])
def process_images():
    saved_files = []

    try:
        files = request.files.getlist("images")

        if len(files) < 2:
            return jsonify({
                "error": "Captura o selecciona al menos dos fotografías."
            }), 400

        if len(files) > MAX_IMAGES:
            return jsonify({
                "error": f"El máximo permitido es de {MAX_IMAGES} fotografías."
            }), 400

        for file in files:
            if not file or not file.filename:
                continue

            if not allowed_file(file.filename):
                raise ValueError(
                    "Formato no permitido. Usa JPG, JPEG, PNG o WEBP."
                )

            extension = Path(secure_filename(file.filename)).suffix.lower()
            filename = f"{uuid.uuid4().hex}{extension}"
            file_path = UPLOAD_DIR / filename

            file.save(file_path)
            saved_files.append(file_path)

        if len(saved_files) < 2:
            raise ValueError("No se recibieron suficientes imágenes válidas.")

        result_name = f"stack_{uuid.uuid4().hex}.jpg"
        result_path = RESULT_DIR / result_name

        process_stack(saved_files, result_path)

        return jsonify({
            "message": "Apilamiento completado correctamente.",
            "result": url_for("static", filename=f"results/{result_name}"),
            "download": url_for("download_result", filename=result_name),
            "count": len(saved_files),
        })

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Error durante el apilamiento.")
        return jsonify({
            "error": (
                "No se pudo procesar la imagen. Revisa la función "
                "stack_images de photoStack.py y la terminal de Flask."
            )
        }), 500

    finally:
        # Elimina las fotografías temporales recibidas.
        for file_path in saved_files:
            try:
                file_path.unlink(missing_ok=True)
            except OSError:
                app.logger.warning(
                    "No se pudo eliminar el archivo temporal: %s",
                    file_path,
                )


# --------------------------------------------------
# Descarga del resultado
# --------------------------------------------------

@app.route("/download/<filename>")
def download_result(filename):
    # Evita que se soliciten rutas arbitrarias.
    if Path(filename).name != filename:
        return jsonify({"error": "Nombre de archivo no válido."}), 400

    return send_from_directory(
        RESULT_DIR,
        filename,
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(debug=True)

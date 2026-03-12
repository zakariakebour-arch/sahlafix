from app import create_app
from flask import send_from_directory
from dotenv import load_dotenv
import os
load_dotenv()
app = create_app()

# Ruta absoluta a la carpeta de avatars
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "app", "uploads", "avatars")

@app.route("/api/v1/uploads/avatars/<filename>")
def get_avatar(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
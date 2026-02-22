from flask import Flask, request, send_file
import zipfile
import io

app = Flask(__name__)

@app.route('/api/zip', methods=['POST'])
def generate_zip():
    if 'file' not in request.files:
        return {"error": "No file"}, 400

    file = request.files['file']

    if file.filename == '':
        return {"error": "No selected file"}, 400

    memory_zip = io.BytesIO()
    with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(file.filename, file.read())

    memory_zip.seek(0)

    return send_file(
        memory_zip,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{file.filename}.zip"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

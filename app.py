import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from utils.converter import convert_to_markdown
import tempfile

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "markitdown-converter-secret-key"

# Configure upload settings
ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'pptx', 'xlsx', 
    'png', 'jpg', 'jpeg', 'gif',
    'mp3', 'wav', 'html', 'csv', 
    'json', 'xml'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400

    try:
        # Create temp directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            temp_file_path = os.path.join(temp_dir, secure_filename(file.filename))
            file.save(temp_file_path)
            
            # Convert file to markdown
            markdown_content = convert_to_markdown(temp_file_path)
            
            # Create temporary markdown file
            output_path = os.path.join(temp_dir, 'converted.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return jsonify({
                'success': True,
                'markdown': markdown_content
            })
    
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

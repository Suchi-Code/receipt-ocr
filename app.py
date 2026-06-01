from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['receipt']
    img = Image.open(file)

    text = pytesseract.image_to_string(img, lang='tha')

    company = re.search(r'บริษัท\s+(.*)', text)
    amount = re.search(r'ยอดรวม\s+([\d,\.]+)', text)

    data = {
        "company": company.group(1).strip() if company else None,
        "amount": amount.group(1).strip() if amount else None,
        "raw_text": text
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

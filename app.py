import ddddocr
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
# تفعيل CORS للسماح لإضافة المتصفح بالاتصال بالسيرفر
CORS(app)

# تحميل المكتبة في الذاكرة مرة واحدة عند التشغيل لسرعة الحل
ocr = ddddocr.DdddOcr(show_ad=False)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json.get('image')
        if not data:
            return jsonify({"error": "No image data provided"}), 400
        
        # تحويل Base64 إلى بايتات
        img_bytes = base64.b64decode(data)
        
        # فك التشفير (الحل)
        result = ocr.classification(img_bytes)
        
        print(f"[*] Done: {result}")
        return jsonify({"code": result})
    
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Railway يحدد المنفذ تلقائياً عبر متغيرات البيئة
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

from datetime import datetime
import cv2
import re
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
from cnn import predict

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        ans = get_answer(request)
        return jsonify({'ans': ans})
    else:
        return render_template('index.html')
    
def get_answer(req):
    img_str = re.search(r'base64,(.*)', req.form['img']).group(1)
    nparr = np.fromstring(base64.b64decode(img_str), np.uint8)
    img_src = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_negaposi = 255 - img_src
    img_gray = cv2.cvtColor(img_negaposi, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(img_gray,(28,28))
    cv2.imwrite(f"images/{datetime.now().strftime('%s')}.jpg",img_resize)
    ans = predict.result(img_resize)
    return ans

if __name__ == "__main__":
    app.run()
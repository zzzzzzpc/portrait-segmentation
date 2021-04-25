# coding:utf-8

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import time

from segmentation.client_rest import *

from datetime import timedelta

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

# 添加路由,负责人像风格部分
@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # 获取上传图片
        f = request.files['file']
        fb = request.files['fileback']

        if not (f and allowed_file(f.filename) and fb and allowed_file(fb.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        # 当前文件所在路径
        basepath = os.path.dirname(__file__)

        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径，将原图备份到服务器
        path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        path_back = os.path.join(basepath, 'static/images', secure_filename(fb.filename))
        f.save(path)
        fb.save(path_back)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'portrait.jpg'), img)

        img_back = cv2.imread(path_back)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'background.jpg'), img_back)

        # 合并之后的图片调用分割函数，将结果图片同时也备份到服务器
        result_img = client_rest(path, path_back)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'result.jpg'), result_img)

        return render_template('index_ok.html', val1=time.time())

    return render_template('index.html')

if __name__ == '__main__':
    # app.debug = True
    app.run()

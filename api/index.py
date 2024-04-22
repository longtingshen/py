import hashlib
import requests
import uuid
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
def get_num(aid, index):
    normalCutNum = 10  # 默认切割数
    aIndex = str(aid) + str(index)  # aid 和 index
    aIndex = hashlib.md5(aIndex.encode()).hexdigest()  # MD5 加密
    aIndex = ord(aIndex[-1])  # 获取最后一位的 Unicode 码表位置
    if 268850 <= int(aid) <= 421925:
        aIndex %= 10
    elif int(aid) >= 421926:
        aIndex %= 8
    if aIndex in range(10):
        normalCutNum = 2 + 2 * aIndex
    return normalCutNum

def on_image_loaded(url):
    urls = url.split('/')
    aid = urls[-2]
    img_name = urls[-1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("下载失败")
        return ""
    img = Image.open(BytesIO(response.content))
    canvas = Image.new('RGB', img.size)  # 创建一个与图片大小相同的画布
    canvas.paste(img)  # 将图片粘贴到画布上
    index = img_name.split(".")[0]  # 获取图片在一组中的index，当前为00002
    cut_num = get_num(str(aid), str(index))  # 获取分割次数
    unknown = img.size[1] % cut_num  # 偏移高度，最后一张图的高度会比其他图高度要高
    output_img = BytesIO()
    for m in range(cut_num):
        cut_height = img.size[1] // cut_num  # 分割的高度
        y_coordinate = cut_height * m  # 要分割的y坐标
        end_coordinate = img.size[1] - cut_height * (m + 1) - unknown  # 要分割的图片底部y
        if m == 0:
            cut_height += unknown
        else:
            y_coordinate += unknown
        region = (0, end_coordinate, img.size[0], end_coordinate + cut_height)
        region_img = img.crop(region)
        canvas.paste(region_img, (0, y_coordinate))
    # 返回文件数据
    canvas.save(output_img, format='JPEG')  # 这里可以根据需要选择图片格式
    output_img.seek(0)
    return output_img


@app.route('/jm', methods=['GET', 'POST'])
def go_jm():
    url = request.args.get('url')
    if len(url) <= 0:
        return jsonify({"code": "异常", "message": "url参数不能为空"})
    img_io = on_image_loaded(url)

    response = make_response(img_io)

    # 设置响应头部信息，指定附件名称
    response.headers.set('Content-Disposition', 'attachment', filename=f'{uuid.uuid4()}.jpg')
    response.headers.set('Content-Type', 'image/jpeg')

    # 返回响应对象
    return response


@app.route('/', methods=["GET"])
def return_OneText():
    return "<h1>欢迎使用本接口</h1>"




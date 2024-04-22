# 1, debug模式: 开启debug 模式 点右上角的Flask -> 编辑 -> FLASK_DEBUG(勾选上)  ===》 * Debug mode: on 终端显示成功
# 1.1 开启debug后，改变代码自动重启
# 1.2 如果开发的时候出现BUG，开启了debug后在浏览器上就可以看到出错信息

# 2， 修改host:
# 主要的作用：就是让其它设备可以访问我们电脑上的项目 修改 点右上角的Flask -> 编辑 -> 其他选项 -> --host=0.0.0.0 ===》Running on http://192.168.1.5:5000 终端显示成功

# 3, 修改端口号:
# 3.1 修改 点右上角的Flask -> 编辑 -> 其他选项 -> --host=0.0.0.0 --port=8000
from flask import Flask, request

# 使用Flask类创建一个app对象

app = Flask(__name__)


# 创建一个路由和一个视图函数的映射
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello 中国！！,我又来学python了'


@app.route('/profile')
def profile():
    return '我是个人中心'


@app.route('/a/<booy_id>')  # 默认字符串
def booy1(booy_id):
    return f"你访问的id是：{booy_id}"


@app.route('/a/b/<int:bl>')  # bl必须是一个整形才会监听到
def booy2(bl):
    return f"你访问的数字是：{bl}"


@app.route('/c')
def booy3():
    data = request.args.get('p', default=1, type=int)  # p是参数 default=1是默认值  type=str是类型
    return f"你获取到的参数是：{data}"


if __name__ == '__main__':
    app.run(debug=True)  # debug=True 开启debug模式


class Args:
    # 构造函数，当创建对象时自动调用
    def __init__(self, msg="代码开发", url="http://eds.newtouch.cn:8081/eds3/"):
        # 定义对象的属性
        self.user = None
        self.password = None
        self.msg = msg
        self.url = url
        self.headless = True
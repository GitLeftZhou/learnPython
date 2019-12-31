class Person:
    """
    关键字 class 声明一个类 Person
    """

    def __init__(self, name, gender, works):
        """
        定义属性  属性都在__init__里面定义
        :param name: 姓名
        :param gender: 性别
        :param work :  工作
        """
        self.name = name
        self.gender = gender
        self.works = works

    def say(self):
        """
        方法 (就是执行具体操作的实体)
        :return:
        """
        print("hello everyone,my name is ", self.name)

    def do_work(self):
        """
        示例 for 循环
        :return:
        """
        for work in self.works:
            print("I'm doing ", work)


class Girl(Person):
    """
    继承 Person 拥有Person的所有特性
    """
    def make_up(self):
        """
        当前class 自有的特性
        :return:
        """
        print("I'm a pretty girl ,i am good at make up")


# 运行入口
if __name__ == "__main__":
    # 定义变量
    p_name = "张三"
    p_gender = "boy"
    p_works = ["做作业", "聊微信", "打游戏"]
    # 实例化一个对象(根据class模版创建具体的个体)
    zhang_san = Person(p_name, p_gender, p_works)
    # 调用对象的方法，方法就是  do 做事
    zhang_san.say()
    zhang_san.do_work()

    p_name = "xiao zou"
    p_gender = "girl"
    p_works = ["做作业", "聊微信", "看电视"]
    # 实例化一个对象(根据class模版创建具体的个体)
    xiao_zou = Girl(p_name, p_gender, p_works)
    # 调用对象的方法，方法就是  do 做事
    xiao_zou.say()
    xiao_zou.do_work()
    xiao_zou.make_up()

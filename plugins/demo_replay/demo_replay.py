from plugins.plugin import Plugin


class Demo_replay(Plugin):
    """
    这是一个Demo插件，用于回复用户的消息，用户发什么就回复什么。
    类的名称需要与包名一致，否则无法正常加载。
    """
    name = 'Demo_replay'

    def deal_msg(self):
        """
        这里写你的业务处理逻辑，
        过滤器已经将您不需要的消息过滤掉了，
        能到这儿的全是真实有效需要处理的消息 。
        :return:
        """
        # 将收到的消息转发给发送消息的人。
        self.wcf.forward_msg(self.msg.id, self.msg.sender)

    def filter_msg(self) -> bool:
        """
        黑名单过滤机制，默认通过原则。
        :return:
        """

        print(f"{self.name}插件收到消息如下：")
        print(f"发送人：{self.msg.sender}\n"
              f"消息类型：{self.msg.type}\n"
              f"消息微信群ID：{self.msg.roomid}\n"
              f"消息ID：{self.msg.id}")

        # 消息类型过滤，不是指定类型的消息不处理，1代表文本消息，3代表图片消息
        if self.msg.type not in [1]:
            return False

        # 群消息不处理
        if self.msg.from_group():
            return False

        return True

    def run(self):
        """
        插件运行入口函数
        :return:
        """

        # 初始化配置信息
        self.init_config_data()
        # 消息过滤器检查
        if self.filter_msg():
            self.deal_msg()
        else:
            print(f"{self.name}：此消息插件不需要处理！")

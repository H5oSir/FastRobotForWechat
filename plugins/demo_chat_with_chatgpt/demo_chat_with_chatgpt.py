from datetime import datetime
from plugins.plugin import Plugin
from openai import OpenAI


class Demo_chat_with_chatgpt(Plugin):
    """
    这是一个接入AI对话的插件，用来给开发者做演示的。
    类的名称需要与包名一致，否则无法正常加载。
    """
    name = 'Demo_chat_with_chatgpt'

    def deal_msg(self):
        """
        这里写你的业务处理逻辑，
        过滤器已经将您不需要的消息过滤掉了，
        能到这儿的全是真实有效需要处理的消息 。
        :return:
        """
        # 将收到的消息调用AI的接口进行问答。
        client = OpenAI(api_key=self.config.get("api_key"), base_url=self.config.get("base_url"))
        current_time_local = datetime.now().astimezone()
        response = client.chat.completions.create(model=self.config.get("model_name"), messages=[{
            "role": "system",
            "content": f"{self.config.get('system_prompt')} 当前时间（本地时区）: {current_time_local}"
        },
            {
                "role": "user",
                "content": self.msg.content
            }
        ])
        text = response.choices[0].message.content
        self.wcf.send_text(text, self.msg.roomid if self.msg.from_group() else self.msg.sender, None)

    def filter_msg(self) -> bool:
        """
        黑名单过滤机制，默认通过原则。
        :return:
        """

        # 消息类型过滤，不是指定类型的消息不处理，1代表文本消息，3代表图片消息
        if self.msg.type not in [1]:
            return False

        # 群消息不处理
        if self.msg.from_group() and self.msg.roomid not in self.config.get("chat_room_id", []):
            return False
        if not self.msg.from_group() and self.msg.sender not in self.config.get("chat_wxid", []):
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

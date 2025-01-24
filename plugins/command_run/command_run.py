from pprint import pprint as print
from plugins.plugin import Plugin


def get_function_name(text: str):
    """
    demo: call get_user_info() or forward_msg("1154564564156", "wxid_xxxxxx")
    :param text:
    :return:
    """
    return text.split(" ")[-1]


class Command_run(Plugin):
    """
    这是一个执行wcf实例函数的插件，用来给开发者通过私信的方式执行wcf函数获取需要的信息。
    类的名称需要与包名一致，否则无法正常加载。
    """
    _status = False
    name = 'Command_run'

    def deal_msg(self):
        """
        这里写你的业务处理逻辑，
        过滤器已经将您不需要的消息过滤掉了，
        能到这儿的全是真实有效需要处理的消息 。
        self.msg.content: call get_user_info() or forward_msg("1154564564156", "wxid_xxxxxx")
        :return:
        """
        if self.msg.content.startswith("call "):
            function_name = get_function_name(self.msg.content)
            try:
                response = eval(f"self.wcf.{function_name}")
                print(f"{function_name} 结果如下:")
                print(response)
                text = f"self.wcf.{function_name}执行结果:\n{response}"
                start = 0
                step_len = 4096
                end = step_len
                while end < len(text):
                    self.wcf.send_text(text[start:end - 1], self.msg.sender, None)
                    start = end
                    end = end + step_len
                self.wcf.send_text(text[start:len(text)], self.msg.sender, None)
            except Exception as e:
                text = f"{function_name} 执行错误！错误信息：{e}"
                print(text)
                self.wcf.send_text(text, self.msg.sender, None)
        if self.msg.content == "show groupid" and self.msg.from_group():
            sender_alias_name = self.wcf.get_alias_in_chatroom(self.msg.sender, self.msg.roomid)
            contacts = self.wcf.get_contacts()
            RoomName = ""
            for contact in contacts:
                if contact.get("wxid") == self.msg.roomid:
                    RoomName = contact.get("name")

            text = f"RoomID:{self.msg.roomid} \nRoomName：{RoomName} \nSenderName: {sender_alias_name}\n"
            self.wcf.send_text(text, self.msg.sender, None)
        if self.msg.content == "show wcf" or self.msg.content == "show msg":

            if "msg" in self.msg.content:
                class_name = "msg"
                response = dir(self.msg)
            else:
                class_name = "wcf"
                response = dir(self.wcf)

            text = f"dir({class_name})执行结果:\n{response}"
            start = 0
            step_len = 4096
            end = step_len
            while end < len(text):
                self.wcf.send_text(text[start:end - 1], self.msg.sender, None)
                start = end
                end = end + step_len
            self.wcf.send_text(text[start:len(text)], self.msg.sender, None)

    def filter_msg(self) -> bool:
        """
        黑名单过滤机制，默认通过原则。
        :return:
        """

        # 只处理文本消息
        if self.msg.type not in [1]:
            return False

        # 不是指定用户发的消息不处理
        if self.msg.sender not in self.config.get("manager_wxid", []):
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

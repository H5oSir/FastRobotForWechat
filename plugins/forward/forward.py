import os
import time
from pathlib import Path

from cffi.model import pointer_cache

from plugins.plugin import Plugin
from wcferry import Wcf,WxMsg



user_id="wxid_g22os5kllmh522"
broad_id_list=['wxid_ngacb0c6zloa21',"46179504386@chatroom"]
master_user_id=["wxid_ngacb0c6zloa21"]
master_room_id=["43555336996@chatroom","46179504386@chatroom"]

police_rule={}


class Forward(Plugin):
    name = "消息转发插件"
    _status = True

    def deal_msg(self):
        print(f"消息{self.msg.type} 内容如下所示：")
        for receive_id in self.config.get("slave_room_id"):
            if self.msg.type == 3:
                plugins_dir = Path(__file__).resolve().parent/"img"
                print(plugins_dir)
                # 如果文件夹不存在，则创建文件夹
                if not plugins_dir.exists():
                    plugins_dir.mkdir(parents=True, exist_ok=True)

                # 调用下载函数
                d_path = self.wcf.download_image(self.msg.id, self.msg.extra, os.fspath(plugins_dir), 60)
                print(f"图片下载路径：{d_path}")
                if d_path:
                    send_count=1
                    s_status=-1
                    while send_count<=3 and s_status!=0:
                        s_status = self.wcf.send_image(d_path, receive_id)
                        print(f"图片发送{receive_id} 结果：{s_status}")
                        send_count+=1
            else:
                status = self.wcf.forward_msg(self.msg.id, receive_id)
                print(f"转发给用户{receive_id} 结果：{status}")

    def filter_msg(self):
        # 不是指定的人或群里发的消息不处理
        if not (self.msg.from_group() and self.msg.roomid in self.config.get("master_room_id")):
            # 不需要处理，直接返回
            return False
        # 不是文本 不是图片
        if self.msg.type not in [1,3]:
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

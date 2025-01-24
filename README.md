# FastRobotForWechat

1. 一个快速开发微信机器人的框架。主打Fast，3分钟就玩明白，2分钟安装部署环境，1分钟跑通上手。<br/>
2. 内置了Demo插件案例，开发一个微信机器人功能只需要3分钟，足够的Fast。<br/>
3. 内置了供开发者使用的调试插件（Command_run），可以快速的调试学习wcf框架，方便获取机器人的数据和框架数据。

<details><summary><font color="red" size="12">免责声明【必读】</font></summary>

本工具仅供学习和技术研究使用，不得用于任何商业或非法行为，否则后果自负。

本工具的作者不对本工具的安全性、完整性、可靠性、有效性、正确性或适用性做任何明示或暗示的保证，也不对本工具的使用或滥用造成的任何直接或间接的损失、责任、索赔、要求或诉讼承担任何责任。

本工具的作者保留随时修改、更新、删除或终止本工具的权利，无需事先通知或承担任何义务。

本工具的使用者应遵守相关法律法规，尊重微信的版权和隐私，不得侵犯微信或其他第三方的合法权益，不得从事任何违法或不道德的行为。

本工具的使用者在下载、安装、运行或使用本工具时，即表示已阅读并同意本免责声明。如有异议，请立即停止使用本工具，并删除所有相关文件。

</details>


| <img alt="阿鹏微信" height="400" src="https://7up.pics/images/2025/01/24/_202501240805561.png" width="400"/> | <img alt="交流群" height="400" src="https://7up.pics/images/2025/01/24/_20250124101620.jpeg" width="400"/> |
|:--------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------:|
|                                         扫码私信 `FastRobot` 加微信交流群                                          |                                               直接扫码加微信交流群                                                |

<details><summary>点击查看功能清单</summary>

* 获取登录二维码
* 查询登录状态
* 获取登录账号信息
* 获取消息类型
* 获取联系人
* 获取可查询数据库
* 获取数据库所有表
* 获取语音消息
* 发送文本消息（可 @）
* 发送图片消息
* 发送文件消息
* 发送卡片消息
* 发送 XML 消息
* 发送 GIF 消息
* 拍一拍群友
* 转发消息
* 开启接收消息
* 关闭接收消息
* 查询数据库
* 获取朋友圈消息
* 下载图片、视频、文件
* 解密图片
* 添加群成员
* 删除群成员
* 邀请群成员

</details>

## 快速开始
### Python3.11
1.点击 [微信安装包下载](https://github.com/lich0821/WeChatFerry/releases/tag/v39.3.5) 下载3.9.11.25版本的微信安装包，安装运行，然后正常登录微信。

2.下载项目到本地,安装项目的依赖。
```sh
pip install -r requirements.txt
```

3.检查plugins目录下的插件配置是否要开启，然后启动项目。
```sh
python3 robot.py
```
整个框架的核心就是 wcf 和 msg 这两个类实例，因此必看 WeChatFerry内置函数查询和消息类型查询： [使用 WeChatFerry 搭建部署微信机器人详细教程](https://blog.csdn.net/qq_47452807/article/details/138536720)

## 插件机制
### 插件生命周期
1. 框架实例化插件类
2. 框架会调用插件的run函数
3. 插件执行完毕后数据释放，数据跨插件生命周期和跨插件共享请使用wcf的share_data
### 插件代码示例
Demo_replay插件代码
```sh
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

```

## 进阶资料
* 本项目基于 WeChatFerry 进行封装开发，建议了解一下 WeChatFerry 。

|[📖 Python 文档](https://wechatferry.readthedocs.io/)|[📺 Python 视频教程](https://mp.weixin.qq.com/s/APdjGyZ2hllXxyG_sNCfXQ)|[🙋 FAQ](https://mp.weixin.qq.com/s/YvgFFhF6D-79kXDzRqtg6w)|
|:-:|:-:|:-:|

* 可参考学习案例：[🤖WeChatRobot](https://github.com/lich0821/WeChatRobot)

## 项目结构

```sh
WeChatFerry
├── LICENSE                 # LICENSE
├── README.md               # 说明
├── robot.py                # 运行入口
└── plugins                 # 插件目录
```

## 致谢
1. 本项目基于<strong>[WeChatFerry🤖](https://github.com/lich0821/WeChatFerry)</strong>进行封装，在此对<strong>WeChatFerry</strong>所有贡献人员由衷的表示感谢！

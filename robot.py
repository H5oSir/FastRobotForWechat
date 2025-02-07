import signal
from pathlib import Path

from wcferry import Wcf, WxMsg
from queue import Empty
from threading import Thread
from plugins.plugin import deal_msg_with_plugins
from common.file import File


file=File()

# __file__ 是当前文件的路径，parent 指向文件所在目录
config_dir = Path(__file__).resolve().parent
print(f"配置文件目录: {config_dir}")

config=file.load_config_from_yaml_file(config_dir)
debug = config.get("debug",False)

wcf = Wcf(debug=debug)
wcf.debug = debug
# 开启插件多线程运行，每个插件一个线程
wcf.multi_threading_run_plugin=config.get("multi_threading_run_plugin",False)

if wcf.is_login():
    print("微信机器人登录状态：True")
    print(f"机器人信息：{wcf.get_user_info()}")
else:
    print("微信机器人登录状态：False")


def handler(sig, frame):
    wcf.cleanup()  # 退出前清理环境
    exit(0)


signal.signal(signal.SIGINT, handler)


def enableReceivingMsg():
    def innerWcFerryProcessMsg():
        while wcf.is_receiving_msg():
            try:
                msg = wcf.get_msg()
                deal_msg_with_plugins(wcf, msg)
            except Empty:
                continue
            except Exception as e:
                print(f"ERROR: {e}")

    wcf.enable_receiving_msg()
    Thread(target=innerWcFerryProcessMsg, name="ListenMessageThread", daemon=True).start()


enableReceivingMsg()

wcf.keep_running()

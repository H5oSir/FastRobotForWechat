import signal
from wcferry import Wcf, WxMsg
from queue import Empty
from threading import Thread
from plugins.plugin import deal_msg_with_plugins

debug = True

wcf = Wcf(debug=debug)
wcf.debug = debug

if wcf.is_login():
    print("微信机器人登录状态：True")
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

import json
import threading

import yaml
from wcferry import Wcf, WxMsg


class Plugin(object):
    wcf: Wcf = None
    msg: WxMsg = None
    name: str = None
    _status: bool = True

    def __init__(self, wcf: Wcf, msg: WxMsg):
        self.wcf = wcf
        self.msg = msg

        self.init_config_data()
        self._status =self.config.get("status",False) or self._status

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

    def help(self) -> str:
        return "No Help"

    def filter_msg(self):
        pass

    def deal_msg(self):
        pass

    def get_status(self) -> bool:
        """
        是否开启插件，默认开启
        :return:
        """
        return self._status

    def load_config_from_json_file(self):
        """
        读取当前插件的 config.json 配置文件。
        """
        # 获取当前插件的目录名（即子类的名称）
        plugin_name = self.__class__.__name__.lower()  # 类名转小写
        print(f"插件名称: {plugin_name}")

        # 获取 plugins 目录的路径
        # __file__ 是当前文件的路径，parent 指向 plugin 目录，再 parent 指向 plugins 目录
        plugins_dir = Path(__file__).resolve().parent
        print(f"plugins 目录: {plugins_dir}")

        # 构建 config.json 的路径
        config_path = plugins_dir / plugin_name / "config.json"
        print(f"配置文件路径: {config_path}")

        # 检查文件是否存在
        if not config_path.exists():
            #raise FileNotFoundError(f"配置文件 {config_path} 不存在！")
            print(f"配置文件 {config_path} 不存在！")
            return {}

        # 读取配置文件
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"配置文件内容: {config}")
        return config

    def load_config_from_yaml_file(self):
        """
        读取当前插件的 config.json 配置文件。
        """
        # 获取当前插件的目录名（即子类的名称）
        plugin_name = self.__class__.__name__.lower()  # 类名转小写
        print(f"插件名称: {plugin_name}")

        # 获取 plugins 目录的路径
        # __file__ 是当前文件的路径，parent 指向 plugin 目录，再 parent 指向 plugins 目录
        plugins_dir = Path(__file__).resolve().parent
        print(f"plugins 目录: {plugins_dir}")

        # 构建 config.json 的路径
        config_path = plugins_dir / plugin_name / "config.yaml"
        print(f"配置文件路径: {config_path}")

        # 检查文件是否存在
        if not config_path.exists():
            #raise FileNotFoundError(f"配置文件 {config_path} 不存在！")
            print(f"配置文件 {config_path} 不存在！")
            return {}

        # 读取配置文件
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print(f"配置文件内容: {config}")
        return config

    def get_value_from_config(self, *keys):
        """
        获取嵌套字典中的值。
        :param keys: 嵌套键，例如 `("app", "settings", "debug")`
        :return: 对应的值，如果键不存在则返回 None
        """
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value

    def init_config_data(self):
        # 从json中导入配置数据
        if not self.config or self.wcf.debug:
            # self.config = self.load_config_from_json_file()
            self.config = self.load_config_from_yaml_file()

    def set_global_share_data(self, key: str = None, data: any = None) -> None:
        if not key:
            key = self.name
        if not hasattr(self.wcf, "share_data"):
            self.wcf.share_data = {}
        self.wcf.share_data[key] = data

    def get_global_share_data(self, key: str = None) -> dict:
        """
        挂载变量到实例wcf的share_data上，
        以实现变量的全局共享、跨插件共享、跨生命周期共享，share_data为dict，
        建议每个plugin的配置变量挂载到share_data["plugin_name"]["config"]里面、
        :param key:
        :return:
        """
        if not key:
            key = self.name
        if not hasattr(self.wcf, "share_data"):
            self.wcf.share_data = {}
        return self.wcf.share_data.get(key, {})

    def set_plugin_global_share_data(self,key:str=None, value: any = None) -> None:
        """
        挂载变量到实例wcf的share_data["plugin_name"]上，
        以实现变量的跨生命周期共享，share_data["plugin_name"]，
        建议不需要跨越plugin传递的变量挂载到share_data["plugin_name"]上，
        建议每个plugin的配置变量挂载到share_data["plugin_name"]["config"]里面、
        :param key:
        :param value:
        :return:
        """
        plugin_global_share_data = self.get_global_share_data(self.name)
        plugin_global_share_data[key]=value
        self.set_global_share_data(key=self.name, data=plugin_global_share_data)

    def get_plugin_global_share_data(self,key:str) -> dict:
        plugin_global_share_data = self.get_global_share_data(self.name)
        return plugin_global_share_data.get(key, {})

    def set_config_data(self, value: any = None) -> None:
        """
        每个plugin的配置变量挂载到share_data["plugin_name"]["config"]里面、
        以实现配置变量的跨生命周期共享，share_data["plugin_name"]["config"]。
        配置变量可以从文件里面读取，可以发送请求从后端获取，从而可以实现不用每次加载插件的时候都获取一遍或发送一次网络请求。
        :param value:
        :return:
        """
        self.set_plugin_global_share_data("config", value)

    def get_config_data(self) -> dict:
        config_data = self.get_plugin_global_share_data(key="config")
        return config_data

    @property
    def config(self):
        return self.get_config_data()

    @config.setter
    def config(self, value):
        self.set_config_data(value)

    @config.deleter
    def config(self):
        self.set_config_data(None)

    @property
    def plugin_global_share_data(self):
        return self.get_global_share_data(key=self.name)

    @plugin_global_share_data.setter
    def plugin_global_share_data(self, value):
        self.set_global_share_data(key=self.name, data=value)

    @plugin_global_share_data.deleter
    def plugin_global_share_data(self):
        self.set_global_share_data(key=self.name, data=None)

    @property
    def global_share_data(self):
        if not hasattr(self.wcf, "share_data"):
            self.wcf.share_data = {}
        return self.wcf.share_data

    @global_share_data.setter
    def global_share_data(self, value):
        if not hasattr(self.wcf, "share_data"):
            self.wcf.share_data = {}
        self.wcf.share_data = value

    @global_share_data.deleter
    def global_share_data(self):
        self.wcf.share_data = {}




def deal_msg_with_plugins(wcf, msg):
    # 获取插件类
    plugins_cls = load_plugins()
    # 检查重新加载
    # check_and_reload_plugins(plugins_cls)
    count=1
    thread_list=[]
    for plugin_name, plugin_class in plugins_cls.items():
        try:
            print(f"第{count}个插件 {plugin_name} 执行开始")
            # 实例化插件类
            plugin_instance = plugin_class(wcf, msg)
            # 调用 run 方法
            if plugin_instance.get_status():
                if wcf.multi_threading_run_plugin:
                    thread = threading.Thread(target=plugin_instance.run,name=plugin_name, daemon=True)
                    thread.start()
                    thread_list.append(thread)
                    print(f"{plugin_name} 开启线程成功")
                else:
                    plugin_instance.run()
                    print(f"{plugin_name} 执行成功")
            else:
                print(f"{plugin_name} 插件未开启")

            count+=1
        except Exception as e:
            print(e)
            print(f"{plugin_name} 执行失败")


import os
import importlib
import time
from pathlib import Path

# 插件文件路径和最后修改时间的字典
plugin_mtimes = {}


def load_plugins(plugins_dir: str = "plugins"):
    """
    加载 plugins 目录下的所有插件类
    :param plugins_dir: plugins 目录路径，默认为 "plugins"
    :return: 返回插件类的字典，键为插件名称，值为插件类
    """
    plugins = {}  # 用于存储插件类
    global plugin_mtimes

    # 获取 plugins 目录的绝对路径
    plugins_dir_path = Path(plugins_dir).resolve()

    # 遍历 plugins 目录下的所有子文件夹
    for entry in os.scandir(plugins_dir_path):
        if entry.is_dir():  # 只处理文件夹
            # 排除_开头的文件夹名称，如 __pycache__
            if entry.name.startswith("_"):
                continue
            plugin_name = entry.name  # 插件文件夹名称
            plugin_module_path = f"{plugins_dir}.{plugin_name}.{plugin_name}"  # 模块路径
            plugin_file_path = plugins_dir_path / plugin_name / f"{plugin_name}.py"  # 插件文件路径

            try:
                # 动态导入插件模块
                plugin_module = importlib.import_module(plugin_module_path)
                # 强制重加载
                plugin_module = importlib.reload(plugin_module)

                # 获取插件类
                plugin_class = getattr(plugin_module, plugin_name.capitalize())

                # 保存插件类
                plugins[plugin_name] = plugin_class
                print(f"成功加载插件类: {plugin_name}")

                # 保存插件文件的最后修改时间
                plugin_mtimes[plugin_file_path] = os.path.getmtime(plugin_file_path)
            except ImportError as e:
                print(f"加载插件 {plugin_name} 失败: {e}")
            except AttributeError as e:
                print(f"插件类 {plugin_name.capitalize()} 不存在: {e}")
            except Exception as e:
                print(f"插件 {plugin_name} 加载失败: {e}")

    return plugins


def reload_plugin(plugin_file_path: str, plugin_module_path: str, plugin_class_name: str):
    """
    重新加载插件模块
    :param plugin_file_path: 插件文件路径
    :param plugin_module_path: 插件模块路径
    :param plugin_class_name: 插件类名
    :return: 返回重新加载后的插件类
    """
    try:
        # 重新加载模块
        plugin_module = importlib.import_module(plugin_module_path)
        plugin_module = importlib.reload(plugin_module)

        # 获取插件类
        plugin_class = getattr(plugin_module, plugin_class_name)
        print(f"重新加载插件类: {plugin_class_name}")
        return plugin_class
    except ImportError as e:
        print(f"重新加载插件失败: {e}")
    except AttributeError as e:
        print(f"插件类 {plugin_class_name} 不存在: {e}")
    except Exception as e:
        print(f"插件重新加载失败: {e}")
    return None


def check_and_reload_plugins(plugins: dict, plugins_dir: str = "plugins"):
    """
    检查插件文件是否修改，如果修改则重新加载
    :param plugins: 插件类的字典
    :param plugins_dir: plugins 目录路径，默认为 "plugins"
    """
    global plugin_mtimes

    # 获取 plugins 目录的绝对路径
    plugins_dir_path = Path(plugins_dir).resolve()

    for plugin_name in list(plugins.keys()):
        # 排除_开头的文件夹名称，如 __pycache__
        if plugin_name.startswith("_"):
            continue
        plugin_module_path = f"{plugins_dir}.{plugin_name}.{plugin_name}"  # 模块路径
        plugin_file_path = plugins_dir_path / plugin_name / f"{plugin_name}.py"  # 插件文件路径

        if os.path.exists(plugin_file_path):
            # 获取文件的最新修改时间
            current_mtime = os.path.getmtime(plugin_file_path)
            last_mtime = plugin_mtimes.get(plugin_file_path)

            # 如果文件修改时间变化，重新加载插件
            if current_mtime != last_mtime:
                plugin_class = reload_plugin(plugin_file_path, plugin_module_path, plugin_name.capitalize())
                if plugin_class:
                    plugins[plugin_name] = plugin_class
                    plugin_mtimes[plugin_file_path] = current_mtime


def run_plugin(plugin_class, *args, **kwargs):
    """
    实例化插件类并调用其 run 方法
    :param plugin_class: 插件类
    :param args: 传递给插件类的初始化参数
    :param kwargs: 传递给插件类的初始化关键字参数
    """
    try:
        # 实例化插件类
        plugin_instance = plugin_class(*args, **kwargs)

        # 调用 run 方法
        plugin_instance.run()
    except Exception as e:
        print(f"插件运行失败: {e}")


# 测试代码
if __name__ == "__main__":
    # 加载所有插件类
    plugins = load_plugins()

    # 主循环：定期检查插件文件是否修改，并运行插件
    while True:
        print("检查插件文件是否修改...")
        check_and_reload_plugins(plugins)

        for plugin_name, plugin_class in plugins.items():
            print(f"运行插件: {plugin_name}")
            run_plugin(plugin_class)

        # 休眠一段时间，避免频繁检查
        time.sleep(5)

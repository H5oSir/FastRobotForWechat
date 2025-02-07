from pathlib import Path

import yaml


class File:

    def load_config_from_yaml_file(self,path):
        """
        读取path下的 config.json 配置文件。
        """


        # 构建 config.json 的路径
        config_path = path /  "config.yaml"
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
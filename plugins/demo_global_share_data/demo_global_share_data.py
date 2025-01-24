from plugins.plugin import Plugin



class Demo_global_share_data(Plugin):
    """
    这是一个Demo插件，插件的加载到调用完毕算一次生命周期，
    插件内部的变量是无法跨越插件生命周期的，
    需要用到框架的global变量机制，通过wcf进行共享从而跨越生命周期，
    简单理解为：
    1.同一个插件第一次调用存一个值，第二次调用时可以读取到。
    2.第一个插件存一个值，可以让第二个插件读取到，即跨越插件传值。
    类的名称需要与包名一致，否则无法正常加载。
    """
    name = 'Demo_global_share_data'
    def deal_msg(self):
        """
        这里写你的业务处理逻辑，
        过滤器已经将您不需要的消息过滤掉了，
        能到这儿的全是真实有效需要处理的消息 。
        :return:
        """
        #self.wcf.share_data["Demo_global_share_data"]["count"]
        count=self.get_plugin_global_share_data("count")
        if not count:
            count =0
        count=count+1
        print(F"{self.name}插件调用的次数:{count}")
        self.set_plugin_global_share_data("count", count)

        # self.wcf.share_data["Demo_global_share_data"]["count2"]
        if not self.plugin_global_share_data.get("count2"):
            self.plugin_global_share_data["count2"] = 0
        self.plugin_global_share_data["count2"] += 1
        print(F"{self.name}插件调用的次数:{self.plugin_global_share_data['count2']}")

        # self.wcf.share_data["count"]
        if not self.global_share_data.get("count"):
            self.global_share_data["count"] = 0
        self.global_share_data["count"] += 1
        print(F"{self.name}插件调用的次数:{self.global_share_data['count']}")


    def filter_msg(self)->bool:
        """
        黑名单过滤机制，默认通过原则。
        :return:
        """
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

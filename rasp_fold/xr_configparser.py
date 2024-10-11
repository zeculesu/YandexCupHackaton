"""
树莓派WiFi无线视频小车机器人驱动源码
作者：Sence
版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
"""
"""
@version: python3.7
@Author  : xiaor
@Explain :封装配置文件
@contact :
@Time    :2020/05/09
@File    :xr_configparser.py
@Software: PyCharm
"""
from configparser import ConfigParser


class HandleConfig:
    """
    配置文件读写数据的封装
    """
    def __init__(self, filename):
        """
        :param filename: 配置文件名
        """
        self.filename = filename
        self.config = ConfigParser()        # 读取配置文件1.创建配置解析器
        self.config.read(self.filename, encoding="utf-8")   # 读取配置文件2.指定读取的配置文件

    def save_data(self, group, key, data):

        if not self.config.has_section(group):  # 判断section是否存在
            self.config.add_section(group)      # 不存在则添加
        self.config.set(group, key, str(data))  # 修改section
        with open(self.filename, "w") as file:  # 保存到哪个文件filename=需要指定文件名
            self.config.write(file)

    def get_data(self, group, key):
        data = self.get_value(group, key)  # 读取什么内容
        data = str(data)[1:-1].split(',')
        data = list(map(int, data))
        return data

    # get_value获取所有的字符串，section区域名, option选项名
    def get_value(self, section, option):
        return self.config.get(section, option)
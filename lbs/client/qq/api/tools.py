# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class Tools(base.QQMapBaseApi):
    """
    工具
    """
    def district_list(self):
        """
        获取全部行政区划数据
        https://lbs.qq.com/webservice_v1/guide-region.html
        """
        return self._get("/ws/district/v1/list")

    def district_getchildren(self, _id=None):
        """
        获取指定行政区划的子级行政区划
        https://lbs.qq.com/webservice_v1/guide-region.html

        :param _id: 父级行政区划ID
        """
        return self._get("/ws/district/v1/getchildren", optionaldict({'id': _id}))

    def district_search(self, keyword):
        """
        根据关键词搜索行政区划
        https://lbs.qq.com/webservice_v1/guide-region.html

        :param keyword: 搜索关键词
        """
        return self._get("/ws/district/v1/search", {'keyword': keyword})

    def distance(self, _from, to, mode='driving'):
        """
        距离计算(一对多)
        https://lbs.qq.com/webservice_v1/guide-distance.html

        :param _from: 起点坐标
        :param to: 终点坐标
        :param mode: 计算方式
        """
        _from, from_num = self._parse_location(_from)
        to, to_num = self._parse_location(to)
        if from_num == 0 or to_num == 0 or (from_num > 1 and to_num > 1):
            raise ValueError("from和to参数仅可有一个为多坐标")
        return self._get("/ws/distance/v1/", {"from": _from, 'to': to, 'mode': mode})

    def distance_matrix(self, _from, to, mode='driving'):
        """
        距离计算(多对多)
        https://lbs.qq.com/webservice_v1/guide-distancematrix.html

        :param _from: 起点坐标
        :param to: 终点坐标
        :param mode: 计算方式
        """
        _from, _ = self._parse_location(_from)
        to, _ = self._parse_location(to)
        return self._get("/ws/distance/v1/matrix", {"from": _from, 'to': to, 'mode': mode})

    def translate(self, locations, _type=5):
        """
        坐标转换
        https://lbs.qq.com/webservice_v1/guide-convert.html

        :param locations: 预转换的坐标
        :param _type: 输入的locations的坐标类型
        """
        locations, _ = self._parse_location(locations)
        return self._get("/ws/coord/v1/translate", {"locations": locations, 'type': _type})

    def ip(self, ip):
        """
        IP定位
        https://lbs.qq.com/webservice_v1/guide-ip.html

        :param ip: IP地址
        """

        return self._get("/ws/location/v1/ip ", {"ip": ip})

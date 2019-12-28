# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class TrafficStatus(base.AmapBaseApi):
    """
    交通态势
    https://lbs.amap.com/api/webservice/guide/api/trafficstatus
    """

    def rectangle(self, rectangle, level=5, extensions='base'):
        """
        矩形区域交通态势

        :param rectangle: 矩形区域查询
        :param level: 道路等级
        :param extensions: 返回结果控制
        """
        rectangle, num = self._parse_location(rectangle, join_str=';')
        if num != 2:
            raise ValueError("rectangle 解析失败")
        data = optionaldict({
            'rectangle': rectangle,
            'level': level,
            'extensions': extensions,
        })
        return self._get('/v3/traffic/status/rectangle', data, result_processor=lambda x: x['trafficinfo'])

    def circle(self, location, radius=5000, level=5, extensions='base'):
        """

        :param location: 中心点坐标
        :param radius: 半径
        :param level: 道路等级
        :param extensions: 返回结果控制
        """
        location, num = self._parse_location(location, many=False)
        if num != 1:
            raise ValueError("rectangle 解析失败")
        data = optionaldict({
            'location': location,
            'radius': radius,
            'level': level,
            'extensions': extensions,
        })
        return self._get('/v3/traffic/status/circle', data, result_processor=lambda x: x['trafficinfo'])

    def road(self, name, city=None, adcode=None, level=5, extensions='base'):
        """

        :param name:
        :param city:
        :param adcode:
        :param level: 道路等级
        :param extensions: 返回结果控制
        """
        if not city and not adcode:
            raise ValueError("city和adcode必填一个")
        data = optionaldict({
            'name': name,
            'city': city,
            'adcode': adcode,
            'level': level,
            'extensions': extensions,
        })
        return self._get('/v3/traffic/status/road', data, result_processor=lambda x: x['trafficinfo'])

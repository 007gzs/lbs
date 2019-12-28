# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class Geocode(base.AmapBaseApi):
    """
    地理/逆地理编码
    https://lbs.amap.com/api/webservice/guide/api/georegeo
    """

    def geo(self, address, city=None, batch=None):
        """
        地理编码

        :param address: 结构化地址信息
        :param city: 指定查询的城市
        :param batch: 批量查询控制
        """
        if isinstance(address, (list, tuple, set)):
            address = "|".join(address)
            if len(address) > 1 and batch is None:
                batch = True
        data = optionaldict({
            "address": address,
            "city": city,
            "batch": batch,
        })
        return self._get("/v3/geocode/geo", data, result_processor=lambda x: x['geocodes'])

    def regeo(self, location, poitype=None, radius=1000, extensions='base', batch=None, roadlevel=None, homeorcorp=0):
        """
        逆地理编码

        :param location: 经纬度坐标
        :param poitype: 返回附近POI类型
        :param radius: 搜索半径
        :param extensions: 返回结果控制
        :param batch: 批量查询控制
        :param roadlevel: 道路等级
        :param homeorcorp: 是否优化POI返回顺序
        """
        location, num = self._parse_location(location)
        if num == 0:
            raise ValueError("location解析失败")
        if num > 1 and batch is None:
            batch = True
        data = optionaldict({
            "location": location,
            "poitype": poitype,
            "radius": radius,
            "extensions": extensions,
            "batch": batch,
            "roadlevel": roadlevel,
            "homeorcorp": homeorcorp,
        })
        return self._get("/v3/geocode/regeo", data, result_processor=lambda x: x['regeocode'])

# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class Geocoder(base.QQMapBaseApi):
    """
    地理/逆地理编码
    """
    def geocoder(self, address, region=None):
        """
        地理编码
        https://lbs.qq.com/webservice_v1/guide-geocoder.html

        :param address: 地址
        :param region: 指定地址所属城市
        """
        data = optionaldict({
            "address": address,
            "region": region
        })
        return self._get("/ws/geocoder/v1/", data)

    def regeocoder(self, location, get_poi=0, poi_options=None):
        """
        逆地理编码
        https://lbs.qq.com/webservice_v1/guide-gcoder.html

        :param location: 位置坐标
        :param get_poi: 是否返回周边POI列表
        :param poi_options: 用于控制POI列表
        """
        location, num = self._parse_location(location, False)
        if num != 1:
            raise ValueError("location解析失败")
        data = optionaldict({
            "location": location,
            "get_poi": get_poi,
            "poi_options": poi_options
        })
        return self._get("/ws/geocoder/v1/", data)

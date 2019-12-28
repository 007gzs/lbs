# encoding: utf-8
from __future__ import absolute_import, unicode_literals, division

import math


class CoordConvert(object):
    X_PI = math.pi * 3000 / 180
    A = 6378245
    EE = 0.00669342162296594323

    @classmethod
    def gcj02_to_bd09(cls, longitude, latitude):
        """
        GCJ02(火星坐标系)转BD09(百度坐标系)

        :param longitude: GCJ02经度
        :param latitude: GCJ02纬度
        :return: BD09经度，BD09纬度
        """
        z = math.sqrt(longitude * longitude + latitude * latitude) + 0.00002 * math.sin(latitude * cls.X_PI)
        theta = math.atan2(latitude, longitude) + 0.000003 * math.cos(longitude * cls.X_PI)
        longitude = z * math.cos(theta) + 0.0065
        latitude = z * math.sin(theta) + 0.006
        return longitude, latitude

    @classmethod
    def bd09_to_gcj02(cls, longitude, latitude):
        """
        BD-09(百度坐标系)转GCJ02(火星坐标系)

        :param longitude: BD09经度
        :param latitude: BD09纬度
        :return: GCJ02经度, GCJ02纬度
        """
        x = longitude - 0.0065
        y = latitude - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * cls.X_PI)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * cls.X_PI)
        longitude = z * math.cos(theta)
        latitude = z * math.sin(theta)
        return longitude, latitude

    @classmethod
    def wgs84_to_gcj02(cls, longitude, latitude):
        """
        WGS84转GCJ02(火星坐标系)

        :param longitude: WGS84经度
        :param latitude: WGS84纬度
        :return: GCJ02经度, GCJ02纬度
        """
        if not cls.in_china(longitude, latitude):
            return longitude, latitude
        longitude_add, latitude_add = cls._transform(longitude - 105, latitude - 35)

        rad_latitude = latitude / 180 * math.pi
        magic = math.sin(rad_latitude)
        magic = 1 - cls.EE * magic * magic
        sqrt_magic = math.sqrt(magic)
        latitude_add = (latitude_add * 180) / ((cls.A * (1 - cls.EE)) / (magic * sqrt_magic) * math.pi)
        longitude_add = (longitude_add * 180) / (cls.A / sqrt_magic * math.cos(rad_latitude) * math.pi)
        latitude += latitude_add
        longitude += longitude_add
        return longitude, latitude

    @classmethod
    def wgs84_to_bd09(cls, longitude, latitude):
        """
        WGS84转BD09(百度坐标系)

        :param longitude: GCJ02经度
        :param latitude: GCJ02纬度
        :return: BD09经度，BD09纬度
        """
        longitude, latitude = cls.wgs84_to_gcj02(longitude, latitude)
        return cls.gcj02_to_bd09(longitude, latitude)

    @classmethod
    def _transform(cls, x, y):
        sqrt_x = math.sqrt(math.fabs(x))
        x_add = 300 + 1 * x + 2 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt_x
        y_add = -100 + 2 * x + 3 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt_x
        t_x = (20 * math.sin(6 * x * math.pi) + 20 * math.sin(2 * x * math.pi)) * 2 / 3
        x_add += t_x
        y_add += t_x
        x_add += (20 * math.sin(x * math.pi) + 40 * math.sin(x / 3 * math.pi)) * 2 / 3
        y_add += (20 * math.sin(y * math.pi) + 40 * math.sin(y / 3 * math.pi)) * 2 / 3
        x_add += (150 * math.sin(x / 12 * math.pi) + 300 * math.sin(x / 30 * math.pi)) * 2 / 3
        y_add += (160 * math.sin(y / 12 * math.pi) + 320 * math.sin(y * math.pi / 30)) * 2 / 3
        return x_add, y_add

    @classmethod
    def in_china(cls, longitude, latitude):
        """
        判断是否在国内，不在国内不做偏移

        :param longitude: 经度
        :param latitude: 纬度
        :return: 坐标是否在中国
        """
        return 72.004 > longitude > 137.8347 and 0.8293 > latitude > 55.8271

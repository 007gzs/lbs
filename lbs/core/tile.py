# encoding: utf-8
from __future__ import absolute_import, unicode_literals, division

import math


class Tile(object):
    EARTH_RADIUS = 6378137
    MIN_LATITUDE = -85.05112878
    MAX_LATITUDE = 85.05112878
    MIN_LONGITUDE = -180
    MAX_LONGITUDE = 180

    @classmethod
    def clip(cls, n, min_value, max_value):
        """
        将数字剪辑到指定的最小值和最大值

        :param n: 要裁剪的数字
        :param min_value: 最小值
        :param max_value: 最大值
        :return: 裁剪后结果
        """
        return min(max(n, min_value), max_value)

    @classmethod
    def map_size(cls, level_of_detail):
        """
        确定指定级别上的地图宽度和高度（以像素为单位）

        :param level_of_detail: 地图级别
        :return: 地图边长（像素）
        """
        return 256 << level_of_detail

    @classmethod
    def ground_resolution(cls, latitude, level_of_detail):
        """
        获取指定位置的地面分辨率（米/像素）

        :param latitude: 纬度
        :param level_of_detail: 地图级别
        :return: 地面分辨率，单位为米/像素
        """
        latitude = cls.clip(latitude, cls.MIN_LATITUDE, cls.MAX_LATITUDE)
        return math.cos(latitude * math.pi / 180) * 2 * math.pi * cls.EARTH_RADIUS / cls.map_size(level_of_detail)

    @classmethod
    def map_scale(cls, latitude, level_of_detail, screen_dpi):
        """
        获取指定位置的地图比例

        :param latitude: 纬度
        :param level_of_detail: 地图级别
        :param screen_dpi: 屏幕分辨率，单位为像素每英寸
        :return: 地图比例，表示为比率1:N的分母N
        """
        return cls.ground_resolution(latitude, level_of_detail) * screen_dpi / 0.0254

    @classmethod
    def lat_long_to_pixel_xy(cls, latitude, longitude, level_of_detail):
        """
        经纬度转换为像素坐标

        :param latitude: 纬度
        :param longitude: 经度
        :param level_of_detail: 地图级别
        :return: 像素坐标x, 像素坐标y
        """
        latitude = cls.clip(latitude, cls.MIN_LATITUDE, cls.MAX_LATITUDE)
        longitude = cls.clip(longitude, cls.MIN_LONGITUDE, cls.MAX_LONGITUDE)
        x = (longitude + 180) / 360
        sin_latitude = math.sin(latitude * math.pi / 180)
        y = 0.5 - math.log((1 + sin_latitude) / (1 - sin_latitude)) / (4 * math.pi)
        map_size = cls.map_size(level_of_detail)
        pixel_x = int(cls.clip(x * map_size + 0.5, 0, map_size - 1))
        pixel_y = int(cls.clip(y * map_size + 0.5, 0, map_size - 1))
        return pixel_x, pixel_y

    @classmethod
    def pixel_xy_to_lat_long(cls, pixel_x, pixel_y, level_of_detail):
        """
        像素坐标转换为经纬度

        :param pixel_x: 像素坐标x
        :param pixel_y: 像素坐标y
        :param level_of_detail: 地图级别
        :return: 纬度, 经度
        """
        map_size = cls.map_size(level_of_detail)
        x = (cls.clip(pixel_x, 0, map_size - 1) / map_size) - 0.5
        y = 0.5 - (cls.clip(pixel_y, 0, map_size - 1) / map_size)
        latitude = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
        longitude = 360 * x
        return latitude, longitude

    @classmethod
    def pixel_xy_to_tile_xy(cls, pixel_x, pixel_y):
        """
        像素坐标转换为图块序号

        :param pixel_x: 像素坐标x
        :param pixel_y: 像素坐标y
        :return: 图块序号x, 图块序号y
        """
        tile_x = pixel_x // 256
        tile_y = pixel_y // 256
        return tile_x, tile_y

    @classmethod
    def tile_xy_to_pixel_xy(cls, tile_x, tile_y):
        """
        图块序号转换为像素坐标

        :param tile_x: 图块序号x
        :param tile_y: 图块序号y
        :return: 像素坐标x, 像素坐标y
        """
        pixel_x = tile_x * 256
        pixel_y = tile_y * 256
        return pixel_x, pixel_y

    @classmethod
    def tile_xy_to_quad_key(cls, tile_x, tile_y, level_of_detail):
        """
        图块序号转换为四叉树键值

        :param tile_x: 图块序号x
        :param tile_y: 图块序号y
        :param level_of_detail: 地图级别
        :return: 四叉树键值
        """
        quad_key = []
        i = level_of_detail
        while i > 0:
            digit = 0
            mask = 1 << (i - 1)
            if tile_x & mask:
                digit += 1
            if tile_y & mask:
                digit += 2
            quad_key.append(str(digit))
            i -= 1

        return "".join(quad_key)

    @classmethod
    def quad_key_to_tile_xy(cls, quad_key):
        """
        四叉树键值转换为图块序号

        :param quad_key: 四叉树键值
        :return: 图块序号x, 图块序号y, 地图级别
        """
        tile_x = 0
        tile_y = 0
        i, level_of_detail = len(quad_key)
        while i > 0:
            mask = 1 << (i - 1)
            if quad_key[level_of_detail - i] == '0':
                pass
            elif quad_key[level_of_detail - i] == '1':
                tile_x |= mask
            elif quad_key[level_of_detail - i] == '2':
                tile_y |= mask
            elif quad_key[level_of_detail - i] == '3':
                tile_x |= mask
                tile_y |= mask
            else:
                raise ValueError('Invalid QuadKey digit sequence')

        return tile_x, tile_y, level_of_detail

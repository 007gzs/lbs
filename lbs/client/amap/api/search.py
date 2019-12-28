# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class Search(base.AmapBaseApi):
    """
    搜索POI
    https://lbs.amap.com/api/webservice/guide/api/search
    """

    def text(self, keywords=None, types=None, city=None, citylimit=False,
             children=0, offset=20, page=1, extensions='base'):
        """
        关键字搜索

        :param keywords: 查询关键字
        :param types: 查询POI类型
        :param city: 查询城市
        :param citylimit: 仅返回指定城市数据
        :param children: 是否按照层级展示子POI数据
        :param offset: 每页记录数据
        :param page: 当前页数
        :param extensions: 返回结果控制
        """
        if not keywords and not types:
            raise ValueError("keywords和types两者至少必选其一")
        data = optionaldict({
            'keywords': keywords,
            'types': types,
            'city': city,
            'citylimit': citylimit,
            'children': children,
            'offset': offset,
            'page': page,
            'extensions': extensions,
        })
        return self._get("/v3/place/text", data)

    def around(self, location, radius=3000, sortrule='distance', keywords=None, types=None, city=None,
               offset=20, page=1, extensions='base'):
        """
        周边搜索

        :param location: 中心点坐标
        :param radius: 查询半径
        :param sortrule: 排序规则
        :param keywords: 查询关键字
        :param types: 查询POI类型
        :param city: 查询城市
        :param offset: 每页记录数据
        :param page: 当前页数
        :param extensions: 返回结果控制
        """
        location, num = self._parse_location(location, False)
        if num != 1:
            raise ValueError("location解析失败")
        data = optionaldict({
            'location': location,
            'radius': radius,
            'sortrule': sortrule,
            'keywords': keywords,
            'types': types,
            'city': city,
            'offset': offset,
            'page': page,
            'extensions': extensions,
        })
        return self._get("/v3/place/around", data)

    def polygon(self, polygon, keywords=None, types=None, city=None, offset=20, page=1, extensions='base'):
        """
        多边形搜索

        :param polygon: 经纬度坐标对
        :param keywords: 查询关键字
        :param types: 查询POI类型
        :param city: 查询城市
        :param offset: 每页记录数据
        :param page: 当前页数
        :param extensions: 返回结果控制
        """
        polygon, num = self._parse_location(polygon, False)
        if num <= 1:
            raise ValueError("polygon")
        data = optionaldict({
            'polygon': polygon,
            'keywords': keywords,
            'types': types,
            'city': city,
            'offset': offset,
            'page': page,
            'extensions': extensions,
        })
        return self._get("/v3/place/polygon", data)

    def detail(self, _id):
        """
        ID查询

        :param _id: 兴趣点ID
        """
        return self._get("/v3/place/detail", {"id": _id})

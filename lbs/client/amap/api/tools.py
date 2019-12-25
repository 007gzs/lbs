# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class Tools(base.AmapBaseApi):
    """
    工具
    """

    def district(self, keywords=None, subdistrict=1, page=1, offset=20, extensions="base", filter=None):
        """
        行政区域查询
        https://lbs.amap.com/api/webservice/guide/api/district

        :param keywords: 查询关键字
        :param subdistrict: 子级行政区
        :param page: 需要第几页数据
        :param offset: 最外层返回数据个数
        :param extensions: 返回结果控制
        :param filter: 根据区划过滤
        """
        data = optionaldict({
            'keywords': keywords,
            'subdistrict': subdistrict,
            'page': page,
            'offset': offset,
            'extensions': extensions,
            'filter': filter,
        })
        return self._get("/v3/config/district", data)

    def ip(self, ip):
        """

        :param ip: ip地址
        :return:
        """
        return self._get("/v3/config/district", {'ip': ip})

    def convert(self, locations, coordsys="autonavi"):
        """
        坐标转换
        https://lbs.amap.com/api/webservice/guide/api/convert

        :param locations: 坐标点
        :param coordsys: 原坐标系
        """
        locations, num = self._parse_location(locations)
        assert 0 < num <= 40, "坐标点解析失败"
        data = optionaldict({
            'locations': locations,
            'coordsys': coordsys,
        })
        return self._get("/v3/assistant/coordinate/convert", data, result_processor=lambda x: x['locations'].split(";"))

    def inputtips(self, keywords, type=None, location=None, city=None, citylimit=False, datatype='all'):
        """
        输入提示
        https://lbs.amap.com/api/webservice/guide/api/inputtips

        :param keywords: 查询关键词
        :param type: POI分类
        :param location: 坐标
        :param city: 搜索城市
        :param citylimit: 仅返回指定城市数据
        :param datatype: 返回的数据类型
        """
        location, _ = self._parse_location(location, False)
        data = optionaldict({
            'keywords': keywords,
            'type': type,
            'location': location,
            'city': city,
            'citylimit': 'true' if citylimit else 'false',
            'datatype': datatype,
        })
        return self._get("/v3/assistant/inputtips", data)

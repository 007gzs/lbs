# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class Tools(base.AmapBaseApi):
    """
    工具
    """

    def district(self, keywords=None, subdistrict=1, page=1, offset=20, extensions="base", _filter=None):
        """
        行政区域查询
        https://lbs.amap.com/api/webservice/guide/api/district

        :param keywords: 查询关键字
        :param subdistrict: 子级行政区
        :param page: 需要第几页数据
        :param offset: 最外层返回数据个数
        :param extensions: 返回结果控制
        :param _filter: 根据区划过滤
        """
        data = optionaldict({
            'keywords': keywords,
            'subdistrict': subdistrict,
            'page': page,
            'offset': offset,
            'extensions': extensions,
            'filter': _filter,
        })
        return self._get("/v3/config/district", data)

    def ip(self, ip):
        """
        IP定位
        https://lbs.amap.com/api/webservice/guide/api/ipconfig

        :param ip: ip地址
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
        if not 0 < num <= 40:
            raise ValueError("坐标点解析失败")
        data = optionaldict({
            'locations': locations,
            'coordsys': coordsys,
        })
        return self._get("/v3/assistant/coordinate/convert", data, result_processor=lambda x: x['locations'].split(";"))

    def inputtips(self, keywords, _type=None, location=None, city=None, citylimit=False, datatype='all'):
        """
        输入提示
        https://lbs.amap.com/api/webservice/guide/api/inputtips

        :param keywords: 查询关键词
        :param _type: POI分类
        :param location: 坐标
        :param city: 搜索城市
        :param citylimit: 仅返回指定城市数据
        :param datatype: 返回的数据类型
        """
        location, _ = self._parse_location(location, False)
        data = optionaldict({
            'keywords': keywords,
            'type': _type,
            'location': location,
            'city': city,
            'citylimit': 'true' if citylimit else 'false',
            'datatype': datatype,
        })
        return self._get("/v3/assistant/inputtips", data)

    def static_map(
            self, zoom, location=None, size=(400, 400), scale=1, markers=None, labels=None, paths=None, traffic=0
    ):
        """
        静态地图
        https://lbs.amap.com/api/webservice/guide/api/staticmaps

        :param zoom: 地图级别
        :param location: 地图中心点
        :param size: 地图大小
        :param scale: 普通/高清
        :param markers: 标注
        :param labels: 标签
        :param paths: 折线
        :param traffic: 交通路况标识
        :return: 静态地图对应URl
        """
        data = optionaldict({
            'zoom': zoom,
            'location': location,
            'size': size,
            'scale': scale,
            'markers': markers,
            'labels': labels,
            'paths': paths,
            'traffic': traffic
        })
        return self._gen_get_url('/v3/staticmap', params=data)

    def weather(self, city):
        """
        天气查询
        https://lbs.amap.com/api/webservice/guide/api/weatherinfo

        :param city: 城市编码
        """
        return self._gen_get_url('/v3/staticmap', params={'city': city})

    def grasproad(self, data=()):
        """
        轨迹纠偏
        https://lbs.amap.com/api/webservice/guide/api/grasproad

        :param data: body数据
        """
        return self._post('/v4/grasproad/driving', json=data)

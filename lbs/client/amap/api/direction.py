# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class Direction(base.AmapBaseApi):
    """
    路径规划
    https://lbs.amap.com/api/webservice/guide/api/direction
    """

    def walking(self, origin, destination):
        """
        步行路径规划

        :param origin: 出发点
        :param destination: 目的地
        """
        origin, num = self._parse_location(origin, False)
        if num != 1:
            raise ValueError("出发点解析失败")
        destination, num = self._parse_location(destination, False)
        if num != 1:
            raise ValueError("目的地解析失败")
        data = optionaldict({
            "origin": origin,
            "destination": destination,
        })
        self._get("/v3/direction/walking", data)

    def transit_integrated(self, origin, destination, city, cityd=None, extensions="base",
                           strategy=0, nightflag=0, date=None, time=None):
        """
        公交路径规划

        :param origin: 出发点
        :param destination: 目的地
        :param city: 城市/跨城规划时的起点城市
        :param cityd: 跨城公交规划时的终点城市
        :param extensions: 返回结果详略
        :param strategy: 公交换乘策略
        :param nightflag: 是否计算夜班车
        :param date: 出发日期
        :param time: 出发时间
        """
        origin, num = self._parse_location(origin, False)
        if num != 1:
            raise ValueError("出发点解析失败")
        destination, num = self._parse_location(destination, False)
        if num != 1:
            raise ValueError("目的地解析失败")
        data = optionaldict({
            'origin': origin,
            'destination': destination,
            'city': city,
            'cityd': cityd,
            'extensions': extensions,
            'strategy': strategy,
            'nightflag': nightflag,
            'date': date,
            'time': time,
        })
        return self._get("/v3/direction/transit/integrated", data)

    def driving(self, origin, destination, originid=None, destinationid=None, origintype=None, destinationtype=None,
                strategy=0, waypoints=None, avoidpolygons=None, avoidroad=None, province=None, number=None,
                cartype=0, ferry=0, roadaggregation=False, nosteps=0, extensions='base'):
        """
        驾车路径规划

        :param origin: 出发点
        :param destination: 目的地
        :param originid: 出发点poiid
        :param destinationid: 目的地poiid
        :param origintype: 起点的poi类别
        :param destinationtype: 终点的poi类别
        :param strategy: 驾车选择策略
        :param waypoints: 途经点
        :param avoidpolygons: 避让区域
        :param avoidroad: 避让道路名
        :param province: 用汉字填入车牌省份缩写，用于判断是否限行
        :param number: 填入除省份及标点之外，车牌的字母和数字（需大写）。用于判断限行相关。
        :param cartype: 车辆类型
        :param ferry: 在路径规划中，是否使用轮渡
        :param roadaggregation: 是否返回路径聚合信息
        :param nosteps: 是否返回steps字段内容
        :param extensions: 返回结果控制
        """
        origin, num = self._parse_location(origin, False)
        if not 0 < num <= 3:
            raise ValueError("出发点解析失败")
        destination, num = self._parse_location(destination, False)
        if num != 1:
            raise ValueError("目的地解析失败")
        data = optionaldict({
            'origin': origin,
            'destination': destination,
            'originid': originid,
            'destinationid': destinationid,
            'origintype': origintype,
            'destinationtype': destinationtype,
            'strategy': strategy,
            'waypoints': waypoints,
            'avoidpolygons': avoidpolygons,
            'avoidroad': avoidroad,
            'province': province,
            'number': number,
            'cartype': cartype,
            'ferry': ferry,
            'roadaggregation': 'true' if roadaggregation else 'false',
            'nosteps': nosteps,
            'extensions': extensions,
        })

        return self._get("/v3/direction/driving", data)

    def bicycling(self, origin, destination, ):
        pass

    def truck(self, origin, destination, ):
        pass

    def distance(self, origin, destination, ):
        pass

# encoding: utf-8
from __future__ import absolute_import, unicode_literals, division

from optionaldict import optionaldict

from lbs.core import model
from . import base


class Direction(base.QQMapBaseApi):
    """
    路线规划
    https://lbs.qq.com/webservice_v1/guide-road.html
    """
    def driving(self, _from, to, from_poi=None, heading=None, speed=None, accuracy=None, road_type=0, from_track=None,
                to_poi=None, waypoints=None, policy=None, plate_number=None, cartype=0):
        """
        驾车路线规划

        :param _from: 起点位置坐标
        :param to: 终点位置坐标
        :param from_poi: 起点POI ID
        :param heading: 在起点位置时的车头方向
        :param speed: 速度
        :param accuracy: 定位精度
        :param road_type: 起点道路类型
        :param from_track: 起点轨迹
        :param to_poi: 终点POI ID
        :param waypoints: 途经点
        :param policy: 策略参数
        :param plate_number: 车牌号
        :param cartype: 车辆类型
        """
        _from, num = self._parse_location(_from, False)
        if num != 1:
            raise ValueError("起点位置坐标解析失败")
        to, num = self._parse_location(to, False)
        if num != 1:
            raise ValueError("终点位置坐标解析失败")
        waypoints, _ = self._parse_location(waypoints)
        data = optionaldict({
            'from': _from,
            'to': to,
            'from_poi': from_poi,
            'heading': heading,
            'speed': speed,
            'accuracy': accuracy,
            'road_type': road_type,
            'from_track': from_track,
            'to_poi': to_poi,
            'waypoints': waypoints,
            'policy': policy,
            'plate_number': plate_number,
            'cartype': cartype,
        })
        return self._get("/ws/direction/v1/driving/", data)

    def walking(self, _from, to):
        """
        步行路线规划

        :param _from: 起点位置坐标
        :param to: 终点位置坐标
        """
        _from, num = self._parse_location(_from, False)
        if num != 1:
            raise ValueError("起点位置坐标解析失败")
        to, num = self._parse_location(to, False)
        if num != 1:
            raise ValueError("终点位置坐标解析失败")
        return self._get("/ws/direction/v1/walking/", {'from': _from, 'to': to})

    def bicycling(self, _from, to):
        """
        骑行路线规划

        :param _from: 起点位置坐标
        :param to: 终点位置坐标
        """
        _from, num = self._parse_location(_from, False)
        if num != 1:
            raise ValueError("起点位置坐标解析失败")
        to, num = self._parse_location(to, False)
        if num != 1:
            raise ValueError("终点位置坐标解析失败")
        return self._get("/ws/direction/v1/bicycling/", {'from': _from, 'to': to})

    def transit(self, _from, to, departure_time=None, policy=None):
        """
        公交路线规划

        :param _from: 起点位置坐标
        :param to: 终点位置坐标
        :param departure_time: 出发时间
        :param policy: 路线规划优先条件
        """
        _from, num = self._parse_location(_from, False)
        if num != 1:
            raise ValueError("起点位置坐标解析失败")
        to, num = self._parse_location(to, False)
        if num != 1:
            raise ValueError("终点位置坐标解析失败")
        data = optionaldict({
            'from': _from,
            'to': to,
            'departure_time': departure_time,
            'policy': policy,
        })
        return self._get("/ws/direction/v1/transit/", data)

    def polyline_to_location(self, coors):
        """
        polyline 坐标解压

        :param coors: polyline的坐标串
        """
        if len(coors) % 2 != 0:
            raise ValueError("坐标串错误")
        ret = list()
        last = None
        for i in range(0, len(coors) // 2):
            if last is None:
                last = model.LbsLocation(coors[i], coors[i + 1])
            else:
                last = model.LbsLocation(last.longitude + coors[i] / 1000000, last.latitude + coors[i + 1] / 1000000)
            ret.append(last)

        return ret

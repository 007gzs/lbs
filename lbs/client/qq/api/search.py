# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from . import base


class Search(base.QQMapBaseApi):
    """
    搜索
    """
    def gen_region_boundary(self, city_name, auto_extend=1, location=None):
        """
        指定地区名称

        :param city_name: 检索区域名称
        :param auto_extend: 当前城市搜索无结果，是否自动扩大范围
        :param location: 泛关键词搜索中心
        """
        location, _ = self._parse_location(location, False)
        if location:
            location = "," + location
        else:
            location = ""
        return "region(%s,%s%s)" % (city_name, auto_extend, location)

    def gen_nearby_boundary(self, location, radius, auto_extend=1):
        """
        周边搜索

        :param location: 中心坐标
        :param radius: 半径/米
        :param auto_extend: 当前范围无结果时，是否自动扩大范围
        """
        location, num = self._parse_location(location, False)
        if num != 1:
            raise ValueError("location解析失败")
        return "nearby(%s,%s,%s)" % (location, radius, auto_extend)

    def gen_rectangle_boundary(self, location_lb, location_rt):
        """
        矩形搜索

        :param location_lb: 左下/西南 坐标
        :param location_rt: 右上/东北 坐标
        """
        location_lb, num = self._parse_location(location_lb, False)
        if num != 1:
            raise ValueError("location_lb解析失败")
        location_rt, num = self._parse_location(location_rt, False)
        if num != 1:
            raise ValueError("location_rt解析失败")
        return "rectangle(%s,%s)" % (location_lb, location_rt)

    def search(self, keyword, boundary, _filter=None, orderby=None, page_size=20, page_index=1):
        """
        地点搜索
        https://lbs.qq.com/webservice_v1/guide-search.html

        :param keyword: 关键字
        :param boundary: 搜索地理范围（gen_xxx_boundary）
        :param _filter: 筛选条件
        :param orderby: 排序
        :param page_size: 每页条目数
        :param page_index: 页码
        """
        data = optionaldict({
            'keyword': keyword,
            'boundary': boundary,
            'filter': _filter,
            'orderby': orderby,
            'page_size': page_size,
            'page_index': page_index,
        })
        return self._get("/ws/place/v1/search/", data)

    def suggestion(self, keyword, region, region_fix=0, location=None, get_subpois=0, policy=0, _filter=None,
                   address_format=None, page_index=1, page_size=20):
        """
        关键词输入提示
        https://lbs.qq.com/webservice_v1/guide-suggestion.html

        :param keyword: 关键词
        :param region: 限制城市范围
        :param region_fix: 是否固定在当前城市
        :param location: 定位坐标
        :param get_subpois: 是否返回子地点
        :param policy: 检索策略
        :param _filter: 筛选条件
        :param address_format: 返回地址格式
        :param page_index: 页码
        :param page_size: 每页条数
        """
        location, _ = self._parse_location(location, False)
        data = optionaldict({
            'keyword': keyword,
            'region': region,
            'region_fix': region_fix,
            'location': location,
            'get_subpois': get_subpois,
            'policy': policy,
            'filter': _filter,
            'address_format': address_format,
            'page_index': page_index,
            'page_size': page_size,
        })
        return self._get("/ws/place/v1/suggestion/", data)

# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from lbs.client.base import BaseClient
from lbs.core import model, utils

from . import api


class QQMapClient(BaseClient):

    API_BASE_URL = "https://apis.map.qq.com/"
    search = api.Search()
    tools = api.Tools()
    geocoder = api.Geocoder()
    direction = api.Direction()

    def __init__(self, key, timeout=None):
        """
        qq地图服务

        :param key: qq地图 Key
        :param timeout: 请求过期时间
        """
        super(QQMapClient, self).__init__(timeout)
        self.key = key

    def _handle_pre_request(self, method, uri, kwargs):
        kwargs.setdefault("params", dict())
        kwargs['params']['key'] = self.key
        return method, uri, kwargs

    def _handle_result(self, res, method=None, url=None, **kwargs):
        result = super(QQMapClient, self)._handle_result(res, method=method, url=url, **kwargs)
        if not isinstance(result, dict):
            return result
        result = self._parse_error_code(url, kwargs, res, result, 'message', 'status', 0, code_type=int)
        result = result.get('result', result)
        return result

    @classmethod
    def parse_location(cls, location, many=True, join_str="|"):
        if not location:
            return location, 0
        if isinstance(location, model.LbsLocation):
            return "%s,%s" % (location.latitude, location.longitude), 1
        elif isinstance(location, (list, tuple)):
            if len(location) == 2 and not isinstance(location[0], (list, tuple)):
                return "%s,%s" % tuple(location), 1
            elif many:
                locations = list()
                for loc in location:
                    l, num = cls.parse_location(loc, False)
                    if num > 0:
                        locations.append(l)
                return join_str.join(locations), len(locations)
        return utils.to_text(location), 1

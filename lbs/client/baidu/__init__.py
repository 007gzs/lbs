# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from lbs.client.base import BaseClient


class BaiduMapClient(BaseClient):

    API_BASE_URL = "http://api.map.baidu.com/"

    def __init__(self, ak, sk=None, timeout=None):
        """
        百度地图服务

        :param ak: 百度地图 ak
        :param sk: 百度地图 sk
        :param timeout: 请求过期时间
        """
        super(BaiduMapClient, self).__init__(timeout)
        self.ak = ak
        self.sk = sk

    def _handle_pre_request(self, method, uri, kwargs):
        kwargs.setdefault("params", dict())
        kwargs['params']['ak'] = self.ak
        return method, uri, kwargs

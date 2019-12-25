# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from lbs.client.base import BaseClient


class QQMapClient(BaseClient):

    API_BASE_URL = "https://apis.map.qq.com/"

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

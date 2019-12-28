# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import hashlib
from six.moves.urllib.parse import urlencode, quote
from collections import OrderedDict

from lbs.client.base import BaseClient
from lbs.core.utils import to_binary


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

    def _calc_sn(self, data, uri):
        if isinstance(data, dict):
            data = urlencode(data)
        encode_str = "%s?%s%s" % (uri, data, self.sk)
        return hashlib.md5(to_binary(quote(encode_str))).hexdigest()

    def _handle_pre_request(self, method, uri, kwargs):
        if 'data' in kwargs and isinstance(kwargs['data'], dict):
            kwargs['data']['ak'] = self.ak
            if self.sk:
                kwargs['data'] = OrderedDict(sorted(kwargs['data'].items()))
                kwargs['data']['sn'] = self._calc_sn(uri, kwargs['data'])
        else:
            kwargs.setdefault("params", dict())
            kwargs['params']['ak'] = self.ak
            if self.sk:
                params = kwargs.pop("params", dict())
                query_string = urlencode(params)
                sn = self._calc_sn(uri, query_string)
                uri += '?' + urlencode(params) + '&sn=' + sn

        return method, uri, kwargs

    def _handle_result(self, res, method=None, url=None, **kwargs):
        result = super(BaiduMapClient, self)._handle_result(res, method=method, url=url, **kwargs)
        result = self._parse_error_code(url, kwargs, res, result, 'message', 'status', 0, code_type=int)
        return result

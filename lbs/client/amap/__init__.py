# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from lbs.core import utils, model
from lbs.core.exceptions import LbsClientException
from lbs.client.base import BaseClient
from . import api


class AmapClient(BaseClient):

    API_BASE_URL = "https://restapi.amap.com/"

    geocode = api.Geocode()
    direction = api.Direction()
    search = api.Search()
    traffic_status = api.TrafficStatus()
    tools = api.Tools()

    def __init__(self, key, sig_key=None, timeout=None):
        """
        高德地图服务

        :param key: 高德地图 Key
        :param sig_key: 高德地图私钥
        :param timeout: 请求过期时间
        """
        super(AmapClient, self).__init__(timeout)
        self.key = key
        self.sig_key = sig_key

    def _handle_pre_request(self, method, uri, kwargs):
        kwargs.setdefault("params", dict())
        kwargs['params']['key'] = self.key
        if self.sig_key:
            kwargs['params']['sig'] = self.get_sig(**kwargs['params'])
        return method, uri, kwargs

    def _handle_result(self, res, method=None, url=None, **kwargs):
        result = super(AmapClient, self)._handle_result(res, method=method, url=url, **kwargs)
        if not isinstance(result, dict):
            return result
        if 'status' in result:
            result['status'] = int(result['status'])

        if 'status' in result and result['status'] != 1:
            errcode = result.get('infocode', result['status'])
            errmsg = result.get('info', errcode)

            self.get_logger().error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                                    url, kwargs.get('params', ''), kwargs.get('data', ''), result)
            raise LbsClientException(
                errcode,
                errmsg,
                client=self,
                request=res.request,
                response=res
            )

        return result

    def get_sig(self, **params):
        signer = utils.LbsMd5Signer(delimiter=b'&', key=self.sig_key)
        for k, v in params.items():
            signer.add_data("%s=%s" % (k, v))
        return signer.signature

    @classmethod
    def parse_location(cls, location, many=True, join_str="|"):
        if not location:
            return location, 0
        if isinstance(location, model.LbsLocation):
            return "%s,%s" % (location.longitude, location.latitude), 1
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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
import json
import logging
import requests
from six.moves.urllib.parse import urljoin, urlencode

from lbs.core.exceptions import LbsClientException
from lbs.core.utils import json_loads

logger = logging.getLogger(__name__)


class LbsBaseAPI(object):

    API_BASE_URL = None

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, params=None, **kwargs):
        if self.API_BASE_URL and 'api_base_url' not in kwargs:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, params, **kwargs)

    def _post(self, url, data=None, params=None, **kwargs):
        if self.API_BASE_URL and 'api_base_url' not in kwargs:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, data, params, **kwargs)

    def _gen_get_url(self, url, **kwargs):
        if self.API_BASE_URL and 'api_base_url' not in kwargs:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.gen_get_url(url, **kwargs)


def _is_api_endpoint(obj):
    return isinstance(obj, LbsBaseAPI)


class BaseClient(object):

    _http = requests.Session()

    API_BASE_URL = None

    def __new__(cls, *args, **kwargs):
        self = super(BaseClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, timeout=None):
        self.timeout = timeout

    def get_logger(self):
        return logger

    def gen_get_url(self, url, **kwargs):
        url = self._real_url(url, kwargs)
        _, url, kwargs = self._handle_pre_request('get', url, kwargs)
        if "params" not in kwargs:
            return url
        if "?" not in url:
            return url + "?" + urlencode(kwargs["params"])
        if not url.endswith("&"):
            url += "&"
        url += urlencode(kwargs["params"])
        return url

    def _real_url(self, url_or_endpoint, kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = urljoin(api_base_url, url_or_endpoint)
        else:
            url = url_or_endpoint
        return url

    def _request(self, method, url_or_endpoint, **kwargs):
        url = self._real_url(url_or_endpoint, kwargs)
        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs.get('data', ''), (dict, list, tuple)):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Content-Type'] = 'application/json'

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            self.get_logger().error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【异常信息】：%s",
                                    url, kwargs.get('params', ''), kwargs.get('data', ''), reqe)
            raise LbsClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )

        result = self._handle_result(res, method, url, **kwargs)
        if result_processor is not None:
            result = result_processor(result)

        self.get_logger().debug("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【响应数据】：%s",
                                url, kwargs.get('params', ''), kwargs.get('data', ''), result)
        return result

    def _decode_result(self, res):
        try:
            result = json_loads(res.content.decode('utf-8', 'ignore'), strict=False)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            self.get_logger().debug('Can not decode response as JSON', exc_info=True)
            return res
        return result

    def _handle_result(self, res, method=None, url=None, **kwargs):
        if not isinstance(res, dict):
            # Dirty hack around asyncio based AsyncWeChatClient
            result = self._decode_result(res)
        else:
            result = res
        return result

    def _handle_pre_request(self, method, uri, kwargs):
        return method, uri, kwargs

    def _handle_request_except(self, e, func, *args, **kwargs):
        raise e

    def request(self, method, uri, **kwargs):
        method, uri_with_key, kwargs = self._handle_pre_request(method, uri, kwargs)
        try:
            return self._request(method, uri_with_key, **kwargs)
        except LbsClientException as e:
            return self._handle_request_except(e, self.request, method, uri, **kwargs)

    def get(self, uri, params=None, **kwargs):
        """
        get 接口请求

        :param uri: 请求url
        :param params: get 参数（dict 格式）
        """
        if params is not None:
            kwargs['params'] = params
        return self.request('GET', uri, **kwargs)

    def post(self, uri, data=None, params=None, **kwargs):
        """
        post 接口请求

        :param uri: 请求url
        :param data: post 数据（dict 格式会自动转换为json）
        :param params: post接口中url问号后参数（dict 格式）
        """
        if data is not None:
            kwargs['data'] = data
        if params is not None:
            kwargs['params'] = params
        return self.request('POST', uri, **kwargs)

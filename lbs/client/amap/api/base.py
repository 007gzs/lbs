# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from lbs.client.base import LbsBaseAPI


class AmapBaseApi(LbsBaseAPI):

    API_BASE_URL = None

    def __init__(self, client=None):
        super(AmapBaseApi, self).__init__(client)

    def _parse_location(self, location, many=True, join_str="|"):
        return self._client.parse_location(location, many, join_str)

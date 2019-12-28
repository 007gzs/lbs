qq地图
===========================================

.. module:: lbs.client.qq

.. autoclass:: QQMapClient
   :members:
   :inherited-members:

`QQMapClient` 基本使用方法::

   from lbs import QQMapClient

   client = QQMapClient('key')

   client.geocoder.geocoder("北京")

.. toctree::
   :maxdepth: 2
   :glob:

   qq/*


高德地图
===========================================

.. module:: lbs.client.amap

.. autoclass:: AmapClient
   :members:
   :inherited-members:

`AmapClient` 基本使用方法::

   from lbs import AmapClient

   client = AmapClient('key')

   client.geocode.geo("北京")


.. toctree::
   :maxdepth: 2
   :glob:

   amap/*


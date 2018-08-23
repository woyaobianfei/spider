# -*- coding:utf-8 -*-
from iqiyi.spiders.mysql import mysql


class executesql:

    # 查出所有影视名称
    def queryTitleList(self):
        sql = "SELECT title from flnet_cms_media.media_drama;"
        return mysql().queryOperation(sql)

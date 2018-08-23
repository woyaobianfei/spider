# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IqiyiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    city_play_data = scrapy.Field()

    play_device_distribution = scrapy.Field()

    video_play_trend_7_days = scrapy.Field()

    video_play_trend_30_days = scrapy.Field()

    video_play_trend_90_days = scrapy.Field()

    video_play_trend_180_days = scrapy.Field()

    video_play_trend_all_days = scrapy.Field()

    star_look = scrapy.Field()

    view_of_public_opinion = scrapy.Field()

    audience_portrait = scrapy.Field()
    pass


class DeviceDistributionItem(scrapy.Item):

    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # PC端播放占比
    pc_device_distribution = scrapy.Field()
    # 移动端播放占比
    mobile_terminal_distribution = scrapy.Field()


class PlayTrend7DaysItem(scrapy.Item):

    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 播放日期
    playtime = scrapy.Field()
    # 播放量
    data = scrapy.Field()


class PlayTrend30DaysItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 播放日期
    playtime = scrapy.Field()
    # 播放量
    data = scrapy.Field()


class PlayTrend90DaysItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 播放日期
    playtime = scrapy.Field()
    # 播放量
    data = scrapy.Field()


class PlayTrend180DaysItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 播放日期
    playtime = scrapy.Field()
    # 播放量
    data = scrapy.Field()


class PlayTrendAllDaysItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 播放日期
    playtime = scrapy.Field()
    # 播放量
    data = scrapy.Field()


class StarLookItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 明星集数，出场时长单位，明星名称数据集合
    data = scrapy.Field()


class ViewOfPublicOpinionItem(scrapy.Item):
    key_name = scrapy.Field()
    # name = scrapy.Field()
    aid = scrapy.Field()
    # 观影舆情详细数据
    data = scrapy.Field()


class AudienceAgeItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 年龄分布数据
    age_data_name = scrapy.Field()
    age_data_value = scrapy.Field()


class AudienceSexItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 性别分布数据
    sex_data_name = scrapy.Field()
    sex_data_value = scrapy.Field()


class AudienceConstellationItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 星座分布数据
    constellation_data_name = scrapy.Field()
    constellation_data_value = scrapy.Field()


class AudienceEducationItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 学历分布数据
    education_data_name = scrapy.Field()
    education_data_value = scrapy.Field()


class AudienceInterestItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 兴趣分布数据
    interest_data_name = scrapy.Field()
    interest_data_value = scrapy.Field()


class CityPlayDataItem(scrapy.Item):
    key_name = scrapy.Field()
    name = scrapy.Field()
    aid = scrapy.Field()
    # 地域播放分布数据
    data = scrapy.Field()


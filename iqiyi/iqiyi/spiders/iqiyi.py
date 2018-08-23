# -*- coding: utf-8 -*-
import string
import time

import requests
import scrapy
import urllib
import json
import urllib3
import urllib.request as urlrequest
from urllib.parse import quote
from scrapy.http import Request
from urllib import parse

from iqiyi.items import IqiyiItem
from iqiyi.items import DeviceDistributionItem
from iqiyi.items import PlayTrend7DaysItem
from iqiyi.items import PlayTrend30DaysItem
from iqiyi.items import PlayTrend90DaysItem
from iqiyi.items import PlayTrend180DaysItem
from iqiyi.items import PlayTrendAllDaysItem
from iqiyi.items import StarLookItem
from iqiyi.items import ViewOfPublicOpinionItem
from iqiyi.items import AudienceAgeItem
from iqiyi.items import AudienceConstellationItem
from iqiyi.items import AudienceEducationItem
from iqiyi.items import AudienceInterestItem
from iqiyi.items import AudienceSexItem
from iqiyi.items import CityPlayDataItem
from iqiyi.pipelines import IqiyiPipeline
from iqiyi.spiders.executesql import executesql


class IqiyiSpider(scrapy.Spider):
    name = 'iqiyi_index'
    # allowed_domains = ['index.iqiyi.com', 'uaa.if.iqiyi.com', 'sentiment.if.iqiyi.com']
    # start_urls = ['http://index.iqiyi.com/']

    def start_requests(self):
        # 每次请求详情之前先通过名称获取aid
        # step 1
        # 抓取网页内容-发送报头-1
        # 循环遍历电影列表
        titlelist = executesql().queryTitleList()
        print("剧集数为： " + str(len(titlelist)))
        aidset = set()
        for title in titlelist:
            title = str(title[0])
            title = title.replace('[', ' ').replace(']', ' ')
            search_for_aid_url = 'https://uaa.if.iqiyi.com/video_index/v2/filtered_suggest_album?key=' + title + '&platform=11&rltnum=10'
            yield Request(search_for_aid_url, callback=self.parse_add_aid)

    def parse_add_aid(self, response):
        jsondata = json.loads(response.text)
        if len(jsondata['data']) > 0:
            aid = jsondata['data'][0]['aid']
            aid = str(aid)
            # 播放地域分布
            city_play_data = 'https://uaa.if.iqiyi.com/video_index/v2/get_province_distribution?album_id=' + aid
            yield Request(url=parse.urljoin(response.url, city_play_data), callback=self.parse_city_play_data_detail)

            # 播放设备分布
            play_device_distribution = 'https://uaa.if.iqiyi.com/video_index/v2/get_platform_distribution?album_id=' + aid
            yield Request(url=parse.urljoin(response.url, play_device_distribution), callback=self.parse_play_device_distribution_detail)

            # 视频播放趋势-最近7天
            video_play_trend_7_days = 'https://uaa.if.iqiyi.com/video_index/v2/get_index_trend?album_id=' + aid + '&time_window=7'
            yield Request(url=parse.urljoin(response.url, video_play_trend_7_days), callback=self.parse_video_play_trend_7_days_detail)

            # 视频播放趋势-最近30天
            video_play_trend_30_days = 'https://uaa.if.iqiyi.com/video_index/v2/get_index_trend?album_id=' + aid + '&time_window=30'
            yield Request(url=parse.urljoin(response.url, video_play_trend_30_days), callback=self.parse_video_play_trend_30_days_detail)

            # 视频播放趋势-最近90天
            video_play_trend_90_days = 'https://uaa.if.iqiyi.com/video_index/v2/get_index_trend?album_id=' + aid + '&time_window=90'
            yield Request(url=parse.urljoin(response.url, video_play_trend_90_days), callback=self.parse_video_play_trend_90_days_detail)

            # 视频播放趋势-最近半年
            video_play_trend_180_days = 'https://uaa.if.iqiyi.com/video_index/v2/get_index_trend?album_id=' + aid + '&time_window=180'
            yield Request(url=parse.urljoin(response.url, video_play_trend_180_days), callback=self.parse_video_play_trend_180_days_detail)

            # 视频播放趋势-全部
            video_play_trend_all_days = 'https://uaa.if.iqiyi.com/video_index/v2/get_index_trend?album_id=' + aid + '&time_window=-1'
            yield Request(url=parse.urljoin(response.url, video_play_trend_all_days), callback=self.parse_video_play_trend_all_days_detail)

            # 明星看点
            star_look = 'https://uaa.if.iqiyi.com/video_index/v2/star_appearance?album_id=' + aid
            yield Request(url=parse.urljoin(response.url, star_look), callback=self.parse_star_look_detail)

            # 观影舆情 -30天内
            view_of_public_opinion = 'http://sentiment.if.iqiyi.com/po?qipu_ids=' + aid + '&type=VideoView&range=Last30Days'
            yield Request(url=parse.urljoin(response.url, view_of_public_opinion), callback=self.parse_view_of_public_opinion_detail)

            # 社交舆情 暂无数据

            # 场景看点 暂无数据

            # 受众画像
            audience_portrait = 'https://uaa.if.iqiyi.com/video_index/v2/get_user_profile?album_id=' + aid
            yield Request(url=parse.urljoin(response.url, audience_portrait), callback=self.parse_audience_portrait_detail)


    def parse_city_play_data_detail(self, response):
        city_play_data_item = CityPlayDataItem()
        # 播放设备分布key_name
        key_name = "city_play_data"
        city_play_data_item['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            city_play_data_item['name'] = name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_item(city_play_data_item, key_name, name)
            # 剧集aid
            city_play_data_item['aid'] = jsondata['ids'][0]
            # 具体数据
            city_play_data_item['data'] = jsondata['data'][0]
            yield city_play_data_item

    def parse_play_device_distribution_detail(self, response):

        device_distribution_item = DeviceDistributionItem()
        # 播放设备分布key_name
        key_name = "play_device_distribution"
        device_distribution_item['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            device_distribution_item['name'] = name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_item(device_distribution_item, key_name, name)
            # 剧集aid
            device_distribution_item['aid'] = jsondata['ids'][0]
            # 具体数据
            data = jsondata['data'][0]
            for device_distribution in data:
                dev_names = device_distribution
                dev_name = dev_names['name']
                value = dev_names['value']
                if dev_name == '移动端':
                    print("移动端：" + str(value))
                    device_distribution_item['mobile_terminal_distribution'] = value
                else:
                    print("PC端：" + str(value))
                    device_distribution_item['pc_device_distribution'] = value

            yield device_distribution_item

    def parse_video_play_trend_7_days_detail(self, response):
        play_trend_7_days_item = PlayTrend7DaysItem()
        # key_name
        key_name = "play_trend_7_days"
        play_trend_7_days_item['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            play_trend_7_days_item['name'] = name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_item(play_trend_7_days_item, key_name, name)
            # 剧集aid
            play_trend_7_days_item['aid'] = jsondata['ids'][0]
            # 具体数据
            # 播放量
            play_trend_7_days_item['data'] = jsondata['details'][0]['data']
            # 播放日期
            play_trend_7_days_item['playtime'] = jsondata['playtime']
            yield play_trend_7_days_item

    def parse_video_play_trend_30_days_detail(self, response):
        play_trend_30_days_item = PlayTrend30DaysItem()
        # key_name
        key_name = "play_trend_30_days"
        play_trend_30_days_item['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            play_trend_30_days_item['name'] = name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_item(play_trend_30_days_item, key_name, name)
            # 剧集aid
            play_trend_30_days_item['aid'] = jsondata['ids'][0]
            # 具体数据
            # 播放量
            play_trend_30_days_item['data'] = jsondata['details'][0]['data']
            # 播放日期
            play_trend_30_days_item['playtime'] = jsondata['playtime']
            yield play_trend_30_days_item

    def parse_video_play_trend_90_days_detail(self, response):
        play_trend_90_days_item = PlayTrend90DaysItem()
        # key_name
        key_name = "play_trend_90_days"
        play_trend_90_days_item['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            play_trend_90_days_item['name'] = name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_item(play_trend_90_days_item, key_name, name)
            # 剧集aid
            play_trend_90_days_item['aid'] = jsondata['ids'][0]
            # 具体数据
            # 播放量
            play_trend_90_days_item['data'] = jsondata['details'][0]['data']
            # 播放日期
            play_trend_90_days_item['playtime'] = jsondata['playtime']
            yield play_trend_90_days_item

    def parse_video_play_trend_180_days_detail(self, response):
        play_trend_180_days_item = PlayTrend180DaysItem()
        # key_name
        key_name = "play_trend_180_days"
        play_trend_180_days_item['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            play_trend_180_days_item['name'] = name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_item(play_trend_180_days_item, key_name, name)
            # 剧集aid
            play_trend_180_days_item['aid'] = jsondata['ids'][0]
            # 具体数据
            # 播放量
            play_trend_180_days_item['data'] = jsondata['details'][0]['data']
            # 播放日期
            play_trend_180_days_item['playtime'] = jsondata['playtime']
            yield play_trend_180_days_item

    def parse_video_play_trend_all_days_detail(self, response):
        play_trend_all_days_item = PlayTrendAllDaysItem()
        # key_name
        key_name = "play_trend_all_days"
        play_trend_all_days_item['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            play_trend_all_days_item['name'] = name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_item(play_trend_all_days_item, key_name, name)
            # 剧集aid
            play_trend_all_days_item['aid'] = jsondata['ids'][0]
            # 具体数据
            # 播放量
            play_trend_all_days_item['data'] = jsondata['details'][0]['data']
            # 播放日期
            play_trend_all_days_item['playtime'] = jsondata['playtime']
            yield play_trend_all_days_item

    def parse_star_look_detail(self, response):
        star_look_item = StarLookItem()
        # key_name
        key_name = "star_look"
        star_look_item['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            star_look_item['name'] = name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_item(star_look_item, key_name, name)
            # 剧集aid
            star_look_item['aid'] = jsondata['ids'][0]
            # 具体数据
            star_look_item['data'] = jsondata['data'][0]
            yield star_look_item

    def parse_view_of_public_opinion_detail(self, response):
        view_of_public_opinion = ViewOfPublicOpinionItem()
        # key_name
        key_name = "sentiments"
        view_of_public_opinion['key_name'] = key_name
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            aid = jsondata['data'][0]['albumID']
            view_of_public_opinion['aid'] = aid
            str_aid = str(aid)
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline = IqiyiPipeline()
            iqiyipipline.remove_aid_item(view_of_public_opinion, key_name, str_aid)
            view_of_public_opinion['data'] = jsondata['data'][0]['sentiments']
            yield view_of_public_opinion

    def parse_audience_portrait_detail(self, response):
        jsondata = json.loads(response.text)
        code = jsondata['code']
        if code == 'A00000':
            # 剧集名称
            name = jsondata['names'][0]
            # 剧集aid
            aid = jsondata['ids'][0]
            str_aid = str(aid)
            iqiyipipline = IqiyiPipeline()
            # ----------------受众性别 start------------------------
            audience_sex = AudienceSexItem()
            key_name = "audience_sex"
            audience_sex['key_name'] = key_name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入

            iqiyipipline.remove_item(audience_sex, key_name, name)
            audience_sex['name'] = name
            audience_sex['aid'] = aid
            # 具体数据
            audience_sex['sex_data_name'] = jsondata['data']['genderLabels']

            audience_sex['sex_data_value'] = jsondata['data']['details'][0][str_aid]['gender']
            yield audience_sex
            # ----------------受众年龄 start------------------------
            audience_age = AudienceAgeItem()
            key_name = "audience_age"
            audience_age['key_name'] = key_name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline.remove_item(audience_age, key_name, name)
            audience_age['name'] = name
            audience_age['aid'] = aid
            # 具体数据
            audience_age['age_data_name'] = jsondata['data']['ageLabels']
            audience_age['age_data_value'] = jsondata['data']['details'][0][str_aid]['age']
            yield audience_age
            # ----------------受众星座 start------------------------
            audience_constellation = AudienceConstellationItem()
            key_name = "audience_constellation"
            audience_constellation['key_name'] = key_name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline.remove_item(audience_constellation, key_name, name)
            audience_constellation['name'] = name
            audience_constellation['aid'] = aid
            # 具体数据
            audience_constellation['constellation_data_name'] = jsondata['data']['constellationLabels']
            audience_constellation['constellation_data_value'] = jsondata['data']['details'][0][str_aid]['constellation']
            yield audience_constellation
            # ----------------受众学历 start------------------------
            audience_education = AudienceEducationItem()
            key_name = "audience_education"
            audience_education['key_name'] = key_name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline.remove_item(audience_education, key_name, name)
            audience_education['name'] = name
            audience_education['aid'] = aid
            # 具体数据
            audience_education['education_data_name'] = jsondata['data']['educationLabels']
            audience_education['education_data_value'] = jsondata['data']['details'][0][str_aid]['education']
            yield audience_education
            # ----------------受众兴趣 start------------------------
            audience_interest = AudienceInterestItem()
            key_name = "audience_interest"
            audience_interest['key_name'] = key_name
            # 伪造一个唯一key，插入mongodb之前先做删除，再做插入
            iqiyipipline.remove_item(audience_interest, key_name, name)
            audience_interest['name'] = name
            audience_interest['aid'] = aid
            # 具体数据
            audience_interest['interest_data_name'] = jsondata['data']['interestLabels']
            audience_interest['interest_data_value'] = jsondata['data']['details'][0][str_aid]['interest']
            yield audience_interest

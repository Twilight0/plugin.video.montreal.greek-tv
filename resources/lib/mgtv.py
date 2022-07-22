# -*- coding: utf-8 -*-

"""
    Montreal Greek TV Add-on
    Author: greektimes

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# import json
from tulip import control, cache, directory #, client, bookmarks as bms
# from scrapetube.list_formation import list_channel_videos
# from tulip.compat import range, iteritems
# from tulip.init import syshandle
# from tulip.log import LOGDEBUG

# cid = 'UCFr8nqHDhA_fLQq2lEK3Mlw'
cache_function = cache.FunctionCache().cache_function


# @cache_function(720)
# def yt_videos():
#
#     videos = list_channel_videos(cid, limit=3)
#
#     LOGDEBUG(repr(videos))
#
#     return list_channel_videos(cid, limit=3)
#
#
# def vod():
#
#     video_list = yt_videos()
#
#     if not video_list:
#         return
#
#     for vid in video_list:
#         vid.update({'action': 'play', 'isFolder': 'False'})
#         bookmark = dict((k, v) for k, v in iteritems(vid) if not k == 'next')
#         bookmark['bookmark'] = vid['url']
#         bookmark_cm = {'title': 30009, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
#         vid.update({'cm': [bookmark_cm]})
#
#     directory.add(video_list)


# @cache_function(720)
# def _news_index():
#
#     base_link = 'https://issuu.com/greektimes/docs/'
#     json_obj = 'https://issuu.com/call/profile_demo/v1/documents/greektimes?offset=0&limit=1000'
#
#     result = client.request(json_obj)
#
#     news_list = json.loads(result)['items']
#
#     menu = []
#
#     for n in news_list:
#
#         title = n['title']
#         image = n['coverUrl']
#         url = base_link + n['uri']
#
#         data = {'title': title, 'image': image, 'url': url, 'action': 'paper_index'}
#
#         menu.append(data)
#
#     return menu


# def news_index():
#
#     menu = _news_index()
#
#     if menu is None:
#         return
#
#     directory.add(menu, content='images')


# @cache_function(720)
# def _paper_index(link):
#
#     base_img_url = 'https://image.isu.pub/'
#
#     html = client.request(link)
#
#     script = client.parseDOM(html, 'script', attrs={'type': 'application/javascript'})[-2]
#
#     data = json.loads(script.partition(' = ')[2].rstrip(';'))
#     document = data['document']
#     total_pages = int(document['pageCount'])
#
#     menu = []
#
#     for page in list(range(1, total_pages + 1)):
#
#         title = document['title'] + ' - ' + control.lang(30003) + ' ' + str(page)
#         page_img = base_img_url + document['id'] + '/jpg/page_{0}_thumb_large.jpg'.format(str(page))
#         page_url = base_img_url + document['id'] + '/jpg/page_{0}.jpg'.format(str(page))
#
#         data = {'title': title, 'image': page_img, 'url': page_url}
#
#         menu.append(data)
#
#     return menu
#
#
# def paper_index(link):
#
#     menu = []
#
#     items = _paper_index(link)
#
#     if items is None:
#         return
#
#     for i in items:
#         li = control.item(label=i['title'])
#         li.setArt(
#             {
#                 'poster': i['image'], 'thumb': i['image'],
#                 'fanart': control.join(control.addonPath, 'resources', 'media', 'newspaper_fanart.png')
#             }
#         )
#         li.setInfo('image', {'title': i['title'], 'picturepath': i['url']})
#         url = i['url']
#         menu.append((url, li, False))
#
#     control.content(syshandle, 'images')
#     control.addItems(syshandle, menu)
#     control.directory(syshandle)


def main_menu():

    livetv_url = 'http://live.greektv.ca/hls1/greektv.m3u8'
    radio_url = 'http://live.greekradio.ca:8000/live'
    center_ville_url = 'http://mediacast.b2b2c.ca:8010/'

    menu = [
        {
            'title': 'Montreal Greek TV - Live'.replace('Live', control.lang(30004)),
            'action': 'play',
            'url': livetv_url,
            'icon': 'livetv.png',
            'isFolder': 'False'
        }
        ,
        {
            'title': 'Montreal Greek Radio - Live'.replace('Live', control.lang(30004)),
            'action': 'play',
            'url': radio_url,
            'icon': 'radio.png',
            'isFolder': 'False'
        }
        # ,
        # {
        #     'title': u'Montreal Greek TV - {0}'.format(control.lang(30001)),
        #     'action': 'youtube',
        #     'icon': 'youtube.png'
        # }
        ,
        {
            'title': u'Radio Centre-Ville - Live'.replace('Live', control.lang(30004)),
            'action': 'play',
            'url': center_ville_url,
            'icon': 'Radio_Centre-ville-live.png',
            'isFolder': 'False'
        }
        # {
        #     'title': u'Radio Centre-Ville - {0}'.format(control.lang(30005)),
        #     'action': 'audio_addon',
        #     'icon': 'pod_icon.png',
        #     'fanart': 'pod_fanart.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30002),
        #     'action': 'news_addon',
        #     'icon': 'newspaper_icon.png',
        #     'fanart': 'xronika_fanart.png'
        # }
    ]

    # for item in menu:
    #     cache_clear = {'title': 30006, 'query': {'action': 'cache_clear'}}
    #     item.update({'cm': [cache_clear]})

    directory.add(menu)


# def bookmarks():
#
#     self_list = bms.get()
#
#     if not self_list:
#         na = [{'title': control.lang(30008), 'action': None}]
#         directory.add(na)
#         return
#
#     for i in self_list:
#         bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
#         bookmark['delbookmark'] = i['url']
#         i.update({'cm': [{'title': 30010, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})
#
#     control.sortmethods('title')
#
#     directory.add(self_list, content='videos')


def play_item(path):

    directory.resolve(path)

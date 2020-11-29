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

import json, re
from base64 import b64decode
from tulip import control, youtube, cache, directory, client
from tulip.compat import range
from tulip.init import syshandle


def yt():

    # Please do not copy these keys, instead create your own:
    # https://ytaddon.page.link/keys

    key = 'QUl6YVN5Q3JHU1c3RHB3aWpkYkxMOWh5WU54VHFfRWR1b0M3b2w4'
    cid = 'UCFr8nqHDhA_fLQq2lEK3Mlw'

    return youtube.youtube(key=b64decode(key)).videos(cid)


def vod():

    video_list = cache.get(yt, 12)

    for v in video_list:
        v.update({'action': 'play', 'isFolder': 'False'})

    video_list.sort(key=lambda i: i['dateadded'], reverse=True)

    directory.add(video_list)


def _news_index():

    base_link = 'https://issuu.com/greektimes/docs/'
    json_obj = 'https://issuu.com/call/profile_demo/v1/documents/greektimes?offset=0&limit=1000'

    result = client.request(json_obj)

    news_list = json.loads(result)['items']

    menu = []

    for n in news_list:

        title = n['title']
        image = n['coverUrl']
        url = base_link + n['uri']

        data = {'title': title, 'image': image, 'url': url, 'action': 'paper_index'}

        menu.append(data)

    return menu


def news_index():

    menu = cache.get(_news_index, 12)

    if menu is None:
        return

    directory.add(menu, content='images')


def _paper_index(link):

    base_img_url = 'https://image.isu.pub/'

    html = client.request(link)

    script = client.parseDOM(html, 'script', attrs={'type': 'application/javascript'})[-2]

    data = json.loads(script.partition(' = ')[2].rstrip(';'))
    document = data['document']
    total_pages = int(document['pageCount'])

    menu = []

    for page in list(range(1, total_pages + 1)):

        title = document['title'] + ' - ' + control.lang(30003) + ' ' + str(page)
        page_img = base_img_url + document['id'] + '/jpg/page_{0}_thumb_large.jpg'.format(str(page))
        page_url = base_img_url + document['id'] + '/jpg/page_{0}.jpg'.format(str(page))

        data = {'title': title, 'image': page_img, 'url': page_url}

        menu.append(data)

    return menu


def paper_index(link):

    menu = []

    items = cache.get(_paper_index, 12, link)

    if items is None:
        return

    for i in items:
        li = control.item(label=i['title'])
        li.setArt(
            {
                'poster': i['image'], 'thumb': i['image'],
                'fanart': control.join(control.addonPath, 'resources', 'media', 'newspaper_fanart.png')
            }
        )
        li.setInfo('image', {'title': i['title'], 'picturepath': i['url']})
        url = i['url']
        menu.append((url, li, False))

    control.content(syshandle, 'images')
    control.addItems(syshandle, menu)
    control.directory(syshandle)


def _podcasts():

    menu = []

    feed_url = 'http://greektimes.ca/feed/podcast/'

    xml = client.request(feed_url)

    items = client.parseDOM(xml, 'item')

    for item in items:

        title = client.parseDOM(item, 'title')[0]
        uri = client.parseDOM(item, 'enclosure', attrs={'type': 'audio/mpeg'}, ret='url')[0]
        fanart = client.parseDOM(item, 'enclosure', attrs={'type': 'image/(?:jpeg|png)'}, ret='url')[0]
        image = client.parseDOM(item, 'img', attrs={'class': '.*?wp-image-\d{1,4}.*?'}, ret='srcset')[0]
        img_urls = image.split(',')
        image = [
            i.rpartition(' ')[0].strip() for i in img_urls if int(i[-5:-1]) == min([int(v[-5:-1]) for v in img_urls])
        ][0]
        comment = client.parseDOM(item, 'description')[0]
        year = int(re.search('(\d{4})', client.parseDOM(item, 'pubDate')[0]).group(1))

        data = {
            'title': title, 'url': uri, 'image': image, 'fanart': fanart, 'comment': comment, 'lyrics': comment,
            'year': year
        }

        menu.append(data)

    return menu


def podcasts():

    items = cache.get(_podcasts, 6)

    if items is None:
        return

    for i in items:
        i.update({'action': 'play', 'isFolder': 'False'})

    directory.add(items, infotype='music', mediatype='music')


def broadcasts():

    xml = client.request('http://greektimes.ca/feed/psa/')

    url = client.parseDOM(xml, 'enclosure', ret='url')[0]

    return url


def main_menu():

    xml = client.request('http://s135598769.onlinehome.us/mgtv.xml')

    mgtv = client.parseDOM(xml, 'title')[0]
    livetv_url = 'http://94.130.180.175:8081/live/greektv/playlist.m3u8'
    mgr = client.parseDOM(xml, 'title')[1]
    radio_url = 'http://94.130.180.175:8000/live'
    center_ville_url = 'http://mediacast.b2b2c.ca:8010/'

    menu = [
        {
            'title': mgtv.replace('Live', control.lang(30004)),
            'action': 'play',
            'url': livetv_url,
            'icon': 'livetv.png',
            'isFolder': 'False'
        }
        ,
        {
            'title': mgr.replace('Live', control.lang(30004)),
            'action': 'play',
            'url': radio_url,
            'icon': 'radio.png',
            'isFolder': 'False'
        }
        ,
        {
            'title': u'Montreal Greek TV - {0}'.format(control.lang(30001)),
            'action': 'youtube',
            'icon': 'youtube.png'
        }
        ,
        {
            'title': u'Radio Centre-Ville - Live',
            'action': 'play',
            'url': center_ville_url,
            'icon': 'Radio_Centre-ville-live.png',
            'isFolder': 'False'
        }
        ,
        {
            'title': control.lang(30007),
            'action': 'play',
            'url': 'broadcasts',
            'icon': 'center_ville.png',
            'isFolder': 'False'
        }
        ,
        {
            'title': u'Radio Centre-Ville - {0}'.format(control.lang(30005)),
            'action': 'audio_addon',
            'icon': 'pod_icon.png',
            'fanart': 'pod_fanart.jpg'
        }
        ,
        {
            'title': control.lang(30002),
            'action': 'news_addon',
            'icon': 'newspaper_icon.png',
            'fanart': 'xronika_fanart.png'
        }
    ]

    for item in menu:
        cache_clear = {'title': 30006, 'query': {'action': 'cache_clear'}}
        item.update({'cm': [cache_clear]})

    directory.add(menu)


def play_item(path):

    if path == 'broadcasts':
        path = broadcasts()

    directory.resolve(path)

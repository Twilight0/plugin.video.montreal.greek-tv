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

from tulip import control, directory
from tulip.url_dispatcher import urldispatcher


LIVETV_URL = 'http://live.greektv.ca/hls1/greektv.m3u8'
RADIO_URL = 'http://live.greekradio.ca:8000/live'


@urldispatcher.register('root')
def root():

    menu = [
        {
            'title': 'Montreal Greek TV - Live'.replace('Live', control.lang(30004)),
            'action': 'play',
            'url': LIVETV_URL,
            'icon': 'montreal_tv.png',
            'isFolder': 'False'
        }
        ,
        {
            'title': 'Montreal Greek Radio - Live'.replace('Live', control.lang(30004)),
            'action': 'play',
            'url': RADIO_URL,
            'icon': 'montreal_radio.png',
            'isFolder': 'False'
        }
    ]

    directory.add(menu)


@urldispatcher.register('play', ['url', 'resolved_mode'])
def play(url, resolved_mode=True):

    if resolved_mode:
        directory.resolve(url)
    else:
        directory.resolve(
            url, meta={
                'title': 'Montreal Greek Radio - Live'.replace('Live', control.lang(30004))
            }, icon={
                'icon': control.addonmedia('montreal_radio.png'), 'thumb': control.addonmedia('montreal_radio.png'),
                'fanart': control.addonmedia('montreal_backround.png')
            }, resolved_mode=resolved_mode
        )

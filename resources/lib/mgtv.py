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


def main_menu():

    livetv_url = 'http://live.greektv.ca/hls1/greektv.m3u8'
    radio_url = 'http://live.greekradio.ca:8000/live'

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
    ]

    directory.add(menu)


def play_item(path):

    directory.resolve(path)

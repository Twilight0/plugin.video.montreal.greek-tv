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

from tulip import bookmarks as bms
from tulip.init import params

action = params.get('action')
url = params.get('url')
content = params.get('content_type')


if action is None:

    if content == 'image':
        from resources.lib.mgtv import news_index
        news_index()
    elif content == 'audio':
        from resources.lib.mgtv import podcasts
        podcasts()
    else:
        from resources.lib.mgtv import main_menu
        main_menu()

elif action == 'play':

    from resources.lib.mgtv import play_item
    play_item(url)

elif action == 'youtube':

    from resources.lib.mgtv import vod
    vod()

elif action == 'news_index':

    from resources.lib.mgtv import news_index
    news_index()

elif action == 'paper_index':

    from resources.lib.mgtv import paper_index
    paper_index(url)

elif action == 'addBookmark':

    bms.add(url)

elif action == 'deleteBookmark':

    bms.delete(url)

elif action == 'news_addon':

    from tulip import control
    control.execute('ActivateWindow(pictures,"plugin://{0}/?content_type=image",return)'.format(control.addonInfo('id')))

elif action == 'audio_addon':

    from tulip import control
    control.execute('ActivateWindow(music,"plugin://{0}/?action=podcasts",return)'.format(control.addonInfo('id')))

elif action == 'cache_clear':

    from tulip import cache
    cache.FunctionCache().reset_cache(notify=True)

else:

    import sys
    sys.exit()

"""
iWriteIt - You Like?

Copyright (C) 2014 Suriyan Laohaprapanon

For comments, suggestions or other messages, contact me at:
<suriyant@gmail.com>

This file is part of iWriteIt.

iWriteIt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

iWriteIt is distributed in the hope that it will be fun,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with iWriteIt.  If not, see <http://www.gnu.org/licenses/>.
"""

from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string('''
<InfoPopup>:
    auto_dismiss: True
    size_hint: None, None
    size: 400, 200
    on_open: root.dismiss_trigger()
    title: root.title
    Label:
        text: root.text
''')


class InfoPopup(Popup):
    title = StringProperty('Information')
    text = StringProperty('')

    def __init__(self, time=2, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.dismiss_trigger = Clock.create_trigger(self.dismiss, time)

#!/usr/bin/env python
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

### 'multistroke' just available in master branch
#import kivy
#kivy.require('1.8.1-dev')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Ellipse, Line
from kivy.multistroke import Recognizer

from threading import Thread
from random import randint

from plyer import tts
from helpers import InfoPopup

# FIXME: require by buildozer?
__version__ = "0.9.0"

MAX_DIGITS = 4


class Background(Image):
    """ Background image
    """
    pass


class DigitBox(Widget):
    """ Class of single digit
    """
    text = StringProperty(None)
    answer = NumericProperty(None)

    def __init__(self, **kwargs):
        super(DigitBox, self).__init__(**kwargs)

    def clear(self):
        self.text = ""


class AppSettings(BoxLayout):
    """ Application settings
    """
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AppSettings, self).__init__(**kwargs)

    def write_settings(self):
        """ Write back current settings to configuration file
        """
        val = 'yes' if self.ids._music.active else 'no'
        self.app.config.set('general', 'music', val)
        val = 'yes' if self.ids._voice.active else 'no'
        self.app.config.set('general', 'voice', val)
        self.app.config.set('basicmath', 'maxdigits', self.ids._maxdigits.text)
        self.app.config.set('basicmath', 'operation', self.ids._operation.text)
        self.app.config.write()
        self.app.play_music()

    def read_settings(self):
        """ Read settings to screen
        """
        if self.app.config.get('general', 'music') == 'yes':
            self.ids._music.active = True
        else:
            self.ids._music.active = False
        if self.app.config.get('general', 'voice') == 'yes':
            self.ids._voice.active = True
        else:
            self.ids._voice.active = False
        self.ids._maxdigits.text = self.app.config.get('basicmath', 'maxdigits')
        self.ids._operation.text = self.app.config.get('basicmath', 'operation')


class WriteBoard(FloatLayout):
    """ Write board
    """
    digit1 = ObjectProperty()
    digit2 = ObjectProperty()
    digit3 = ObjectProperty()
    digit4 = ObjectProperty()
    result_area = ObjectProperty()
    surface = ObjectProperty()
    root = ObjectProperty()

    def __init__(self, **kwargs):
        super(WriteBoard, self).__init__(**kwargs)
        self.a = None
        self.recognizer = None
        self.infopopup = InfoPopup()

    def on_touch_down(self, touch):
        if self.menu.collide_point(*touch.pos):
            return self.menu.on_touch_down(touch)
        if self.collide_point(*touch.pos) and \
           not self.result_area.collide_point(*touch.pos):
            userdata = touch.ud
            userdata['color'] = c = (1, 0, 0)
            with self.canvas.after:
                Color(*c, mode='rgb')
                d = 6
                Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))
                userdata['line'] = Line(points=(touch.x, touch.y), width=3)
            return True
        else:
            return super(WriteBoard, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.menu.collide_point(*touch.pos):
            return self.menu.on_touch_move(touch)
        if self.collide_point(*touch.pos) and \
           not self.result_area.collide_point(*touch.pos):
            if 'line' in touch.ud:
                touch.ud['line'].points += [touch.x, touch.y]
            return True
        else:
            return super(WriteBoard, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.menu.collide_point(*touch.pos):
            return self.menu.on_touch_up(touch)
        if self.collide_point(*touch.pos) and \
           not self.result_area.collide_point(*touch.pos):
            return True
        else:
            return super(WriteBoard, self).on_touch_up(touch)

    def clear(self, all=False):
        if all:
            self.canvas.after.clear()
        self.digit1.clear()
        self.digit2.clear()
        self.digit3.clear()
        self.digit4.clear()

    def _to_int(self, s):
        try:
            i = int(s)
        except:
            i = 0
        return i

    def get_answer(self):
        return eval("%d %s %s" % (self.a, self.oper, self.b))

    def check(self, popup=False):
        a1 = self._to_int(self.digit1.text)
        a2 = self._to_int(self.digit2.text)
        a3 = self._to_int(self.digit3.text)
        a4 = self._to_int(self.digit4.text)
        answer = a4 * 1000 + a3 * 100 + a2 * 10 + a1
        if answer == self.get_answer():
            if popup:
                self.infopopup.text = "Correct, very good!!!"
                self.infopopup.open()
            return True
        else:
            return False

    def set_digits(self, num, prefix):
        leading = True
        for i in range(MAX_DIGITS, 1, -1):
            mul = 10**(i - 1)
            if num >= mul:
                leading = False
                self.ids['%s%d' % (prefix, i)].text = str(int(num / mul))
                num %= mul
            else:
                if leading:
                    self.ids['%s%d' % (prefix, i)].text = ""
                else:
                    self.ids['%s%d' % (prefix, i)].text = "0"

        self.ids['%s%d' % (prefix, 1)].text = str(num)

    def set_answer(self, ans, prefix):
        for i in range(MAX_DIGITS, 1, -1):
            mul = 10**(i - 1)
            if ans >= mul:
                self.ids['%s%d' % (prefix, i)].answer = int(ans / mul)
                ans %= mul
            else:
                self.ids['%s%d' % (prefix, i)].answer = 0

        self.ids['%s%d' % (prefix, 1)].answer = ans

    def new_question(self):
        maxdigits = int(self.root.app.config.get('basicmath', 'maxdigits'))
        maxnum = 10 ** maxdigits - 1
        oper = self.root.app.config.get('basicmath', 'operation')
        if oper == 'Mix':
            if randint(0, 1):
                self.oper = '+'
            else:
                self.oper = '-'
        elif oper == 'Plus':
            self.oper = '+'
        else:
            self.oper = '-'
        a = randint(0, maxnum)
        b = randint(0, maxnum)
        if self.oper == '-' and a < b:
            self.a = b
            self.b = a
        else:
            self.a = a
            self.b = b

    def new(self):
        if self.recognizer is None:
            self.recognizer = Recognizer()
            self.recognizer.import_gesture(filename='gestures/raingan.kg')
            self.surface.bind(on_gesture_discard=self.handle_gesture_discard)
            self.surface.bind(on_gesture_complete=self.handle_gesture_complete)
            self.surface.bind(on_gesture_cleanup=self.handle_gesture_cleanup)

        if self.a is None or self.check(True):
            self.clear(True)
            self.new_question()
            self.set_digits(self.a, 'a')
            self.ids._operator.text = self.oper
            self.set_digits(self.b, 'b')
            text = ("%d %s %d" %
                    (self.a, 'plus' if self.oper == '+' else 'minus', self.b))
            self.root.app.speak(text)
            ans = self.get_answer()
            self.set_answer(ans, '_digit')
        else:
            self.clear(True)

    def handle_gesture_cleanup(self, surface, g, *l):
        if hasattr(g, '_result_label'):
            surface.remove_widget(g._result_label)

    def handle_gesture_discard(self, surface, g, *l):
        # Don't bother creating Label if it's not going to be drawn
        if surface.draw_timeout == 0:
            return

        text = '[b]Please write a number[/b]'
        g._result_label = Label(text=text, markup=True, size_hint=(None, None),
                                center=(g.bbox['minx'], g.bbox['miny']))
        self.surface.add_widget(g._result_label)

    def handle_gesture_complete(self, surface, g, *l):
        result = self.recognizer.recognize(g.get_vectors())
        result._gesture_obj = g
        result.bind(on_complete=self.handle_recognize_complete)

    def handle_recognize_complete(self, result, *l):
        # Don't bother creating Label if it's not going to be drawn
        if self.surface.draw_timeout == 0:
            return

        best = result.best
        if best['name'] is None:
            num = ""
        else:
            num = best['name']

        g = result._gesture_obj
        x = g.bbox['minx']
        y = g.bbox['miny']
        w = Widget(pos=(x, y), size=(g.width, g.height))
        if self.digit1.collide_widget(w):
            self.digit1.text = num
        if self.digit2.collide_widget(w):
            self.digit2.text = num
        if self.digit3.collide_widget(w):
            self.digit3.text = num
        if self.digit4.collide_widget(w):
            self.digit4.text = num

        if self.check():
            Clock.schedule_once(lambda dt: self.new(), 1)


class RootWidget(FloatLayout):
    """ Root Widget of Application
    """
    app = ObjectProperty()
    manager = ObjectProperty()
    board = ObjectProperty()
    settings = ObjectProperty()

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)


class iWriteItApp(App):
    title = 'iWriteIt - You Like?'
    if platform == 'win':
        icon = 'graphics/icon-64.ico'
    elif platform == 'macosx':
        icon = 'graphics/icon.icns'
    else:
        icon = 'graphics/icon-64.png'
    music = None

    # FIXME: to hide Kivy settings
    #use_kivy_settings = False
    # To fully disable settings windows
    #def open_settings(self, *largs):
    #    pass

    def build(self):
        music = "sounds/music.%s" % ('wav' if platform == 'macosx' else 'ogg')
        self.music = SoundLoader.load(music)
        print self.music
        self.play_music()
        self.root = RootWidget(app=self)
        self.speak("Welcome to I Write It")
        return self.root

    def build_config(self, config):
        config.adddefaultsection('general')
        config.setdefault('general', 'music', 'yes')
        config.setdefault('general', 'voice', 'yes')
        config.adddefaultsection('basicmath')
        config.setdefault('basicmath', 'maxdigits', '2')
        config.setdefault('basicmath', 'operation', 'Plus')

    def on_pause(self):
        self.music.stop()
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        self.play_music()
        pass

    def play_music(self):
        if self.config.get('general', 'music') == 'yes':
            # Fix volume to 30% for background music
            self.music.volume = 0.3
            self.music.loop = True
            self.music.play()
        else:
            self.music.stop()

    def speak(self, text):
        if self.config.get('general', 'voice') == "yes":
            if platform == 'android':
                Clock.schedule_once(lambda dt, t=text: tts.speak(t), 0.1)
            else:
                thread = Thread(target=tts.speak, args=(text,))
                thread.start()

    def start(self):
        self.root.manager.current = "writing"
        self.root.board.new()

    def settings(self):
        self.root.settings.read_settings()
        self.root.manager.current = "settings"


if __name__ in ['__main__', '__android__']:
    iWriteItApp().run()

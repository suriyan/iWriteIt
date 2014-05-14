iWriteIt - You Like?
====================

An application for Kids to practice Addition and Substraction skills. 
It utilizes Kivy Gesture recogition, especially for `multistroke`
gesture recognition was just introduced in master branch (1.8.1-dev).

Initially, I've used Tesseract-OCR to recoginize hand writing.
However, we also need to train it for difference hand writing styles
and is not easily compare to Kivy Gesture recognition process.

Finally, I've decided to use Kivy multistroke gesture recognition
instead. This is a good demo application for multistroke gesture
recognition.

https://github.com/kivy/kivy/tree/master/examples/demo/multistroke

For more attractive and may also help to improve Listening skills.
Application includes Text to Speech (TTS) feature.

PREREQUISITE
------------

* Kivy master branch (1.8.1-dev) for Multistroke gesture

    (if you still use stable branch (1.8.0) just apply for only the `multistroke` patch)

* plyer for Text to Speech (TTS)

    ```
    pip install plyer
    ```

    *NOTE THAT: On Windows and Linux also requires eSpeak (http://espeak.sourceforge.net/)*

TESTED TARGET
-------------

* Windows
    - Tested on Windows 8.1 (64-bit)
    - Tested on Windows 7 (32-bit)

* Linux
    - Tested on Ubuntu 12.10 (32-bit)

* Android Target
    - Tested on 2.3.6 (Motorola Defy)
    - Tested on 4.2.2 (Samsung Galaxy Note 8)

SOURCE CODE
-----------

    https://github.com/suriyan/iWriteIt

PRE-BUILD BINARIES VERSION
----------------

Pre-built binary versions will available at :-

https://www.dropbox.com/sh/csp47vb5v2xa22v/AADSU-9A7xXwhctxAV7dCYRCa

TODO
----

* User profile for specific gesture data
* Statistics
* Localize number (eg. Thai)
* ...

BUILD & PACKAGING
-----------------

* Windows

    TBD (PyInstaller?)

* Linux

    TBD (PyInstaller?)

* MacOSX

    TBD (PyInstaller?)

* Android (Python for Android)

    ```
    ./build.py --dir /opt/projects/iWriteIt --name "iWriteIt" --package com.gurucafe.iwriteit --version 0.9.0 --orientation landscape --icon /opt/projects/iWriteIt/graphics/icon-128.png debug
    ```

    See http://kivy.org/docs/guide/packaging-android.html for more detail

* iOS (TBD)

    http://kivy.org/docs/guide/packaging-ios.html

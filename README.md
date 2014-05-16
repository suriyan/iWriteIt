iWriteIt - You Like?
====================

An application for Kids to practice Addition and Subtraction skills. 
It utilizes Kivy Gesture recognition, especially for `multistroke`
gesture recognition was just introduced in master branch (1.8.1-dev).

Initially, I've started with Tesseract-OCR to recognize hand writing.
However, we also need to train it for difference hand writing styles
and is not easily compare to Kivy Gesture recognition process.

Finally, I've decided to use Kivy multistroke gesture recognition
instead. This is a good demo application for multistroke gesture
recognition.

https://github.com/kivy/kivy/tree/master/examples/demo/multistroke

For more attractive and may also help to improve Listening skills.
Application includes Text to Speech (TTS) feature.

Please visit the following link to see how does it working :-

http://1drv.ms/1nQKnGx

HISTORY
-------

* 2014/05/15 (1.0.0)
    - Implement my gesture load/save/update

* 2014/05/14 (0.9.0)
    - Initial release

TODO
----

* User profile for specific gesture data
* Timer, score and statistics
* More number practical skills (eg. sequence, multiply, ...)
* Localize number (ex. Thai)
* ...

PREREQUISITE
------------

* Kivy master branch (1.8.1-dev) for Multistroke gesture

    (if you still use stable branch (1.8.0) you need to patch for `multistroke` feature)

* `plyer` for Text to Speech (TTS)

    ``
    pip install -e git+https://github.com/kivy/plyer#egg=plyer
    ```

    *REMARKS*
    - `plyer` in PyPi is NOT up-to-date, please install from git repository
    - On Windows and Linux depended on eSpeak (http://espeak.sourceforge.net/)

TESTED TARGET
-------------

* Windows
    - Tested on Windows 8.1 (64-bit)
    - Tested on Windows 7 (32-bit)
    - Tested on Windows XP (32-bit)

* Linux
    - Tested on Ubuntu 12.10 (32-bit)

* Android
    - Tested on 2.3.6 (Motorola Defy)
    - Tested on 4.2.2 (Samsung Galaxy Note 8)

* MacOSX
    - Tested on 10.8.5

* iOS (TBD)

SOURCE CODE
-----------

    https://github.com/suriyan/iWriteIt

PRE-BUILD BINARIES VERSION
----------------

* Android
  
    [iWriteIt-0.9.0-debug.apk](https://www.dropbox.com/s/s3jthisv7a71ggd/iWriteIt-0.9.0-debug.apk)

* Windows 8/7/XP (Standalone executable file, includes all dependencies)

    [iWriteIt-0.9.0.exe](https://www.dropbox.com/s/3hmfl2mb9uj283m/iWriteIt-0.9.0.exe)
    
* Linux (Standalone executable file, but excludes `espeak` and `gstreamer`)

    [iWriteIt-0.9.0.bin](https://www.dropbox.com/s/2h6tn3kk27wn1h2/iWriteIt-0.9.0.bin)

    On Ubuntu you can install `espeak` and `gstreamer` with the following command :-

    ```
    sudo apt-get install espeak gstreamer0.10-plugins-good
    ```

* Mac OSX

    [iWriteIt-0.9.0.dmg](https://www.dropbox.com/s/bng1rnq27utdovk/iWriteIt-0.9.0.dmg)

    For more recently Pre-built binary version will available at :-

    https://www.dropbox.com/sh/csp47vb5v2xa22v/AADSU-9A7xXwhctxAV7dCYRCa

BUILD & PACKAGING
-----------------

* Windows / MacOSX / Linux (TBD)

    Using PyInstaller 2.1

    ```
    python ..\PyInstaller-2.1\pyinstaller.py bin\iWriteIt.spec
    ```

* Android (using Python for Android)

    ```
    ./build.py --dir /opt/projects/iWriteIt --name "iWriteIt" --package com.gurucafe.iwriteit --version 1.0.0 --orientation landscape --icon /opt/projects/iWriteIt/graphics/icon-128.png debug
    ```

    See http://kivy.org/docs/guide/packaging-android.html for more detail
    
* iOS (TBD)

    http://kivy.org/docs/guide/packaging-ios.html

CREDITS & ACKNOWLEDGEMENT
-------------------------

* Font http://www.f0nt.com/release/raingan/

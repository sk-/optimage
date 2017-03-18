Optimage
========

.. image:: https://badge.fury.io/py/optimage.svg
    :target: http://badge.fury.io/py/optimage

.. image:: https://travis-ci.org/sk-/optimage.svg?branch=master
    :target: https://travis-ci.org/sk-/optimage

.. image:: https://coveralls.io/repos/sk-/optimage/badge.svg?branch=master
    :target: https://coveralls.io/r/sk-/optimage?branch=master

Optimage optimizes JPEGs and PNGs by losslessly recompressing them and removing
unnecessary metadata (EXIF, comments, etc), making the web faster and your repo
smaller.

Optimizers
----------

- JPEG

  * `jpegtran <http://manpages.ubuntu.com/manpages/trusty/man1/jpegtran.1.html>`_
  * `jpegoptim <http://manpages.ubuntu.com/manpages/trusty/man1/jpegoptim.1.html>`_

- PNG

  * `pngcrush <http://manpages.ubuntu.com/manpages/trusty/man1/pngcrush.1.html>`_
  * `optipng <http://manpages.ubuntu.com/manpages/trusty/man1/optipng.1.html>`_


Example usage
-------------

  $ optimage test_data/valid1.png
  File can be losslessly compressed to 67 bytes (savings: 52 bytes = 43.70%)
  Replace it by running either:
    optimage --replace test_data/valid1.png
    optimage --output <FILENAME> test_data/valid1.png

  $ optimage --replace test_data/valid1.png
  File was losslessly compressed to 67 bytes (savings: 52 bytes = 43.70%)

  $ optimage --output /tmp/valid1.png test_data/valid1.png
  File was losslessly compressed to 67 bytes (savings: 52 bytes = 43.70%)


Installation
------------

You can install, upgrade or uninstall ``optimage`` with these commands::

  $ pip install optimage
  $ pip install --upgrade optimage
  $ pip uninstall optimage


Python Versions
---------------

Python 2.7, 3.3, 3.4 and 3.5 are supported.


Development
-----------

Help for this project is more than welcomed, so feel free to create an issue or
to send a pull request via http://github.com/sk-/optimage.

Tests are run using pytest, either with::

  $ python setup.py test
  $ pytest


Changelog
=========

v0.3.0 (2017-03-19)
----------

* Fixed #19: remove --lossy_8bit from zopflipng call
* Fixed #13: temporary files are removed after use

v0.2.0 (2016-02-08)
-------------------

* Added support for Python 2.7
* Added support for zopflipng
* Fixed #4: Images are now considered equal when alpha is 0 regardless of RGB.
* Fixed #6: Add --debug option to gather performance stats

v0.0.1 (2015-12-24)
-------------------

* Initial release with support for (jpegtran, jpegoptim, optipng, pngcrush)

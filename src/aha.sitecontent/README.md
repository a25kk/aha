# aha.sitecontent

## AHA 360 Sitecontent

* `Source code @ GitHub <https://github.com/kreativkombinat/aha.sitecontent>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/aha.sitecontent>`_
* `Documentation @ ReadTheDocs <http://ahasitecontent.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/kreativkombinat/aha.sitecontent>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

The generated Python package holds an example content type `ContentPage` which
provides a folderish version of the default **Page** document type.

The implementation is kept simple on purpose and asumes that the developer will
add further content manually.


## Installation

To install `aha.sitecontent` you simply add ``aha.sitecontent``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `aha.sitecontent` using the Add-ons control panel.

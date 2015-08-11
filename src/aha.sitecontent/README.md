# aha.sitecontent

## aha Site Content

* `Source code @ GitHub <https://github.com/potzenheimer/aha.sitecontent>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

The generated Python package hold the necessary scaffold to add content types
via the 'contenttype' template and to add functionality.

In order to get productive you still need to generate a contenttype

```bash
$ cd aha.sitecontent/src/ck/sitecontent/
$ mrbob --config ~/.mrbob.ini -O example_type bobtemplates:contenttype

```


## Installation

To install `aha.sitecontent` you simply add ``aha.sitecontent``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `aha.sitecontent` using the Add-ons control panel.

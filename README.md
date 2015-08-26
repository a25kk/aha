# buildout

## AHA 360 Website

* `Source code @ GitHub <https://github.com/a25kk/aha>`_
* `Documentation @ ReadTheDocs <http://aha.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/kreativkombinat/aha>`_

## How it works

This project templates provides a full blown Plone project environment. It comes with a preconfigured project specific theme package located under the _src_ directory.

## Installation

This buildout is intended to be used via the development profile to provide
a ready to work on setup. To get started with a new development environment
clone the buildout to your local machine and initialize the buildout:

``` bash
$ git clone git@github.com:username/aha.git
$ cd ./aha
$ virtualenv-2.7 .
$ ./bin/pip install zc.buildout
$ bin/buildout -Nc development.cfg
```

## Configuration

The generated buildout asumes that the developer has setup a local egg cache and therefore provides a buildout 'default.cfg'.

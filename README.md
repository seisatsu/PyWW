PyWW (Python Wiki Wiki)
=======================

PyWW, also known as Python Wiki Wiki, is a tiny, minimalistic wiki inspired by WW (http://www.moria.de/~michael/ww/).

This is a complete rewrite of the last release of this software in early 2012.

A lot of wiki software is overcomplicated. With databases and gratuitous configuration and CMS features, sometimes you
just wish you had a little less to work with. So, after stumbling upon a very small wiki project written in C, I
decided to make something similar in Python to give you less. A lot less. In fact, almost nothing.

PyWW is a tiny wiki in one file written in Python. It has very few features, no database, and almost no configuration
variables. The default page layout contains only text and an edit button, though this can be changed by modifying the
included template files. Simply install the script and navigate to it in your web browser to bootstrap the wiki.

PyWW pages are written in ReStructured Text. (See http://docutils.sourceforge.net/docs/user/rst/quickref.html)

Features
--------

* The software is self-contained in a single file.
* The script is less than 10kb in size.
* The wiki layout can be modified by changing simple template files.
* It's released under the MIT License for maximum freedom.

Requirements
------------

* Python 2 or 3

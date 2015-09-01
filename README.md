PyWW (Python Wiki Wiki)
=======================

https://github.com/pariahsoft/PyWW

PyWW, also known as Python Wiki Wiki, is a tiny, minimalistic wiki inspired by Ww (http://www.moria.de/~michael/ww/).

This is a complete rewrite of the last release of this software in early 2012.

A lot of wiki software is overcomplicated. With databases and gratuitous configuration and CMS features, sometimes you
just wish you had a little less to work with. So, after stumbling upon a very small wiki project written in C, I
decided to make something similar in Python to give you less. A lot less. In fact, almost nothing.

PyWW is a tiny wiki in one file written in Python. It has no extraneous features, no database, and only a few configuration variables. The default page layout contains only text and an edit button, though this can be changed by modifying the included template files. Simply install the script and associated template and css files onto a webserver, and navigate to the script in your browser to bootstrap the wiki. New pages are created by visiting and editing them.

You can also run PyWW easily from your local machine using thttpd (http://acme.com/software/thttpd/). (See below.)

Depending on your setup, you may need to edit the default configuration values at the top of the script.

PyWW pages are written in ReStructured Text. (See http://docutils.sourceforge.net/docs/user/rst/quickref.html)

Demo Wiki (wiped every 24 hours): http://pariahsoft.com/pyww/

Released under the MIT License.

Requirements
------------

* Python 2 or 3
* Python Docutils

Tips and Tricks
---------------

Linking to an external site:

    `PariahSoft <http://pariahsoft.com/>`_

Making a cross-page link named "Some Article" to the page named "thisone":

    `Some Article <?page=thisone>`_

To lock a page from editing, change its file permissions to read only. The edit interface will be automatically disabled and blocked for that page.

To erase the contents of a page, delete its file from the server or edit its contents to a single space.

You can run PyWW on your home machine with almost no setup! Simply install thttpd (http://acme.com/software/thttpd/), review the settings in the thttpd.sh spawn script, review the settings in index.cgi, and then run thttpd.sh while in the same directory. A PyWW instance will be hosted right there, accessible from your local web browser.

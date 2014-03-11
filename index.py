###################################
## PyWW - Python Wiki Wiki       ##
## index.py                      ##
## Copyright 2014 PariahSoft LLC ##
###################################

## **********
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to
## deal in the Software without restriction, including without limitation the
## rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
## sell copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
## IN THE SOFTWARE.
## **********

# Inspired by http://www.moria.de/~michael/ww/

import cgi
import cgitb
import os

from docutils.core import publish_parts

cgitb.enable()

### Configuration ###

###
# Whether or not page names are case sensitive. Changing this may break earlier pages.
#####
casesensitive = False

###
# The base URL directory of this script.
#####
baseurl = "/"

###
# The default/front page to show when none is specified.
#####
default = "index"

###
# Filename of the edit page template.
#####
edit_template = "edit.tpl"

###
# Filename of the view page template.
#####
page_template = "page.tpl"

###
# The relative or absolute path on the server to the directory where pages are kept.
#####
pagedir = "."

###
# Filename of the stylesheet to use.
#####
stylesheet = "style.css"

### End Configuration ###


class PyWW:
    def __init__(self, page, edit, newcontent):
        self.page = page
        self.edit = edit
        self.newcontent = newcontent

        self.content = ""
        self.httpheader = "Content-type: text/html; charset=utf-8\n\n"
        self.path = os.path.join(pagedir, self.page + ".rst")
        self.formatdict = {}

        # Figure out what to do next.
        self.route()

    def route(self):
        # Editing a page.
        if self.edit:
            self.read_page()
            self.build_edit()

        # Commiting an edit.
        elif self.newcontent:
            self.commit_edit()
            self.read_page()
            self.build_page()

        # Just viewing a page.
        else:
            self.read_page()
            self.build_page()

    def read_page(self):
        # Read an existing page.
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.content = f.read()

        # Create a new page.
        else:
            with open(self.path, "w") as f:
                pass

        self.formatdict = {
            "baseurl": baseurl,
            "content": self.content,
            "page": self.page,
            "rstparsed": publish_parts(self.content, writer_name="html")["html_body"],
            "stylesheet": stylesheet
        }

    def build_page(self):
        with open(page_template, "r") as f:
            tpl = f.read()

        print(tpl.format(**self.formatdict))

    def build_edit(self):
        with open(edit_template, "r") as f:
            tpl = f.read()

        print(tpl.format(**self.formatdict))

    def commit_edit(self):
        with open(self.path, "w") as f:
            f.write(self.newcontent)


def main():
    """This function reads the user request and invokes PyWW accordingly.
    """
    # Receive HTTP request fields.
    fields = cgi.FieldStorage()

    # Did the user request a page?
    if "page" in fields:
        page = fields["page"].value
    else:
        page = default

    # Case sensitivity?
    if not casesensitive:
        page = page.lower()

    # Is the user editing the page?
    if "edit" in fields:
        edit = True
    else:
        edit = False

    # Is the user submitting an edited page?
    if "newcontent" in fields:
        newcontent = fields["newcontent"].value
    else:
        newcontent = None

    # Hand this over to PyWW.
    PyWW(page, edit, newcontent)


# Run the script.
if __name__ == "__main__":
    main()

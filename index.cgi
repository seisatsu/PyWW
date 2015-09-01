#!/usr/bin/env python
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
import Cookie
import hashlib
import os
import random

from docutils.core import publish_parts

### Configuration ###

###
# Uncomment this line to enable error reporting on script failure.
#####
# import cgitb; cgitb.enable()

###
# Whether or not page names are case sensitive. Changing this may break earlier pages.
#####
casesensitive = False

###
# The domain (or subdomain) where the script is hosted.
#####
domain = "localhost"

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
# Filename of the ask password page template.
#####
askpass_template = "askpass.tpl"

###
# The relative or absolute path on the server to the directory where pages are kept.
#####
pagedir = "."

###
# Filename of the stylesheet to use.
#####
stylesheet = "style.css"

###
# If set, sha256-hashed password for accessing the wiki.
#####
passhash = ""

###
# HTML for the Edit button in unlocked and locked states.
#####
editbutton = ["<input class=\"button-edit pure-button\" type=\"submit\" value=\"Edit\" />", "<input class=\"pure-button pure-button-disabled\" type=\"button\" value=\"Locked\" />"]

### End Configuration ###


class PyWW:
    """PyWW (Python Wiki Wiki).
    """
    def __init__(self, page, edit, newcontent, cookie):
        """PyWW initializer.

        Arguments:
            page: Name of the page to view or edit.
            edit: Whether or not we are editing.
            newcontent: Either None or the content of an edit.
            cookie: Optional password hash cookie to pass to the user.
        """
        self.page = page
        self.edit = edit
        self.newcontent = newcontent
        self.cookie = cookie

        self.content = ""
        self.locked = False
        self.httpheader = "Content-type: text/html; charset=utf-8"
        self.path = os.path.join(pagedir, self.page + ".rst")
        self.formatdict = {}

        # Figure out what to do next.
        self.route()

    def route(self):
        """Perform the correct actions for the user's request.
        """
        # Send page headers and get cookies.
        print(self.httpheader)
        if self.cookie:
            print(self.cookie.output())
            cookie = self.cookie
        elif "HTTP_COOKIE" in os.environ:
            cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        else:
            cookie = {"passhash": None}
        # Finish the header with a newline.
        print("")
        
        # Check if password is required and/or wrong or already entered.
        if passhash and ((not cookie) or (not cookie["passhash"]) or (passhash != cookie["passhash"].value)):
            # Ask for password.
            self.read_page()
            self.ask_pass()
        
        # Password is correct or nonexistent, do whatever.
        else:
            # Editing a page.
            if self.edit:
                self.read_page()
                if not self.locked:
                    self.build_edit()
                else:
                    self.build_page()

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
        """Read the contents of a page from disk if it exists.
        """
        # Read an existing page.
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.content = f.read()

            # Test if the page is writable.
            try:
                with open(self.path, "a") as f:
                    pass

            except:
                self.locked = True

        # Set up the template formatting dictionary.
        try:
            rstparsed = publish_parts(self.content, writer_name="html", settings_overrides={'report_level':'quiet'})["html_body"]
        except:
            rstparsed = "!!!RST ERROR!!!"
        
        self.formatdict = {
            "baseurl": baseurl,
            "content": self.content,
            "page": self.page,
            "rstparsed": rstparsed,
            "stylesheet": stylesheet
        }
        if not self.locked:
            self.formatdict["editbutton"] = editbutton[0]
        else:
            self.formatdict["editbutton"] = editbutton[1]

    def ask_pass(self):
        """Build the page that asks for the password.
        """
        with open(askpass_template, "r") as f:
            tpl = f.read()

        print(tpl.format(**self.formatdict))

    def build_page(self):
        """Build the page view and deliver it to the user.
        """
        with open(page_template, "r") as f:
            tpl = f.read()

        print(tpl.format(**self.formatdict))

    def build_edit(self):
        """Build the page editor and deliver it to the user.
        """
        with open(edit_template, "r") as f:
            tpl = f.read()

        print(tpl.format(**self.formatdict))

    def commit_edit(self):
        """Commit an edit to the page.
        """
        try:
            with open(self.path, "w") as f:
                f.write(self.newcontent)

        except:
            pass


def main():
    """This function reads the user request and invokes PyWW accordingly.
    """
    # Retrieve HTTP request fields.
    fields = cgi.FieldStorage()

    # Did the user request a page?
    if "page" in fields:
        page = fields["page"].value
    else:
        page = default

    # Case sensitivity?
    if not casesensitive:
        page = page.lower()

    # Is the user entering a password?
    if "password" in fields:
        # Make a password hash cookie.
        cookie = Cookie.SimpleCookie()
        cookie["passhash"] = hashlib.sha256(fields["password"].value).hexdigest()
        cookie["passhash"]["domain"] = '.'+domain
        cookie["passhash"]["path"] = baseurl
    else:
        cookie = ""

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

    # Disallow certain dangerous characters.
    if '.' in page or '/' in page:
        page = default
        edit = False
        newcontent = None

    # Hand this over to PyWW.
    PyWW(page, edit, newcontent, cookie)


# Run the script.
if __name__ == "__main__":
    main()

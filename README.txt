PyWW (Python Wiki Wiki)
http://wiki.omegasdg.com/index.php?title=PyWW

PyWW, also known as Python Wiki Wiki, is a tiny, minimalistic wiki inspired by WW (http://www.moria.de/~michael/ww/).

Lots of wiki software is overcomplicated. With databases and gratuitous configuration and CMS features, sometimes you just wish you had a little less to work with. So, after stumbling upon a really small wiki project written in C, I decided to make something similar in Python to give you less. A lot less. In fact, almost nothing.

PyWW is a tiny wiki in one file written in Python. It has very few features, no database, and almost no configuration variables. The default page layout contains only text and an edit button, though this can be changed by modifying the included template files. Simply install the script and navigate to it in your web browser to bootstrap the wiki.

Supported Markup:
***Bold***
///Italic///
___Underline___
---Strikethrough---
==Heading==
===Subheading===
[[Wiki_Page_Name|Descriptive Text]]
[Link|Descriptive Text]
%nowiki%Disable Markup%nowiki%

Features:
* The software is self-contained in a single file.
* The script is less than 10kb in size.
* There are only a few configuration variables, inside the script itself.
* You don't even have to modify the configuration variables.
* The wiki layout can be modified by changing simple template files.
* It can back up previous versions of pages.
* It's released under the MIT License for maximum freedom.

Planned Features:
* Support named links.
* Built-in documentation with PyDoc.
* Optional password protection for pages.


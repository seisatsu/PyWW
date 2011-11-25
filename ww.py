############################
## PyWW - Python Wiki Wiki #
## By Michael D. Reiley    #
## Copyright 2011 OmegaSDG #
############################

# Python 2.X Minimal Wiki
# Inspired by http://www.moria.de/~michael/ww/

import cgi, sys, os, time, cgitb
cgitb.enable()

### Config Values ###

wikivars = ["TITLE", "CONTENT"] # Variables which must appear in a wiki file.
mainpage = "index.wiki" # Default page to show if none specified.
history = ["history/", True] # Page history directory, enabled or not.

### Initialization ###

if "REQUEST_METHOD" in os.environ: # Are we on a webserver?
	form = cgi.FieldStorage()
	action = form.getvalue("action")
	thispage = form.getvalue("page")
	if not thispage:
		thispage = mainpage
	content = form.getvalue("content")
	print "Content-type: text/html\n"
else: # No CGI capabilities.
	print >> sys.stderr, "Error: This script must be run on a CGI-capable server."
	sys.exit(1)

pyww = os.path.basename(__file__) # Name of pyww script.
globalvars = {"PYWW": pyww, "FILE": thispage} # Template required variables.
wiki = {}

### Preprocessors ###
# TODO: No-markup and custom variables.

def pp_simple(data, startmark, endmark, template, breaks): # For simple markup.
	"""General preprocessor for simple replace-what's-inside markup.
	* data: The page content to be processed.
	* startmark: The opening markup symbols.
	* endmark: The closing markup symbols.
	* template: A str.format() template; {0} replaced by the markup contained text.
	* breaks: True or False; allow linebreaks in the markup.
	* RETURN: Processed data."""

	pos = 0
	startpos = 0
	endpos = 0
	substr = ""

	while pos < len(data):
		if data[pos:pos+8] == "%nowiki%": # Markup is disabled here. Skip this.
			pos += 8
			while pos < len(data) and data[pos:pos+8] != "%nowiki%":
				pos += 1
			pos += 8
		if data[pos:pos+len(startmark)] == startmark: # Begin markup.
			startpos = pos
			pos += len(startmark)
			while pos < len(data) and data[pos:pos+len(endmark)] != endmark:
				substr += data[pos]
				pos += 1
			if pos < len(data): # Otherwise it was a bad markup, or we're done.
				if "<br />" in substr and not breaks: # No linebreaks allowed.
					pos += len(endmark)
					continue
				endpos = pos+len(endmark)
				newdata = replacerange(data, template.format(substr), startpos, endpos)
				data = pp_simple(newdata, startmark, endmark, template, breaks) # Recurse.
		pos += 1
	return data

def pp_link(data, startmark, endmark, template): # Process links.
	"""Similar to pp_simple, but allows two str.format() identifiers.
	* data: The page content to be processed.
	* startmark: The opening markup symbols.
	* endmark: The closing markup symbols.
	* template: A str.format() template; {0}, {1} replaced by dest, description.
	* RETURN: Processed data."""

	inttemp = "<a href=\""+pyww+"?page={0}\">{1}</a>"
	exttemp = "<a href=\"{0}\">{1}</a>"
	pos = 0
	startpos = 0
	endpos = 0
	substr = ""
	
	while pos < len(data):
		if data[pos:pos+8] == "%nowiki%": # Markup is disabled here. Skip this.
			pos += 8
			while pos < len(data) and data[pos:pos+8] != "%nowiki%":
				pos += 1
			pos += 8
		if data[pos:pos+len(startmark)] == startmark: # Begin link markup.
			startpos = pos
			pos += len(startmark)
			while pos < len(data) and data[pos:pos+len(endmark)] != endmark:
				substr += data[pos]
				pos += 1
			if pos < len(data): # Otherwise it was a bad markup, or we're done.
				if "<br />" in substr: # No linebreaks allowed.
					pos += len(endmark)
					continue
				substr = substr.split("|")
				if len(substr) != 2: # Bad markup.
					substr = ""
					pos += 1
					continue
				endpos = pos+len(endmark)
				newdata = replacerange(data, template.format(substr[0], substr[1]), startpos, endpos)
				data = pp_link(newdata, startmark, endmark, template) # Recurse.
		pos += 1
	return data

def pp_vars(data): # Process custom variables from content.
	pos = 0
	substr = ""
	newvars = {}

	while pos < len(data):
		if data[pos:pos+8] == "%nowiki%": # Markup is disabled here. Skip this.
			pos += 8
			while pos < len(data) and data[pos:pos+8] != "%nowiki%":
				pos += 1
			pos += 8
		if data[pos] == "{": # Begin variable markup.
			pos += 1
			while pos < len(data) and data[pos] != "}":
				substr += data[pos]
				pos += 1
			if pos < len(data): # Otherwise it was a bad markup, or we're done.
				substr = substr.split(":")
				if len(substr) != 2: # Bad markup.
					substr = ""
					pos += 1
					continue
				newvars[substr[0]] = substr[1] # Merge in new variable.
				substr = ""
		pos += 1
	return dict(wiki.items() + newvars.items())

def pp_escape(data): # Escape common HTML entities.
	data = data.replace("&", "&amp;") # Must be first.
	data = data.replace("<", "&lt;")
	data = data.replace(">", "&gt;")
	data = data.replace("\"", "&quot;")
	data = data.replace("\'", "&#39;")
	return data

def pp_strip(data): # Strip linebreaks from top of page.
	while True:
		if data[0:6] == "<br />":
			data = data[6:]
		else:
			return data

### Helper Functions ###

def replacerange(string, newstring, startpos, endpos):
	return string[:startpos] + newstring + string[endpos:]
	
def preprocess(data): # Preprocess wiki file content for markup and such.
	# Replace newlines with <br />.
	data = data.replace("\r\n", "<br />")
	data = data.replace("\n\r", "<br />")
	data = data.replace("\r", "<br />")
	data = data.replace("\n", "<br />")

	# Links, internal and external.
	data = pp_link(data, "[[", "]]", "<a href=\""+pyww+"?page={0}\">{1}</a>")
	data = pp_link(data, "[", "]", "<a href=\"{0}\">{1}</a>")
	
	# Miscellaneous markup.
	data = pp_simple(data, "***", "***", "<b>{0}</b>", True) # Bold
	data = pp_simple(data, "///", "///", "<i>{0}</i>", True) # Italic
	data = pp_simple(data, "___", "___", "<u>{0}</u>", True) # Underline
	data = pp_simple(data, "---", "---", "<s>{0}</s>", True) # Strikethrough
	data = pp_simple(data, "===", "===", "<span style=\"font-size: 1.5em;\">{0}</span>", False) # Subheading
	data = pp_simple(data, "==", "==", "<span style=\"font-size: 2em;\">{0}</span>", False) # Heading
	
	# Don't show custom variables.
	data = pp_simple(data, "{", "}", "", False)
	
	# Strip linebreaks from top of page.
	data = pp_strip(data)
	
	# Clean up nomarkup tags.
	data = data.replace("%nowiki%", "")

	return data

def read_wiki(page): # Read in page data from wiki file.
	if os.path.exists(page):
		f = open(page, "r")
		w = f.read()
		exec(w, {"__builtins__": None}, {"wiki": wiki}) # Safe exec.
		f.close()
	else: # The file doesn't exist yet. Return a blank page that can be saved.
		for var in wikivars:
			wiki[var] = " "

def build_page(): # Build this page from page data.
	allvars = dict(globalvars.items() + wiki.items()) # Variables to read.
	f = open("page.tpl", "r")
	tpl = f.read()
	f.close()
	allvars["CONTENT"] = preprocess(allvars["CONTENT"]) # Preprocess the wiki content for markup and such.
	print tpl.format(**allvars) # Process the template file and show the page.

def build_edit(): # Build the edit form for this page.
	allvars = dict(globalvars.items() + wiki.items()) # Variables to read.
	f = open("edit.tpl", "r")
	tpl = f.read()
	f.close()
	print tpl.format(**allvars) # Process the template file and show the page.
	
def build_wiki(): # Build a wiki file from page data.
	global wiki
	data = ""

	wiki = pp_vars(wiki["CONTENT"]) # Add custom variables.
	for var in wiki: # Write values to the wiki file.
		if not wiki[var]:
			wiki[var] = " "
		if var == "CONTENT" or var == "TITLE": # HTML should be escaped.
			data += "wiki[\"{0}\"] = '''{1}'''\n".format(var, pp_escape(wiki[var]))
		else:
			data += "wiki[\"{0}\"] = '''{1}'''\n".format(var, wiki[var])
	f = open(thispage, "w")
	f.write(data)
	f.close()
	if history[1]: # History enabled, write unix timestamped backup file.
		f = open(history[0]+"/"+thispage+"."+str(int(time.time())), "w")
		f.write(data)
		f.close()

### Main ###

def main():
	if content: # An edit was just submitted.
		read_wiki(thispage)
		wiki["CONTENT"] = content
		build_wiki()
		read_wiki(thispage) # Refresh after writing wiki file.
		build_page()
	else:
		if action == "edit": # Edit the page.
			read_wiki(thispage)
			build_edit()
		else: # Show the page.
			read_wiki(thispage)
			build_page()

main()


# YourToDo
Productivity tool for daily, weekly, and monthly planning


To Contribute:

For this project, we're going to use a webframework called Django, and an extension to this framework, mezzanine. Mezzanine is a content management system (cms) which makes it easy to modify content on the website. While we won't be using this functionality too much, it will come in handy. This package extends the django framework which will be vital to our user and database needs. Here's what I did to get started.

Install Python, if you haven't. Visit https://www.python.org/ and download Python 3.5. When prompted, click yes to add python to the PATH variable.

Afterwards, head to the command prompt and type the following command:

pip install mezzanine

This command installs mezzanine and django, as well as a few other packages.

There's one minor change we have to make for mezzanine to work with Python 3.5:

Find where mezzanine is installed, and navigate to mezzanine/utils/ and open the html.py file in a text editor. The following should be preset on lines 5 & 6:

	from html.parser import HTMLParser, HTMLParseError
	from html.entities import name2codepoint

Replace the above code with the following code:

    from html.parser import HTMLParser
    from html.entities import name2codepoint
    try:
        from html.parser import HTMLParseError
    except ImportError:  # Python 3.5+
        class HTMLParseError(Exception):
            pass

This change will solve an import error with python when attempting to run the server.
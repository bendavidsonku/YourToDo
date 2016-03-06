# YourToDo
Productivity tool for daily, weekly, and monthly planning

Git Agreement:
Master should always be left in a functional state. That is to say, there should never be any actual development happening directly on the Master branch. Any development should be done on a separate branch and these branches should be named in a consistent manner. For this project, we will be naming our branches off of master WIPS or "works in progress." For example, if a developer is attempting to create a workflow, he would create a new branch off of the Master named wip/workflow and then only commit changes to that branch. 

Upon finishing the feature that the developer is working on, he will then initiate a pull request to merge his WIP into Master. All other developers must comment approval in github before the owner of the branch should merge his pull request into Master in order to keep Master as up-to-date and functional as possible. 



To Contribute:

For this project, we're going to use a webframework called Django, and an extension to this framework, mezzanine. Mezzanine is a content management system (cms) which makes it easy to modify content on the website. While we won't be using this functionality too much, it will come in handy. This package extends the django framework which will be vital to our user and database needs. Here's what I did to get started.

Install Python, if you haven't. Visit https://www.python.org/ and download Python 3.5. When prompted, click yes to add python to the PATH variable.

Afterwards, head to the command prompt and type the following command:

pip install mezzanine

This command installs mezzanine and django, as well as a few other packages.

There's one minor change we have to make for mezzanine to work with Python 3.5:

Find where mezzanine is installed, and navigate to mezzanine/utils/ and open the html.py file in a text editor. 

Copy the html.py file from the shared Google Drive folder into your mezzaine/utils folder (replacing the current html.py file)


This change will solve an import error with python when attempting to run the server.

Updated 3/5/2016: need to install python dateutil using pip install python-dateutil --upgrade
We're also using django registration redux, python social auth
#!/usr/bin/env python

# Written by Andrew MacDougall Oct. 28, 2013
# This program accepts a text file as input and 
# uploads it to Evernote. This is to be able to take notes in emacs and then
# easily upload them to Evernote, perhaps even automatically at the end of the
# day, so this program is a piece of that puzzle. Adapted from the sample code 
# included in the python SDK.

# There was a nice tutorial in this code on how to add resources such as images to
# programs. Get the sample one back to see this.

# NOTE - I AM OUT OF SANDBOX AND IN TO PRODUCTION

# THINGS TO ADD AFTER BASIC FUNCTIONALITY IS COMPLETE:
# 1) In textfile include information that can be parsed that
# indicates which notebooks/tags should be included as well as
# the title of the note. 
# Organize the code better - there are plenty of things in here that have
# good potential for reuse.
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import sys
from evernote.api.client import EvernoteClient

# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account. To get a developer token, visit
# https://sandbox.evernote.com/api/DeveloperToken.action
#FILLED IN BY ME FOR TESTING PURPOSES
auth_token = ""

if auth_token == "your developer token":
    print "Please fill in your developer token"
    print "To get a developer token, visit " \
        "https://sandbox.evernote.com/api/DeveloperToken.action"
    exit(1)

# Initial development is performed on our sandbox server. To use the production
# service, change sandbox=False and replace your
# developer token above with a token from
# https://www.evernote.com/api/DeveloperToken.action
client = EvernoteClient(token=auth_token, sandbox=False)

user_store = client.get_user_store()

version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
print "Is my Evernote API version up to date? ", str(version_ok)
print ""
if not version_ok:
    exit(1)


note_store = client.get_note_store()

# We need a function that will convert new line characters, 
# \n for instance, to <br/> which will make a new line in 
# Evernote.
# str is a string whose newline characters will be removed.
# returns the fixed string.
def replace_new_lines_with_br(str):
    strNew = str.replace("\n", "<br/>")
    return strNew

# The title can't have new lines characters in it, nor should it
# nor should it have <br> in it. This just gets rid of that.
# str is a string with the unformatted title. Returns properly 
# formatted title
def format_title(str):
    strNew = str.replace("\n", "")
    return strNew


# Store user's notebooks.
notebooks = note_store.listNotebooks()

#Store user's tags.


# List all of the notebooks in the user's account
def listNotebooks():
    print "Found ", len(notebooks), " notebooks:"
    for notebook in notebooks:
        print "  * ", notebook.name



# Here is the part that really is my own work, simple as it may be,
# reading in the text file!
# First, we need a new file object.
# sys.argv[1] is the command line argument passed (remember sys.argv[0]
# is the program name), and r means that we are only going to be reading
# the file. 
def create_formatted_notpe(filename):
    file_object = open(filename,'r')
    noteTitle = file_object.readlines()
    realTitle = noteTitle[0]
    message = ""
    for i in range(1,len(noteTitle)):
        message += noteTitle[i]
    
    
    # To create a new note, simply create a new Note object and fill in
    # attributes such as the note's title.
    note = Types.Note()
    #note.title=noteTitle[0]
    note.title=format_title(noteTitle[0])


    # The content of an Evernote note is represented using Evernote Markup Language
    # (ENML). The full ENML specification can be found in the Evernote API Overview
    # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
                '"http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note> '
    for i in range (1,len(noteTitle)):
        note.content += replace_new_lines_with_br(noteTitle[i]) #adds text file content to note.
    note.content += '</en-note>'

    # Finally, send the new note to Evernote using the createNote method
    # The new Note object that is returned will contain server-generated
    # attributes such as the new note's unique GUID.
    created_note = note_store.createNote(note)

    print "Successfully created a new note with GUID: ", created_note.guid


#Now we run the above create_formatted_note on all of the command line arguments
for i in range(1, len(sys.argv)):
    create_formatted_note(sys.argv[i])


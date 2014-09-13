import sys
import os
import os.path

import sgmllib

class ReutersSGMLParser(sgmllib.SGMLParser):

    def __init__(self, filePath, verbose=1):
        sgmllib.SGMLParser.__init__(self, verbose)
        f = open(filePath, "r")
        self.file_string = f.read()

        self.in_title = 0
        """Flag indicating whether or not we're parsing the title."""

        self.in_dateline = 0
        """Flag indicating whether or not we're parsing the dateline"""

        self.in_body = 0
        """Flag indicating whether or not we're parsing the body"""
        self.in_topic = 0

        self.in_places = 0

        self.title = ""
        """Title of the document"""

        self.doc_id = 0
        """Document ID"""

        self.dateline = ""
        """Date line for the document"""

        self.body = ""
        """Body of the document"""

        self.topics = []
        self.docs = []
        self.places = []

    def parse(self):

        """Parse the given string 's', which is an SGML encoded file."""

        self.docs = []
        self.feed(self.file_string)
        self.close()

    def get_parsed_docs(self):
        return self.docs

    #handle_data method is called in between start_<tag> and end_<tag>
    def handle_data(self, data):
        """Print out data in TEXT portions of the document."""

        if self.in_body:
            self.body += data
        elif self.in_title:
            self.title += data
        elif self.in_dateline:
            self.dateline += data
        elif self.in_topic:
            self.topics.append(data)
        elif self.in_places:
            self.places.append(data)


    ####
    # Handle the Reuters tag
    ####
    def start_reuters(self, attributes):
        """Process Reuters tags, which bracket a document. Create a new
        file for each document encountered.
        """

        for name, value in attributes:
            if name == "newid":
                self.doc_id = value

    def end_reuters(self):
        """Write out the contents to a file and reset all variables."""

        from textwrap import fill
        import re

        # Print out the contents to a file. For the body of the
        # text, merge into 70 character lines using python's fill
        # utility
        """
        filename = "text/" + str(self.doc_id) + ".txt"
        doc_file = open(filename, "w")
        doc_file.write(self.title + "\n")
        doc_file.write(self.dateline + "\n")
        # Strip out multiple spaces in the body
        self.body = re.sub(r'\s+', r' ', self.body)
        doc_file.write(fill(self.body) + "\n")
        doc_file.close()
        """

        # lets cleanup the topics variable a bit by converting to a list
        self.docs.append({'title' : self.title, 'dateline': self.dateline, 'body' : self.body, 'topics' : self.topics})

        # Reset variables
        self.in_title = 0
        self.in_dateline = 0
        self.in_body = 0
        self.in_topic = 0
        self.doc_id = 0
        self.in_places = 0

        self.title = ""
        self.body = ""
        self.dateline = ""
        self.topics = []
        self.places = []

    ####
    # Handle TITLE tags
    ####
    def start_title(self, attributes):
        """Indicate that the parser is in the title portion of the document."""

        self.in_title = 1

    def end_title(self):
        """Indicate that the parser is no longer in the title portion of the document."""

        self.in_title = 0

    ####
    # Handle PLACES tags
    ####
    def start_places(self, attributes):
        """Indicate that the parser is in the title portion of the document."""

        self.in_places = 1

    def end_places(self):
        """Indicate that the parser is no longer in the title portion of the document."""

        self.in_places = 0

    ####
    # Handle DATELINE tags
    ####
    def start_dateline(self, attributes):
        """Indicate that the parser is in the dateline portion of the document."""

        self.in_dateline = 1

    def end_dateline(self):
        """Indicate that the parser is no longer in the dateline portion of the document."""

        self.in_dateline = 0

    ####
    # Handle BODY tags
    ####
    def start_body(self, attributes):
        """Indicate that the parser is in the body portion of the document.
        """

        self.in_body = 1

    def end_body(self):
        """Indicate that the parser is no longer in the body portion of the document."""

        self.in_body = 0

    ####
    # Handle TOPIC tags
    ####
    def start_topics(self, attributes):
        """Indicate that the parser is in the topics portion of the document."""

        self.in_topic = 1

    def end_topics(self):
        """Indicate that the parser is no longer in the topics portion of the document."""

        self.in_topic = 0



def main():
    print 'hello'
    p = ReutersSGMLParser('/home/shridhar/Acads/CSE5423/Project/Datasets/reut2-000.sgm')
    p.parse()
    parsed_docs = p.get_parsed_docs()
    for doc in parsed_docs:
        print doc['topics']

if __name__ == "__main__": main()

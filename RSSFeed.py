"""
Simple RSS generator

Copyright (C) 2015  Jan Schmidt

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__name__ = "RSSFeed"

import sys
version = sys.version_info[0] + 0.1 * sys.version_info[1]
try:
    import datetime
except ImportError:
    print("Error datetime must be installed")
    sys.exit()

if version >= 3.3:
    import xml.etree.ElementTree as ETree
else:
    import xml.etree.cElementTree as ETree


def _timeFormat(time):
    """Return a string in the correct format
    Note, in python >= 3.4 this can be replaced by datetime.timestamp()
    TODO: Replace the fixed GMT
    """
    return "{}, {:02} {} {} {:02}:{:02}:{:02} GMT".format(
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][time.weekday()],
            time.day,
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul","Aug", "Sep", "Oct", "Nov", "Dec"][time.month - 1],
            time.year,
            time.hour, time.minute, time.second)

def _addSubElement(parent, name, text, attribute = None):
    child = ETree.SubElement(parent, name, attribute)
    child.text = text
    return child

class RSSFeed(object):
    def __init__(self, title, link, description,
            language = None, pubDate = None):
        self.rss = ETree.Element("rss", {"version": "2.0"})
        self.feed = ETree.ElementTree(self.rss)
        self.channel = ETree.SubElement(self.rss, "channel")
        self.title = _addSubElement(self.channel, "title", title)
        self.link = _addSubElement(self.channel, "link", link)
        self.description = _addSubElement(self.channel, "description", description)
        if language != None:
            self.language = _addSubElement(self.channel, "language", language)
        if pubDate != None:
            self.pubDate = _addSubElement(self.channel, "pubDate", _timeFormat(pubDate))

        self.items = []

    def addItem(self, title, link, description,
            pubDate = None, guid = None, author = None, category = None):
        item = ETree.SubElement(self.channel, "item")
        item_title = _addSubElement(item, "title", title)
        item_link = _addSubElement(item, "link", link)
        item_description = _addSubElement(item, "description", description)

        if guid == None:
            item_guid = _addSubElement(item, "guid", link)
        else:
            item_guid = _addSubElement(item, "guid", guid, {"isPermaLink": "false"})

        if pubDatei != None:
            item_pubDate = _addSubElement(item, "pubDate", _timeFormat(pubDate))
        if author != None:
            item_autor = _addSubElement(item, "author", author)
        if category != None:
            item_category = _addSubElement(item, "category", category)

        self.items.append(item)

    def writeRSS(self, filename):
        self.feed.write(filename, encoding = "unicode")

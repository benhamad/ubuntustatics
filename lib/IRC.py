import sys
import re
import collections
import requests
from helper import daterange, progressbar
import pygal


class IRC():
    """IRC Class"""
    def __init__(self, channel):
        self.channel = channel
        self.baseUrl = "http://irclogs.ubuntu.com/{}/{:02d}/{:02d}/%23{}.txt"
        self.NickChangingRegex = re.compile("^=== (.*?) is now known as (.*?)$")
        self.NickName = re.compile("<(.*?)>")  


    def GetIRCLines(self,url):
        """Return a generator that contain all lines in the requested URL""" 
        r = requests.get(url)
        if r.status_code != 200:
            # escape error 
            return None
        return r.iter_lines()

    def NumberOfmsgPerDay(self, url):
        r =  self.GetIRCLines(url)
        nicks = collections.Counter()
        if r != None:
            for l in r:
                if "is now known" in l:
                    # Check if someone change his nick 
                    oldNick, NewNick = self.NickChangingRegex.findall(l)[0]
                    try:
                        nicks[NewNick] = nicks.pop(oldNick)
                    except KeyError:
                        # This happen if if someone with no previous msg change his nick.
                        nicks[NewNick]=0
                elif "<" in l :
                    nick = self.NickName.findall(l)[0]
                    if nick in nicks:
                        # If nick existe increment msg count.
                        nicks[nick] += 1
                    else:
                        # Else add the nick to counter.
                        nicks[nick]=1
        return nicks

    def GetNumberofMsgPerDate(self, startDate, endDate):
        """ Return number of msg per user between startDate and endDate"""
        self.startDate = startDate
        self.endDate = endDate
        NumberOfmsgPerYear = collections.Counter()
        numberOfDays, i = (endDate - startDate).days , 0
        for year, month, day in daterange(startDate, endDate):
            url = self.baseUrl.format(year, month, day, self.channel)
            NumberOfmsgPerYear +=  self.NumberOfmsgPerDay(url)
            # Progress bar 
            i+= 1
            progressbar(i, numberOfDays)
        # Return first 10 users
        self.d =  NumberOfmsgPerYear.most_common(10)
        return NumberOfmsgPerYear

    def render(self, fileName):
        pie_chart = pygal.Pie()
        pie_chart.title = self.channel +" users partictipation "+ str(self.startDate)+" untill "+str(self.endDate)
        with open(fileName, 'w') as f:
            for person, numberofmsg in self.d:
                pie_chart.add(person, numberofmsg)
            f.write(pie_chart.render())

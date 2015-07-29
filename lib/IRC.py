import sys
import re
import collections
import requests
from helper import daterange, progressbar
import pygal


class IRC():
    """IRC Class"""
    def __init__(self, channel, startDate, endDate):
        self.channel = channel
        self.startDate = startDate
        self.endDate = endDate
        self.baseUrl = "http://irclogs.ubuntu.com/{}/{:02d}/{:02d}/%23{}.txt"
        self.NickChangingRegex = re.compile("=== (.*?) is now known as (.*?)(?:$|\n)")
        self.NickName = re.compile("<(.*?)>")  

    def GetIRCLines(self,url):
        """Return a generator that contain all lines in the requested URL""" 
        r = requests.get(url)
        if r.status_code != 200:
            # escape error 
            return None
        return r.iter_lines()

    def NumberOfmsgPerDayPerUser(self, url):
        r =  self.GetIRCLines(url)
        nicks = collections.Counter()
        if r != None:
            for l in r:
                if "is now known" in l and l.startswith("==="):
                    # Check if someone change his nick 
                    oldNick, NewNick = self.NickChangingRegex.findall(l)[0]
                    try:
                        nicks[NewNick] = nicks.pop(oldNick)
                    except KeyError:
                        # If someone with no previous msg change his nick.
                        nicks[NewNick]=0


                elif "] <" in l :
                    nick = self.NickName.findall(l)[0]
                    if nick in nicks:
                        # If nick existe increment msg count.
                        nicks[nick] += 1
                    else:
                        # Add the nick to counter.
                        nicks[nick]=1
        return nicks


    def topTenUsers(self):
        """ Top ten users between startDate and endDate"""
        NumberOfmsgPerYear = collections.Counter()
        numberOfDays, i = (self.endDate - self.startDate).days , 0

        # Count number of msg for each user from starDate until endDate
        for year, month, day in daterange(self.startDate, self.endDate):
            url = self.baseUrl.format(year, month, day, self.channel)
            NumberOfmsgPerYear +=  self.NumberOfmsgPerDayPerUser(url)
            # Progress bar 
            i+= 1
            progressbar(i, numberOfDays)

        # Only first 10 users
        d =  NumberOfmsgPerYear.most_common(10)

        # Prepare the pie chart
        pie_chart = pygal.Pie()
        pie_chart.title ="{} users partictipation form {} untill {}".format(self.channel,
                                                                            str(self.startDate),
                                                                            str(self.endDate)
                                                                            )
        for person, numberofmsg in d:
            pie_chart.add(person, numberofmsg)

        # Save it
        with open("{}-top-10.svg".format(self.channel), 'w') as f:
            f.write(pie_chart.render())

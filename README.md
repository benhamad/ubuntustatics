# Ubuntustatics

Generate [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) pie chart
file that list top 10 users of given ubuntu channel.


## How to use it:

    $ ./ubuntustatics.py -h


    usage: ubuntustatics.py [-h] channel startDate endDate

    positional arguments:
      channel     IRC Channel name
      startDate   First date to parse in the form of month-day-year
      endDate     Last date to parse in the form of month-day-year

    optional arguments:
      -h, --help  show this help message and exit



**Example**

    $ ./ubuntustatics.py ubuntu-tn 07-01-2015 07-30-2015
   
Than you can open the svg file with your browser.


## Dependencies:

[requests](http://www.python-requests.org/en/latest/)

    $ pip install requests

[pygal](http://pygal.org/)

    $ pip install pygal

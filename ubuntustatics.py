#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib import IRC
from datetime import date


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("channel", help="IRC Channel name")
    parser.add_argument("startDate", help="First date to parse in the form of month-day-year")
    parser.add_argument("endDate", help="Last date to parse in the form of month-day-year")
    args = parser.parse_args()

    # Prepare dates
    month, day, year = map(int, args.startDate.split("-"))
    start_date = date(year, month, day)
    month, day, year = map(int, args.endDate.split("-"))
    end_date = date(year, month, day)

    # Using the IRC class
    channel = IRC.IRC(args.channel, start_date, end_date)
    # Top ten users
    channel.topTenUsers()
   

if __name__ == '__main__':
    main()

from datetime import timedelta
from sys import stdout

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        d = start_date + timedelta(n)
        yield d.year, d.month, d.day

def progressbar(progress, full, width = 50):
    stdout.write("\r[" + "#" * (width * progress/full) + " " * (width * (full-progress) / full) 
            + "] " + str((float(progress)/full)*100) + "%")
    stdout.flush()

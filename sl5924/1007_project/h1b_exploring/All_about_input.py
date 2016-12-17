"""
This module is responsible for all input and output. 


Author: Sheng Liu (sl5924)

"""
import pandas as pd
import sys
from time import sleep
from h1b_exploring.exception_list import *

def h1bdata_loading():
    """
    used at the start of main function. safely input the data set from the external csv file.
    Raise exception when input failed

    return
    ======
    a verified DataFrame

    """
    string = 'Welcome to Our H1b Analysis System! \n'
    delay_print(string)
    print ("loading data......")
    i = 0
    l = 7
    printProgress(i, l, prefix = 'Progress:', suffix = '', barLength = 50)
    data = {}
    for year in range(2010,2017):
        data[year]= pd.read_csv('DataBase/H-1B_FY'+str(year)+'_clean.csv', encoding = 'iso-8859-1')
        i = year-2009
        printProgress(i, l, prefix = 'Progress:', suffix = '', barLength = 50)
    print ("\ndataset loaded successfully >>>")
    return data



def option_input():
    """
    used at every menu, safely input all options, raise and pass exceptions when input invalid.

    return
    ======
    a verified option

    """

    key = input("Please select one: ")
    options = list('abcdr')
    
    if key == 'quit':
        print ("You have quited the system.")
        sys.exit()
    
    if not(key in options):
        raise wrong_option_exception
    return key

def delay_print(s):
    """
    used at the begin of the program to print sentences like writting.

    """
    for c in s:
        sys.stdout.write( '%s' % c )
        sys.stdout.flush()
        sleep(0.15)
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    # Scource: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console by @Vladimir
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def get_input(path):
    """
    given a file path, verify the input dataset
    argument
    ========
    path: string showing the path of .csv file

    return
    ======
    checked dataframe
    """

    df = pd.read_csv(path)
    attributes = [u'YEAR', u'CASE_NUMBER', u'STATUS', u'VISA_CLASS', u'EMPLOYER_NAME', u'EMPLOYER_CITY',
             u'EMPLOYER_STATE', u'SOC_CODE', u'SOC_NAME', u'JOB_TITLE', u'PREVAILING_WAGE',
             u'FULL_TIME']

    for col in df.columns:
        if not(col in attributes):
            raise wrong_dataset_exception
    return df
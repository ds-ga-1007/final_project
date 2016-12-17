'''Generates the filtered data from the raw data'''

import glob
from RawDataFilter import RawDataFilter

def main() :
    '''Cleans and filters raw data for efficient access'''
    path = r'./Data/'
    outfile = r'./FilteredData/filteredData.csv'
    allFiles = glob.glob(path + "/Storm*.csv")
    dataFilter = RawDataFilter()
    dataFilter.loadData(allFiles)
    dataFilter.writeFilteredData(outfile)

if __name__ == '__main__' :
    main()


'''
This module was run before deployment to generate the predicted labels for songs provided in the package. It was run to
generate the df_toplot.csv file that will be used in the main program. Note that column 'Prediction' in df_toplot stores
the predicted label, with 1 being Jazz and 0 being Classical.

Created on Dec 11, 2016
@author: ShashaLin
'''
import os
from Classifier import * 
from Classify import *
from midi_to_dataframe import *
from process_master import *

cwd = os.getcwd()
package_path = cwd + '/ToClassify'

df_toClassify = process_master(package_path, 2).result()
toClassify = featureExtract(df_toClassify)
prediction = toPredict(toClassify)
toClassify['Prediction'] = prediction #toClassify is a df with each song we provided as a row, some melody and time
#features used for classification, as well as the predicted label.

forMerge = toClassify.drop(['Time_sequence', 'Percussion_time', 'Melody'], 1)
df_toplot = df_toClassify.merge(forMerge, how = 'left') #This is a comprehensive df with each midi message of each
#provided song as a row, with predicted labels added as a new column. Can be easily used for plotting. Keep in mind
#that 'Prediction' stores the result, with 1 being Jazz and 0 being classical.
df_toplot.to_csv('df_toplot.csv')
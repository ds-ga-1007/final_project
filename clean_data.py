import pandas as pd
import os

#################
##Read the data##
#################

# Import os to get or change the working directory
# The working path is usually like '.../py_project'
# Data will be stored in or loaded from '.../py_project/data'
# Use os.chdir() to change directory to data folder
os.chdir("data")
data_path = os.getcwd()
rank_path = data_path + '/cwurdata.xlsx'
score_path = data_path + '/Most-Recent-Cohorts-All-Data-Elements.xlsx'
complete_path = data_path + '/complete_data.xlsx'

data_rank = pd.read_excel(rank_path,"Sheet1")
data_score = pd.read_excel(score_path,"Sheet1")
merge_data=pd.merge(data_rank,data_score, how="inner", on=["UNITID"])   
complete_data=merge_data[['INSTNM','WR2016', 'WR2015', 'WR2014','NR2016', 'NR2015', 'NR2014','CITY','STABBR','ZIP','LATITUDE','LONGITUDE','INSTURL','ADM_RATE','ADM_RATE_ALL','SATVR25','SATVR75','SATMT25','SATMT75','SATWR25','SATWR75','SATVRMID','SATMTMID','SATWRMID','ACTCM25','ACTCM75','ACTEN25','ACTEN75','ACTMT25','ACTMT75','ACTWR25','ACTWR75','ACTCMMID','ACTENMID','ACTMTMID','ACTWRMID','COSTT4_A','MD_EARN_WNE_P10','PCT10_EARN_WNE_P10','PCT25_EARN_WNE_P10','PCT75_EARN_WNE_P10','PCT90_EARN_WNE_P10','MD_EARN_WNE_P6','PCT10_EARN_WNE_P6','PCT25_EARN_WNE_P6','PCT75_EARN_WNE_P6','PCT90_EARN_WNE_P6','MD_EARN_WNE_P8','PCT10_EARN_WNE_P8','PCT25_EARN_WNE_P8','PCT75_EARN_WNE_P8','PCT90_EARN_WNE_P8','UG25ABV','CRIME2014', 'CRIME2013', 'CRIME2012','CRIME2011', 'CRIME2010', 'CRIME2009', 'CRIME2008', 'CRIME2007','CRIME2006', 'CRIME2005', 'CRIME2004', 'CRIME2003', 'CRIME2002','CRIME2001','UNITID']]
##################################
#Fill the writing socre NaN by 0##
##################################
FILL=complete_data[['INSTNM','SATWR25','SATWR75','SATWRMID','ACTWR25','ACTWR75','ACTMTMID']].fillna(0)
drop_data=complete_data.drop(['SATWR25','SATWR75','SATWRMID','ACTWR25','ACTWR75','ACTMTMID'],1)
data=pd.merge(drop_data,FILL,on='INSTNM')
data.to_excel(complete_path)

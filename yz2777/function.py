import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#############################################
##Search the subdata according to SAT score##
#############################################
#Justify if the input is valid
def justify_SAT_score(score):
    #flag=0 indicates input is valid, flag=1 indicates input is wrong
    flag=0;
    if(score.isdigit()==False):
        flag=1;
    else:
        if(int(score)>800):
            flag=1;
    return flag


#Find the top 10 available colleges by SAT score
def search_SAT(data):
    data_3="The user quit the program"
    #Justify if the SAT reading socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
    score_SAT_VR=input("Please enter your SAT reading socre. The score range from 0 to 800. Finish the program by entering quit\n");
    flag_1=justify_SAT_score(score_SAT_VR);
    while(flag_1==1 and score_SAT_VR!='quit'):
        score_SAT_VR=input("The last input is not valid. Please enter your SAT reading socre. The score range from 0 to 800. Finish the program by entering quit\n");
        flag_1=justify_SAT_score(score_SAT_VR);
    #If the SAT reading socre is correct, find the suitable colleges and then search according to SAT math score.
    if(flag_1==0):
        data_1=data[data['SATVR25']<=int(score_SAT_VR)];
        #Justify if the SAT math socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
        score_SAT_MT=input("Please enter your SAT math socre. The score range from 0 to 800. Finish the program by entering quit\n");
        flag_2=justify_SAT_score(score_SAT_MT);
        while(flag_2==1 and score_SAT_MT!='quit'):
            score_SAT_MT=input("The last input is not valid. Please enter your SAT math socre. The score range from 0 to 800. Finish the program by entering quit\n");
            flag_2=justify_SAT_score(score_SAT_MT);
        if(flag_2==0):
            #If the SAT math socre is correct, find the suitable colleges and then search according to SAT writing score
            data_2=data_1[data_1['SATMT25']<=int(score_SAT_MT)];
            #Justify if the SAT writing socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
            score_SAT_WR=input("Please enter your SAT writing socre. The score range from 0 to 800. Finish the program by entering quit\n");
            flag_3=justify_SAT_score(score_SAT_WR);
            while(flag_3==1 and score_SAT_WR!='quit'):
                score_SAT_WR=input("The last input is not valid. The score range from 0 to 800. Please enter your SAT writing socre. Finish the program by entering quit\n");
                flag_3=justify_SAT_score(score_SAT_WR);
            if(flag_3==0):
                #If the SAT writing socre is correct, find the suitable colleges and then output
                data_3=data_2[data_2['SATWR25']<=int(score_SAT_WR)];
                #If there is no suitable colleges, the program will return "There is no available world ranking top 1000 collges available for you, please try next year. Fighting!"
                if(len(data_3)==0):
                    data_3="There is no available world ranking top 1000 collges available for you, please try next year. Fighting!"
                else:
                #If the user have many choices, only return the top 10 suitable colleges
                    data_3=data_3.head(10)
    return data_3
            

#############################################
##Search the subdata according to ACT score##
#############################################
def justify_ACT_score(score):
    #flag=0 indicates input is valid, flag=1 indicates input is wrong
    flag=0;
    if(score.isdigit()==False):
        flag=1;
    else:
        if(int(score)>36):
            flag=1;
    return flag

#Find the top 10 available colleges by ACT score
def search_ACT(data):
    data_4="The user quit the program"
    #Justify if the ACT English socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
    score_ACT_EN=input("Please enter your ACT English socre. The score range from 0 to 36. Finish the program by entering quit\n");
    flag_1=justify_ACT_score(score_ACT_EN);
    while(flag_1==1 and score_ACT_EN!='quit'):
        score_ACT_EN=input("The last input is not valid. Please enter your ACT English socre. The score range from 0 to 36. Finish the program by entering quit\n");
        flag_1=justify_ACT_score(score_ACT_EN);
    #If the ACT Englsih socre is correct, find the suitable colleges and then search according to ACT math score.
    if(flag_1==0):
        data_1=data[data['ACTEN25']<=int(score_ACT_EN)];
        #Justify if the ACT math socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
        score_ACT_MT=input("Please enter your ACT math socre. The score range from 0 to 36. Finish the program by entering quit\n");
        flag_2=justify_ACT_score(score_ACT_MT);
        while(flag_2==1 and score_ACT_MT!='quit'):
            score_ACT_MT=input("The last input is not valid. Please enter your ACT math socre. The score range from 0 to 36. Finish the program by entering quit\n");
            flag_2=justify_ACT_score(score_ACT_MT);
        if(flag_2==0):
            #If the ACT math socre is correct, find the suitable colleges and then search according to ACT writing score
            data_2=data_1[data_1['ACTMT25']<=int(score_ACT_MT)];
            #Justify if the ACT writing socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
            score_ACT_WR=input("Please enter your ACT writing socre. The score range from 0 to 36. Finish the program by entering quit\n");
            flag_3=justify_ACT_score(score_ACT_WR);
            while(flag_3==1 and score_ACT_WR!='quit'):
                score_ACT_WR=input("The last input is not valid. Please enter your ACT writing socre. The score range from 0 to 36. Finish the program by entering quit\n");
                flag_3=justify_ACT_score(score_ACT_WR);
            if(flag_3==0):
                #If the ACT writing socre is correct, find the suitable colleges and then search according to ACT cumulative score
                data_3=data_2[data_2['ACTWR25']<=int(score_ACT_WR)];
                #Justify if the ACT cumulative socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
                score_ACT_CM=input("Please enter your ACT cumulative socre. The score range from 0 to 36. Finish the program by entering quit\n");
                flag_4=justify_ACT_score(score_ACT_CM);
                while(flag_4==1 and score_ACT_CM!='quit'):
                    score_ACT_CM=input("The last input is not valid. Please enter your ACT cumulative socre. The score range from 0 to 36. Finish the program by entering quit\n");
                    flag_4=justify_ACT_score(score_ACT_CM);
                #If the ACT cumulative socre is correct, find the suitable colleges and then output
                if(flag_4==0):
                    data_4=data_3[data_3['ACTCM25']<=int(score_ACT_CM)];
                    #If there is no suitable colleges, the program will return "There is no available world ranking top 1000 collges available for you, please try next year. Fighting!"
                    if(len(data_4)==0):
                        data_4="There is no available world ranking top 1000 collges available for you, please try next year. Fighting!"
                        #If the user have many choices, only return the top 10 suitable colleges
                    else:
                        data_4=data_4.head(10)
    return data_4


################################################################
##Search the top 10 suitable school according to users' choice##
################################################################
#Justify if the input is valid
def justify_type(choice):
    #flag=0 indicates input is valid, flag=1 indicates input is wrong
    flag=0;
    if(choice.isdigit()==False):
        flag=1
    elif(int(choice)!=0 and int(choice)!=1):
        flag=1
    return flag


#Let the user choose input SAT score or ACT score
def search(data):
    data_suit="The user quit the program"
    choice=input("Please enter the socre you use. 0 represents SAT and 1 represents ACT. Finish the program by entering quit\n")
    #Jusity if the input is valid. If the input is invalid, the program will let the user to reinput unitl correct or quit
    flag=justify_type(choice)
    while(flag==1 and choice!='quit'):
        choice=input("The last input is not valid. Please enter the socre you use. 0 represents SAT and 1 represents ACT. Finish the program by entering quit\n")
        flag=justify_type(choice)
    if(flag==0):
        #If the input is valid, use SAT search given choice is 0 and use ACT search given choice is 1
        if(int(choice)==0):
            data_suit=search_SAT(data)
        else: 
            data_suit=search_ACT(data)
    return data_suit


############################################################
##Return the top 10 colleges with UNITID, INSTNM and order##
############################################################
def data_show(data_top_10):
    #data_top_10 is the complete information of top 10 suitable colleges, while data_top_10_sub is part information
    #Return the order, UNITID and name of these 10 available colleges
    data_top_10['USER ORDER']=range(1,len(data_top_10)+1)
    data_top_10_sub=data_top_10[['USER ORDER','INSTNM','UNITID']]
    data_top_10_sub.index=range(1,len(data_top_10_sub)+1)
    print(data_top_10_sub)

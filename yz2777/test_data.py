from function import *



#Modified search_ACT(data) function (see function.py) for generate data for test
def search_ACT_test(data,input_EN1,input_EN2,input_MT1,input_MT2,input_WR1,input_WR2,input_CM1,input_CM2):
    data_4="The user quit the program"
    #Justify if the ACT English socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
    score_ACT_EN=input_EN1;
    flag_1=justify_ACT_score(score_ACT_EN);
    while(flag_1==1 and score_ACT_EN!='quit'):
        score_ACT_EN=input_EN2;
        flag_1=justify_ACT_score(score_ACT_EN);
    #If the ACT Englsih socre is correct, find the suitable colleges and then search according to ACT math score.
    if(flag_1==0):
        data_1=data[data['ACTEN25']<=int(score_ACT_EN)];
        #Justify if the ACT math socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
        score_ACT_MT=input_MT1;
        flag_2=justify_ACT_score(score_ACT_MT);
        while(flag_2==1 and score_ACT_MT!='quit'):
            score_ACT_MT=input_MT2;
            flag_2=justify_ACT_score(score_ACT_MT);
        if(flag_2==0):
            #If the ACT math socre is correct, find the suitable colleges and then search according to ACT writing score
            data_2=data_1[data_1['ACTMT25']<=int(score_ACT_MT)];
            #Justify if the ACT writing socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
            score_ACT_WR=input_WR1;
            flag_3=justify_ACT_score(score_ACT_WR);
            while(flag_3==1 and score_ACT_WR!='quit'):
                score_ACT_WR=input_WR2;
                flag_3=justify_ACT_score(score_ACT_WR);
            if(flag_3==0):
                #If the ACT writing socre is correct, find the suitable colleges and then search according to ACT cumulative score
                data_3=data_2[data_2['ACTWR25']<=int(score_ACT_WR)];
                #Justify if the ACT cumulative socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
                score_ACT_CM=input_CM1;
                flag_4=justify_ACT_score(score_ACT_CM);
                while(flag_4==1 and score_ACT_CM!='quit'):
                    score_ACT_CM=input_CM2;
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


#Modified search_SAT(data) function (see function.py) for generate data for test
def search_SAT_test(data,input_VR1,input_VR2,input_MT1,input_MT2,input_WR1,input_WR2):
    data_3="The user quit the program"
    #Justify if the SAT reading socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
    score_SAT_VR=input_VR1;
    flag_1=justify_SAT_score(score_SAT_VR);
    while(flag_1==1 and score_SAT_VR!='quit'):
        score_SAT_VR=input_VR2;
        flag_1=justify_SAT_score(score_SAT_VR);
    #If the SAT reading socre is correct, find the suitable colleges and then search according to SAT math score.
    if(flag_1==0):
        data_1=data[data['SATVR25']<=int(score_SAT_VR)];
        #Justify if the SAT math socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
        score_SAT_MT=input_MT1;
        flag_2=justify_SAT_score(score_SAT_MT);
        while(flag_2==1 and score_SAT_MT!='quit'):
            score_SAT_MT=input_MT2;
            flag_2=justify_SAT_score(score_SAT_MT);
        if(flag_2==0):
            #If the SAT math socre is correct, find the suitable colleges and then search according to SAT writing score
            data_2=data_1[data_1['SATMT25']<=int(score_SAT_MT)];
            #Justify if the SAT writing socre is correct. If the input is invalid, the program will let the user to reinput unitl correct or quit
            score_SAT_WR=input_WR1;
            flag_3=justify_SAT_score(score_SAT_WR);
            while(flag_3==1 and score_SAT_WR!='quit'):
                score_SAT_WR=input_WR2;
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

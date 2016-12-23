'''
Created on Dec 15, 2016

@author: sj238
'''
import pandas as pd
import warnings

def Clean_df(df):
    """
    clean the raw dataset, convert date type, drop useless features, drop invalid entries
    argument
    ========
    df: the raw dataframe
    return
    ======
    a cleaned dataframe
    """
    
    warnings.filterwarnings('ignore')
    #Too many missing values for these columns
    data = df.drop(['mo_sin_old_rev_tl_op', 'mo_sin_rcnt_rev_tl_op', 'mo_sin_rcnt_tl','mort_acc', 'mths_since_recent_bc', 
                    'mths_since_recent_bc_dlq', 'desc','mths_since_recent_inq', 'mths_since_recent_revol_delinq',
                    'num_accts_ever_120_pd', 'num_actv_bc_tl', 'num_actv_rev_tl', 'num_bc_sats', 'num_bc_tl', 'num_il_tl', 'num_op_rev_tl',
                    'num_rev_accts', 'num_rev_tl_bal_gt_0', 'num_sats','num_tl_120dpd_2m', 'num_tl_30dpd', 'num_tl_90g_dpd_24m',
                    'num_tl_op_past_12m', 'pct_tl_nvr_dlq', 'percent_bc_gt_75', 'tot_hi_cred_lim',
                    'total_bal_ex_mort', 'total_bc_limit', 'total_il_high_credit_limit',
                    'annual_inc_joint', 'dti_joint', 'verification_status_joint', 'tot_coll_amt', 'tot_cur_bal', 'open_acc_6m',
                    'open_il_6m', 'open_il_12m', 'open_il_24m', 'mths_since_rcnt_il','total_bal_il', 'il_util', 'open_rv_12m', 
                    'open_rv_24m','max_bal_bc', 'all_util', 'total_rev_hi_lim', 'inq_fi','total_cu_tl', 'inq_last_12m', 
                    'acc_open_past_24mths', 'avg_cur_bal', 'bc_open_to_buy', 'bc_util', 'mo_sin_old_il_acct',
                    'mths_since_last_delinq', 'mths_since_last_record', 'next_pymnt_d', 'mths_since_last_major_derog',],1)
        
    data.int_rate = pd.Series(data.int_rate).str.replace('%', '').astype(float)
    data.revol_util = pd.Series(data.revol_util).str.replace('%', '').astype(float)
    #These features are not of our interests
    data.drop(['id','pymnt_plan','url','title','policy_code','issue_d','loan_status','initial_list_status',
               'out_prncp','out_prncp_inv','total_pymnt','total_pymnt_inv','total_rec_prncp', 'sub_grade', 
               'last_pymnt_d','last_pymnt_amnt', 'last_credit_pull_d','total_rec_int','total_rec_late_fee',
               'recoveries','collection_recovery_fee', 'collection_recovery_fee', 'emp_title','zip_code',
               'collections_12_mths_ex_med', 'application_type','acc_now_delinq', 'chargeoff_within_12_mths', 
               'delinq_amnt','pub_rec_bankruptcies', 'tax_liens', 'member_id','funded_amnt',
               'funded_amnt_inv','earliest_cr_line'],1, inplace=True)
    data = data.dropna()
    return data
        
        
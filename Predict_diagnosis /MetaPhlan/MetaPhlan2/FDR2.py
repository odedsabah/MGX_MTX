import glob
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import fisher_exact
import mne

def create_excel(min_percent, bacteria_groups,file_name,project_num):
    df = pd.read_excel(file_name)

    df_control = df.loc[df["type" ]==1]
    df_control = df_control.drop(["name", "type", 'Unnamed: 0'], axis=1)
    df_CD = df.loc[df["type"] == 0]
    df_CD = df_CD.drop(["name", "type", 'Unnamed: 0'], axis=1)
    dict_list = []
    for d in [df_control, df_CD]:
        df_dict = {col:0 for col in d.columns if col[0] not in bacteria_groups}
        for i in range(len(d)):
            for col in df_dict:
                if d[i:i+1][col].values > min_percent:
                    df_dict[col] += 1
        dict_list.append(df_dict)



    len_list = [len(d) for d in [df_control, df_CD]]
    df = pd.DataFrame(columns=["spicies", "CD_amount", "CD_percent", "control_amount", "control_percent" ,"fisher test"])
    for key in dict_list[0].keys():
        if key in dict_list[1]:
            df = df.append(pd.Series([key, dict_list[0][key],dict_list[0][key]/len_list[0],
                                      dict_list[1][key],dict_list[1][key]/len_list[1],fisher_test(dict_list[0][key],
                                                                                                  len_list[0],dict_list[1][key],
                                                                                                  len_list[1])], index=df.columns),
                           ignore_index=True)
        else:
            df = df.append(pd.Series([key, dict_list[0][key],dict_list[0][key]/len_list[0],
                                      0, 0,fisher_test(dict_list[0][key],len_list[0],0,len_list[1])], index=df.columns),
                           ignore_index=True)
    set_0 = set(dict_list[0].keys())
    set_1 = set(dict_list[1].keys())
    set_only_1 = set_1 - set_0
    for key in set_only_1:
        df = df.append(pd.Series([key, 0, 0,dict_list[1][key],dict_list[1][key]/len_list[1],fisher_test(0,len_list[0],dict_list[1][key], len_list[1])], index=df.columns),
                       ignore_index=True)

    df = df.sort_values("spicies")
    df = df.reset_index(drop=True)
    df = create_FDR(df)
    try:
        df.to_excel("FDR" + project_num +".xlsx", index=False)
    except Exception as e:
        print("Error %s" % e)
    return df


def get_percent_and_group(bacteria_name, percent_list, bacteria_groups_to_remove, min_percent): #remove for lists valus that are not relevant
    bactiria_name_new = []
    percent_list_new = []
    for i in range(len(bacteria_name)):
        if percent_list[i] > min_percent and not contain_group(bacteria_name[i], bacteria_groups_to_remove):
            bactiria_name_new.append(bacteria_name[i])
            percent_list_new.append(percent_list[i])
    return bactiria_name_new, percent_list_new

def fisher_test(amount_CD, total_CD, amount_control, total_control):
    x = [amount_CD, total_CD, amount_control, total_control, total_CD - amount_CD, total_control - amount_control]
    oddsratio, pvalue = stats.fisher_exact([[amount_CD,amount_control ], [total_CD - amount_CD, total_control - amount_control]])
    return pvalue


def create_FDR(df):
    new_df = pd.DataFrame(columns=["spicies", "CD_amount", "CD_percent", "control_amount", "control_percent" ,"fisher test","FDR"])
    names = df["spicies"].values
    #print(df.loc[df["spicies"] == ''])
    laters_set = set()
    for i in names:
        laters_set.add(i[0])

    for later in laters_set:
        later_df = pd.DataFrame(columns= df.columns)
        for index, row in df.iterrows():
            if row["spicies"][0] == later:
                later_df = later_df.append({"spicies":row["spicies"],"CD_amount":row["CD_amount"],"CD_percent":row["CD_percent"],"control_amount":row["control_amount"],"control_percent":row["control_percent"],"fisher test":row["fisher test"]},ignore_index=True)
        later_df = later_df.sort_values(by=["fisher test"])

        p_adjust = mne.stats.fdr_correction(later_df["fisher test"].values, alpha=0.05, method='indep')
        later_df["FDR"] = p_adjust[1]
        new_df = pd.concat([new_df,later_df])

    return new_df

def create_df_for_rf (bacteria_name_new,amount_CD,amount_control):
    df = pd.DataFrame(columns=[bacteria_name_new, " control/CD"])
    pd.ExcelWriter('random_forest.xlsx', engine='xlsxwriter')
    df.to_excel("random_forest.xlsx", index=False)

def main():
    dir_names = ["df_project1","df_project2","df_project3","DF"]
    for project in dir_names:
        create_excel(0.05, ["t"],"./random forest/" + project + '.xlsx',project[-1])


if __name__ == "__main__":
    main()

import glob
import pandas as pd
import os

root_dir = "/Users/odedsabah/Desktop/python/bacreria"
raw_files_dir = root_dir + "/raw.d"
out_dir = root_dir + "/1.create_table"

healthy = 1
sick = 0

def get_data(file_name):
    '''
    This function reads the information from a metaphlan file and stores it in two lists (bacteria_name, percent_list)
    '''
    f = open(file_name, "r")
    f.readline()  # the first row is not important
    d = dict()
    for line in f:
        line_split = line.split()  # line is a string split sepereted in to array of word
        d[line_split[0].split("|")[-1]] = line_split[1]
    return d


def create_xl(dir_names, out_file):
    columns = ["name"]
    df = pd.DataFrame(columns=columns)
    for a in dir_names:
        files = (glob.glob(raw_files_dir + "/" + a + '/*.txt'))  # open all files in project dir
        for g in files:
            if g == raw_files_dir + "/" + a + "/sample2status.txt":  # open every file that is not the label file
                continue
            d = (get_data(g))
            d["name"] = g.split('\\')[-1][:-4]  # sample name
            for key in d:
                if key not in columns:
                    columns.append(key)
                    df[key] = 0  # it means this don't appear in df so we add it
            for c in columns:
                if c not in d.keys():
                    d[c] = 0  # it means this bacteria don't appear in d so we add it to him
            df = df.append(d, ignore_index=True)

    df["type"] = -1
    for a in dir_names:  # in this loop we add for every row it's label, healthy==1, sick==0
        f = open(raw_files_dir + "/" + a+ "/sample2status.txt", "r")
        for line in f:
            s = line.split()
            name = raw_files_dir + "/" + a + '/' + s[0]
            if s[1] == "Healthy":
                df.loc[df.name == name, "type"] = healthy
            else:
                df.loc[df.name == name, "type"] = sick
    df.to_excel(out_file)

def main():
    os.chdir(root_dir)
    dir_names = ['project_1', 'project_2', 'project_3']

    # Create separate file for each project
    for project in dir_names:
        print(project + "...")
        create_xl([project], out_dir + "/df_" + project + ".xlsx")

    # Create a unified file for all projects
    print("Unified...")
    create_xl(dir_names, out_dir + "/df_project.xlsx")

    print("Done")

main()



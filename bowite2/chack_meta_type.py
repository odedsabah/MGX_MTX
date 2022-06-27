
# upload packages
import pandas as pd

# import data
metadata = pd.read_csv("/Users/odedsabah/Desktop/hmp2_metadata.csv")
# select columns relevant

df = metadata.loc[:,["External ID", "Participant ID", "data_type","date_of_receipt"]]


gro = df.groupby(["External ID" ,"Participant ID","date_of_receipt"])["data_type"].apply(list)

def f(t_p):
      return "metagenomics" and "metatranscriptomics" in t_p
c = gro.apply(f)
c[c].to_csv("/Users/odedsabah/Desktop/hmp.csv")



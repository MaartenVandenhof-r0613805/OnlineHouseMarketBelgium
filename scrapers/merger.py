import pandas as pd


df1 = pd.read_excel('ImmoM_output.xlsx')
df2 = pd.read_excel('ImmoProxio_output.xlsx')
df3 = pd.read_excel('ImmoWeb_output.xlsx')
df4 = pd.read_excel('Zimmo_output.xlsx')

frames = [df1,df2,df3,df4]
result = pd.concat(frames)

result.to_excel("MergedOutput.xlsx")  

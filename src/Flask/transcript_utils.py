import pandas as pd
import re
import numpy as np

def get_tags(raw_string):
    try:
        res_list = []
        res_list = [(i.strip()) for i in re.findall('[0-9-A-Z/ :]*', raw_string) if (len(i.strip()) > 3 and (i.strip()[-1] == ':')) ]
        return res_list
    except:
        return np.nan
    
def get_processed_text(string, keywords):

    string = string.replace('Dr.', 'Dr')
    string = string.replace('dr.', 'Dr')
    
    if(len(keywords) == 0):
        col_names = ['Medical Transcript']
        res = [sent.strip(',').strip() for sent in string.split('. ') if(len(sent.strip()) > 0)]
        col_names.append(res)
        return col_names
        
    table = []
    col_names = []
    
    result = []
    # try:
    for i in range(len(keywords) - 1):
        # print(keywords[i + 1], string)
        start = string.index(keywords[i])
        end_i = (string.index(keywords[i]) + len(keywords[i]))
        end = string.index(keywords[i+1])
        temp = string[end_i:end]
        temp = re.sub(r"^[\s,]+", "", temp)
        temp = re.sub(r"(^\s+)|(\s*,?\s*$)", "", temp)
        # res = [re.sub(r'[ ]+', ' ', sent.strip()).strip(',').strip() for sent in temp.split('. ') if(len(sent.strip()) > 5)]
        col_names.append(keywords[i].strip()[:-1])
        table.append(temp)

    temp = string[(string.index(keywords[-1]) + len(keywords[-1])):]
    temp = re.sub(r"^[\s,]+", "", temp)
    temp = re.sub(r"(^\s+)|(\s*,?\s*$)", "", temp)
    res = [sent.strip(',').strip() for sent in temp.split('. ') if(len(sent.strip()) > 0)]
    col_names.append(keywords[-1].strip()[:-1])
    table.append(temp)

    return col_names, table

def get_table(string):
    keywords = get_tags(string)
    col, values = get_processed_text(string, keywords)
    
    return pd.DataFrame([col, values]).T.rename(columns = {0 : 'Subject of the report', 1 : 'Notes'})
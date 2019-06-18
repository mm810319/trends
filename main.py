import json
from take_out_gtdata import take_out
import csv
import pandas as pd

def main():
    next_file=0
    file = ["g_trends_scoreimdb2005.json", "g_trends_scoreimdb2006.json", "g_trends_scoreimdb2007.json",
            "g_trends_scoreimdb2008.json",
            "g_trends_scoreimdb2009.json", "g_trends_scoreimdb2010.json", "g_trends_scoreimdb2011.json",
            "g_trends_scoreimdb2012.json",
            "g_trends_scoreimdb2013.json", "g_trends_scoreimdb2014.json", "g_trends_scoreimdb20151.json",
            "g_trends_scoreimdb20152.json",
            "g_trends_scoreimdb20161.json", "g_trends_scoreimdb20162.json", "g_trends_scoreimdb20171.json",
            "g_trends_scoreimdb20172.json",
            "g_trends_scoreimdb20181.json", "g_trends_scoreimdb20182.json"]

    read_csvfile = ["scoreimdb2005.csv", "scoreimdb2006.csv", "scoreimdb2007.csv","scoreimdb2008.csv",
        "scoreimdb2009.csv", "scoreimdb2010.csv", "scoreimdb2011.csv","scoreimdb2012.csv",
        "scoreimdb2013.csv", "scoreimdb2014.csv", "scoreimdb20151.csv","scoreimdb20152.csv",
        "scoreimdb20161.csv", "scoreimdb20162.csv", "scoreimdb20171.csv","scoreimdb20172.csv",
        "scoreimdb20181.csv", "scoreimdb20182.csv"]

    for file_count in range (len(file)):

        if file_count<next_file:
            continue
        #print(file_count)
        output_file="add_trends_0617_"+read_csvfile[file_count]

        with open(file[file_count], 'r', encoding='utf-8') as opfile:
            data = json.load(opfile)
        opfile.close()

        datacsv = []
        with open(read_csvfile[file_count], "r", encoding="utf-8") as file2:
            read_data = csv.reader(file2)
            for line in read_data:
                datacsv.append(line)
        file2.close()
        new_col=["Cmovie_8week_ago","Cmovie_7week_ago","Cmovie_6week_ago","Cmovie_5week_ago","Cmovie_4week_ago",
                 "Cmovie_3week_ago","Cmovie_2week_ago","Cmovie_1week_ago","Cmovie_0week_ago","Cmovie_1week_later",
                 "Cmovie_2week_later","Cmovie_3week_later","Cmovie_4week_later","Cmovie_5week_later",
                 "Cmovie_6week_later","Cmovie_7week_later","Cmovie_8week_later"]
        datacsv[0].extend(new_col)


        for i in range(0,len(data)):
            outputlist = []
            for week in range (8,-9,-1):
                try:
                    temp=take_out(data[i],"front",week,0)
                    outputlist.append(temp)
                except:
                    outputlist.append("error")


            datacsv[i+1].extend(outputlist)
            print("第{}筆處理中".format(i+1))
        print("資料寫入中...")
        print(datacsv)
        with open(output_file,'w',newline="",encoding="utf-8") as outf:
            output=csv.writer(outf)
            output.writerows(datacsv)
        outf.close()


main()

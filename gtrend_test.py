from pytrends.request import TrendReq #API
import time
import random
import json
import csv


next_file=1
next_title=4862


file_count=1
for o_filename in["final_618.csv"]:
                # "scoreimdb2005.csv","scoreimdb2006.csv","scoreimdb2007.csv","scoreimdb2008.csv","scoreimdb2009.csv",
                #  "scoreimdb2010.csv", "scoreimdb2011.csv", "scoreimdb2012.csv", "scoreimdb2013.csv", "scoreimdb2014.csv",
                # "scoreimdb20151.csv", "scoreimdb20152.csv", "scoreimdb20161.csv", "scoreimdb20162.csv", "scoreimdb20171.csv",
                #   "scoreimdb20172.csv", "scoreimdb20181.csv","scoreimdb20182.csv"]:

    if file_count<next_file:
        file_count+=1
        continue
    with open(o_filename,'r',newline='',encoding="utf-8") as csvfile:
        movies= csv.reader(csvfile)


        f_output=[]


        outfile_name='g_trends_'+o_filename.split(".")[0]+".json" #輸出檔案名稱

        i=0
        for m in movies:
            if i==0:
                i+=1
                continue
            if  file_count == next_file:
                if i <next_title:
                #       break
                   i += 1
                   continue
            try:
                movie = m[38]
                #movie=m[1]   #m['Title']
                release_date=m[17]    #m['released'_date_USA]
                imdbID=m[0]      #m['imdbID']
            except:                             #如果出錯 回傳是第幾筆錯誤
                output = dict([("error", i)])
                with open(outfile_name, 'a') as outfile:
                    outfile.write(","+json.dumps(output) + "\n")
                outfile.close()
                i += 1
                continue
            s_movie=movie

            if "," in movie:          #Gooletrends不可使用"，" 分隔 所以將名稱有"，"的取代成空白
                s_movie = movie.replace(",", " ")
            if "：" in movie:
                s_movie = movie.split("：")[0]
            if movie!="":

                release_year=int("20"+release_date[-2:])   #取上映年分，還有前一年和後一年
                print(i, movie,s_movie,release_date,release_year)
                try:
                    front_year=int(release_year)-1
                    next_year=int(release_year)+1
                    timeframe = str(front_year) + "-01-01 " + str(next_year) + "-12-31"
                except:
                    output = dict([("error", str(i)+"relased_date_NA")])
                    with open(outfile_name, 'a') as outfile:
                        outfile.write("," + json.dumps(output) + "\n")
                    outfile.close()
                    i += 1
                    continue

                pytrend = TrendReq()
                kw_list=[s_movie]


                #print(i,s_movie)


                #print(timeframe)
                # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()

                pytrend.build_payload(kw_list=kw_list,cat=34,timeframe=timeframe,geo="TW")  #搜尋使用的參數,其中cat=34 為電影類別
                # Interest Over Time
                moviedata = pytrend.interest_over_time().get(kw_list)

                try:
                    moviedata.rename(columns={moviedata.columns[0]: "Count" }, inplace=True)
                except:
                    output = dict([("error", i),("imdbID",imdbID),("Title",movie),("released",release_date)])
                    with open(outfile_name, 'a') as outfile:
                        outfile.write("," + json.dumps(output,ensure_ascii= False) + "\n")
                    outfile.close()
                    i += 1
                    continue
                #print(moviedata)
                preload = json.loads(moviedata.to_json(orient='table'))['data']
               # print(preload)

                for p in preload:
                    year=p["date"][0:10]
                    p["date"]=year
                #print(preload)



                output = dict([("imdbID",imdbID),("Title",movie),("released",release_date),("data", preload)])
                time.sleep(random.randint(3, 5))
            else:
                output = dict([("error", str(i)+"chinese_nameNA")])


            with open(outfile_name, 'a') as outfile:
                if i==1:
                    outfile.write("["+json.dumps(output,ensure_ascii= False)+"\n")
                else:
                    outfile.write(","+json.dumps(output,ensure_ascii= False) + "\n")
                outfile.close()

            i += 1

        with open(outfile_name, 'a') as outfile:
            outfile.write("]")
        outfile.close()

        csvfile.close()
        file_count+=1
# coding: utf-8
import requests, re, os, time, pickle
import pandas as pd

keywords = '''artificial intelligence'''
APIkey = ''

current_time = time.asctime()
current_time = current_time.replace("  ","_")
current_time = current_time.replace(" ","_")
current_time = current_time.replace(":","_")

os.popen("mkdir "+current_time)

def extract_metadata(keywords,APIkey):
    textdata =pd.DataFrame()
    start = 1
    count =100
    idx = 1
    while True:
        url = 'http://api.elsevier.com/content/search/index:SCIDIR?query='+keywords+'&count='+str(count)+"&start="+str(start)
        temp_df,num_results = extract_article_info(url,start,APIkey)
        if num_results == -1:
            break
        textdata=textdata.append(temp_df,ignore_index=True)
        if num_results<count:
            print("last page")
            break
        else:
            start = start+ 100
        break

    return textdata



def extract_article_info(url,start,APIkey):
    intextdata =pd.DataFrame()
    resp = requests.get(url,headers={'Accept':'application/json','X-ELS-APIKey':APIkey})
    results = resp.json()
    num_results = 0
    identifier_set = []

    try:
        num_results = len(results['search-results']['entry'])
        for idx in range(0,num_results):
            try:
                identifier_set.append(results['search-results']['entry'][idx]['dc:identifier'])
            except:
                pass
        print(round(100*len(identifier_set)/num_results,2),'% of results from',start,"~",start+num_results-1,'can be accessed')
    except:
        print("No entry is found, you may need to change the keywords")
        return -1,-1
    idx=0
    for identifier in identifier_set[:5]:
        try:
            try:
                resp_info = requests.get("http://api.elsevier.com/content/article/"+identifier+"?&view=FULL",
                                headers={'Accept':'application/json',
                                         'X-ELS-APIKey': APIkey})
                results_info = resp_info.json()
                _ = results_info["full-text-retrieval-response"]["coredata"]["dc:title"]
            except:
                resp_info = requests.get("http://api.elsevier.com/content/article/"+identifier,
                    headers={'Accept':'application/json',
                         'X-ELS-APIKey': APIkey})
                results_info = resp_info.json()
                _ = results_info["full-text-retrieval-response"]["coredata"]["dc:title"]



            if (idx+start)%1==0:
                print(idx+start,"papers are extracted")

            ### number of citation ###
            try:
                resp_c = requests.get("http://api.elsevier.com/content/search/index:SCOPUS?query=DOI("+identifier[4:]+")&field=citedby-count",
                        headers={'X-ELS-APIKey': APIkey})
                results_c = resp_c.json()
                cv = results_c['search-results']['entry']
                cc = cv[0]['citedby-count']
            except:
                cc = 0

            ### title ###
            try:
                title=results_info["full-text-retrieval-response"]["coredata"]["dc:title"]
            except:
                title="not provided"

            ### date of publication ###
            try:
                date=results_info["full-text-retrieval-response"]["coredata"]["prism:coverDate"]
            except:
                date="not provided"

            ### authors ###
            try:
                authors=[]
                for x in range(0,len(results_info["full-text-retrieval-response"]["coredata"]['dc:creator'])):
                    authors.append(results_info["full-text-retrieval-response"]["coredata"]['dc:creator'][x]['$'])
            except:
                authors="not provided"

            ### Author provided keywords ###
            try:
                apk=[]
                for x in range(0,len(results_info["full-text-retrieval-response"]["coredata"]['dcterms:subject'])):
                    apk.append(results_info["full-text-retrieval-response"]["coredata"]['dcterms:subject'][x]['$'])
            except:
                apk="not provided"

            ### journal/book name ###
            try:
                journal=results_info["full-text-retrieval-response"]["coredata"]['prism:publicationName']
            except:
                journal="not provided"

            ### type of publication ###
            try:
                jtype=results_info["full-text-retrieval-response"]["coredata"]['prism:aggregationType']
            except:
                jtype="not provided"

            ### abstract ###
            try:
                abst=results_info["full-text-retrieval-response"]["coredata"]['dc:description']
            except:
                abst="not provided"

            # links for the paper
            try:
                links = results_info['full-text-retrieval-response']['coredata']['prism:url']
            except:
                links = "not provided"

            ### full body ###
            try:
                full_body = results_info['full-text-retrieval-response']['originalText'].split(results_info['full-text-retrieval-response']['coredata']['dc:description'])[-1]
            except:
                full_body = "not provided"
            f = open(current_time+'/'+str(idx+start)+'.txt','w')
            f.write(full_body)
            f.close()


            intextdata=intextdata.append({'DOI':identifier,'title':title,'date':date,'authors':authors,
                    'keywords':apk,'journal_or_book_name':journal,
                    'journal_type':jtype,'abstract':abst,"citation_count":int(cc),"paper_id":int(idx+start),"link":links},ignore_index=True)
            idx+=1
        except:
            print(idx,": full review failed")

    return intextdata,num_results



textdata = extract_metadata(keywords,APIkey)

pickle.dump(textdata,open( current_time+'/extracted_data.p', "wb" ))

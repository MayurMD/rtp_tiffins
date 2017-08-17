from bs4 import BeautifulSoup
import urllib
import re
import psycopg2
from Tiffin import *




def get_page_list(link):

    while (link is not None):
        print link
        link,tiffin_list=get_tiffins_per_page(link)
        store_tiffin_list(tiffin_list)
        #response=urllib.urlopen(link)
        #soup=BeautifulSoup(response,'html.parser')
        #next=soup.find("li",{"class":"pagination-next"})
        #if next.a is not None:
         #   link="http://apnatriangle.com"+next.a.get('href')
        #else:
         #   link=None




def get_tiffins_per_page(url):
    tiffin_list=[]
    #print url
    response=urllib.urlopen(url)
    soup=BeautifulSoup(response,'html.parser')
    #print soup.prettify()
    #print soup.tr['id']
    row_list=soup.find_all("tr",{"class":"adsmanager_table_description trcategory_14"})
    for x in row_list:
        link="http://apnatriangle.com"+x.a.get('href')
        m = re.search('id=(\d+)',link)
        id=m.group(1)
        tiffin_obj=parse_tiffin(link)
        tiffin_tuple = (id, tiffin_obj)
        tiffin_list.append(tiffin_tuple)
     #Get link for next tiffin page

    next = soup.find("li", {"class": "pagination-next"})
    if next.a is not None:
        link = "http://apnatriangle.com" + next.a.get('href')
    else:
        link = None


    return link,tiffin_list


'''
def get_tiffin_detail(tiffin_dict):
    tiffin_list=[]
    for i in tiffin_dict.keys():
        #print "url",tiffin_dict[i]
        tiffin_obj=parse_tiffin(tiffin_dict[i])
        tiffin_tuple=(i,tiffin_obj)
        tiffin_list.append(tiffin_tuple)
    return tiffin_list
'''



def store_tiffin_list(tiffin_list):
    element_list=[]
    conn=None

    for i in tiffin_list:
        element=(i[0],i[1].title,i[1].description,i[1].fname,i[1].email,
                 i[1].phone,i[1].city,i[1].zipcode,i[1].specialities,i[1].cuisine)
        #print element
        element_list.append(element)


    try:
        conn = psycopg2.connect("dbname='wake' user='gpadmin' host='' ")
    except Exception as e:
        print "inside error"+str(e)

    cur = conn.cursor()

    args_str = ','.join(cur.mogrify('(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', x) for x in element_list)
    try:

        cur.execute("INSERT INTO rtp_tiffins VALUES " + args_str)
    except Exception as e:
        print e
    conn.commit()




def main():
    apnaurl = 'http://apnatriangle.com/index.php?option=com_adsmanager&view=list&catid=14&Itemid=345'
    get_page_list(apnaurl)

main()

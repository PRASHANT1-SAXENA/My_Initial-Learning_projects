import requests
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import csv

page_start = 1
group_range = 0
page_stop = 3
mgb = {"unique_id": [], "City": [], "Property_Name": [], "Rent_price": [], "Property_Address": [], "CarpetArea": [],
       "CarpetAreaUnit": [], "CoveredArea": [], "CoveredAreaUnit": [], "latitude": [], "longitude": [], "Post_date": [],
       "url": []}
for pg in range(page_start, page_stop):
    url = f"https://www.magicbricks.com/mbsrp/propertySearch.html?editSearch=Y&category=R&propertyType=10002,10003,10021,10022,10020,10001,10017,10007,10018,10008,10009,10006,10012,10026,10011,10013,10014&bedrooms=11700,11701,11702,11703&city=3327&page={page_start}&groupstart={group_range}&offset=0&maxOffset=656&sortBy=premiumRecent&postedSince=-1&pType=10002,10003,10021,10022,10020,10001,10017,10007,10018,10008,10009,10006,10012,10026,10011,10013,10014&isNRI=N&multiLang=en"
    print(url)
    r = requests.get(url)
    data = r.json()
    for result in data["resultList"]:
        try:
            mgb["unique_id"].append(result["id"])
        except:
            mgb["unique_id"].append(np.nan)

        try:
            corr = result["ltcoordGeo"].split(",")
            mgb["latitude"].append(corr[0])
            mgb["longitude"].append(corr[1])
        except:
            mgb["latitude"].append(np.nan)
            mgb["longitude"].append(np.nan)

        try:
            mgb["Rent_price"].append(result["price"])
        except:
            mgb["Rent_price"].append(np.nan)

        try:
            mgb["CarpetArea"].append(result["carpetArea"])
            mgb["CarpetAreaUnit"].append("Sq-ft")
        except:
            mgb["CarpetArea"].append(np.nan)
            mgb["CarpetAreaUnit"].append(np.nan)

        try:
            mgb["CoveredArea"].append(result["coveredArea"])
            mgb["CoveredAreaUnit"].append("Sq-ft")
        except:
            mgb["CarpetArea"].append(np.nan)

        try:
            mgb["City"].append(result["ctName"])
        except:
            mgb["City"].append(np.nan)

        try:
            mgb["Property_Name"].append(result["propertyTitle"])
        except:
            mgb["Property_Name"].append(np.nan)

        try:
            fetch_url = result["url"]
            url_link = f"https://www.magicbricks.com/propertyDetails/{fetch_url}"
            mgb["url"].append(url_link)
        except:
            mgb["url"].append(np.nan)

        try:
            r = requests.get(url_link).text
            soup = BeautifulSoup(r, "lxml")
            for i in range(0, 5):
                title = soup.find_all("div", class_="mb-ldp__more-dtl__list--label")[i].text
                if title == "Address":
                    address = soup.find_all("div", class_="mb-ldp__more-dtl__list--value")[i].text
                    mgb["Property_Address"].append(address)
                    break
                else:
                    continue
        except:
            mgb["Property_Address"].append(np.nan)

        try:
            mgb["Post_date"].append(result["postDateT"][0:10])
        except:
            mgb["Post_date"].append(np.nan)

    page_start = page_start + 1
    group_range = group_range + 30

pd.set_option("display.max_rows",500)
pd.set_option("display.max_columns",500)
mgb_f=pd.DataFrame(mgb)
#print(mgb_f.shape)
print(mgb_f)

# -*- coding: utf-8 -*-
"""phones_reviews_scraping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-49D_gj72fkJoS_HXE_jCFxFgMdeoM2u
"""

import requests as req
import bs4

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/51.0.2704.103 Safari/537.36'}

def search_amazon_product(query):
  s_url =  "https://www.amazon.in/s?k="+query
  page = req.get(s_url, headers = header)
  print(s_url, page.status_code)
  if page.status_code == 200:
    results = []
    soup = bs4.BeautifulSoup(page.content)
    for i in soup.findAll("div", {'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"}):
      results.append(i['data-asin'])
    return results
  else:
      return "Error"

amazon_product_asi = []
for i in range(1,3):
  if i==1:
    list1 = search_amazon_product('mobile')
  else :
    list1 = search_amazon_product('mobile'+ '&page=' + str(i))
  if list1 != "Error" :
    for i in list1:
      amazon_product_asi.append(i)

amazon_product_asi

def search_by_product_asni_numbers(asin):
  url = "https://www.amazon.in/dp/"+ str(asin)
  page =  req.get(url, headers=header)
  print(url, page.status_code)
  if page.status_code == 200:
    soup = bs4.BeautifulSoup(page.content)
    link = soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"})
    return link[0]['href']
  else :
    return "Error"

search_by_product_asni_numbers('B089MV96RW')

def get_reviews(review_link, page_number):
  url="https://www.amazon.in" + review_link + '&pageNumber='+ str(page_number)
  print(url)
  page=req.get(url, headers=header)
  if page.status_code==200:
    reviews = []
    soup = bs4.BeautifulSoup(page.content)
    for i in soup.findAll("span",{'data-hook':"review-body"}):
      reviews.append(i.text)
    return reviews
  else:
    return "Error"

get_reviews('/Samsung-Galaxy-Storage-Additional-Exchange/product-reviews/B089MV96RW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews', 1)

return_reviews = []
for i in amazon_product_asi:
  reviews = []
  link = search_by_product_asni_numbers(i)
  for j in range(10):
    asmi_review = get_reviews(link, j)
    for x in asmi_review:
      reviews.append([i, x])
  return_reviews.append(reviews)

import pandas as pd

review_data = pd.DataFrame.from_dict(return_reviews)
review_data.to_excel('reviews.xlsx', index=False)

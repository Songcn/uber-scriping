# # Copyright 2015 IBM Corp. All Rights Reserved.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# # https://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# 
# import os
# from flask import Flask, jsonify
# 
# app = Flask(__name__)
# 
# @app.route('/')
# def Welcome():
#     return app.send_static_file('index.html')
# 
# @app.route('/myapp')
# def WelcomeToMyapp():
#     return 'Welcome again to my app running on Bluemix!'
# 
# @app.route('/api/people')
# def GetPeople():
#     list = [
#         {'name': 'John', 'age': 28},
#         {'name': 'Bill', 'val': 26}
#     ]
#     return jsonify(results=list)
# 
# @app.route('/api/people/<name>')
# def SayHello(name):
#     message = {
#         'message': 'Hello ' + name
#     }
#     return jsonify(results=message)
# 
# port = os.getenv('PORT', '5000')
# if __name__ == "__main__":
# 	app.run(host='0.0.0.0', port=int(port))

'''
Created on Nov 29, 2016

@author: Songcn
'''
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import datetime
import random
import re
# import pymysql

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities
# 
# Map<String, Object> contentSettings = new HashMap<String, Object>();
# contentSettings.put("images", 2);
# 
# Map<String, Object> preferences = new HashMap<String, Object>();
# preferences.put("profile.default_content_settings", contentSettings);

caps = DesiredCapabilities.PHANTOMJS
caps['browserName'] = 'safari'
caps['loadIages'] = False
caps['javascriptEnabled'] = False
print(caps)
# WebDriver driver = new ChromeDriver(caps);

driver = webdriver.PhantomJS(executable_path='/Users/Songcn/IBMWork/Python/tools/phantomjs', desired_capabilities=caps)
def getSource(url, xpath):
    print("will get url: " + url)
    driver.get(url) #"https://zh.airbnb.com/s/Beijing--China"
    
    try:
        print('will get element')
        element = WebDriverWait(driver, 10).until(
                           EC.presence_of_element_located((By.XPATH, xpath))) 
        print("did get element: " + xpath)
    finally:
        pass
#         driver.close()
    return driver.page_source

random.seed(datetime.datetime.now())

# conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='passw0rd', db='mysql', charset='utf8')
# cur = conn.cursor()
# cur.execute("USE scraping")

# def store(title, content):
#     cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\",\"%s\")", (title, content))
#     cur.connection.commit()

pages = set()
queue = []
def getLinks(articleUtl):
    global pages
    try:
#         html = urlopen("https://zh.airbnb.com" + articleUtl)
#         print('will getSource')
        html = getSource("https://zh.airbnb.com" + articleUtl, "//span[@class='listing-name--display']")
    except URLError as e:
        print(e)
        return None
    except HTTPError as e:
        print(e)
        return None
    try:
        try:
            bsObj = BeautifulSoup(html,"html.parser")
        except AttributeError as e:
            print("This page is missing something! No worries though!")
        
        links = bsObj.findAll("a", href=re.compile("^(/rooms/)([0-9])*$"))
            
    except AttributeError as e:
        print(e)
        return None
    return links

links = getLinks("/s/北京--中国?guests=1&ss_id=bgy8tcqq&source=bb&page=1&s_tag=SMB5r6LF&allow_override%5B%5D=")

try:
    while links != None and len(links) > 0:
        for link in links:
            newLink = link.attrs["href"]
            if newLink not in pages and newLink not in queue:
                queue.append(newLink)
        if len(queue) > 0:
            nextArticle = queue.pop(0)
            pages.add(nextArticle)
            links = getLinks(nextArticle)
            print("Next Article: " + nextArticle)
            print("Crawled: " + str(len(pages)) + "  Queue: " + str(len(queue)))
finally:
    pass
#     cur.close()
#     conn.close()
print("finished.")
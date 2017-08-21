
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import csv

def save_comments(driver, pre_path, pre_pages):
    
    # Fetch the comments and write them to local files one by one.
    
    # click the "unfold" to fetch all content if the comment is too long
    
    print("Unfolding all comments!")
    unfold_btns = driver.find_elements_by_xpath("//div/p/a[@action-type='fl_unfold']")
    for unfold_btn in unfold_btns:
        unfold_btn.click()
        sleep(3)   # if click too fast, some may not work
    if len(unfold_btns) != 0 and len(unfold_btns) != len(driver.find_elements_by_xpath("//a[@action-type='fl_fold']")):  # test if all the comments were unfold!
	    print(len(unfold_btns))
	    print(len(driver.find_elements_by_xpath("//a[@action-type='fl_fold']")))
	    quit("Some comments were unfolded!")
        
        
    # End

    print("Writing comments to local files!")
    comments = driver.find_elements_by_xpath("//div[@class='feed_content wbcon']/p[@class='comment_txt'][last()]")
    for i in range(len(comments)):
        path = pre_path + "/" + str(pre_pages + i + 1) + ".txt"
        file = open(path, "w+", encoding = "utf-8")
        file.write(comments[i].text)
        file.close()
    return(pre_pages + len(comments))

def fetch_userinfo(driver, pre_path):
    
    # Fetch user info
    
    print("Fetching userinfo!")

    # Fetch user nick name

    names = []
    name_nodes = driver.find_elements_by_xpath("//div[@class='feed_content wbcon']/a[@class='W_texta W_fb']")
    for name_node in name_nodes:
        names.append(name_node.text)

    # Fetch weibo approved type

    approves = []
    approve_nodes_parents = driver.find_elements_by_xpath("//div[@class='feed_content wbcon']")
    for approve_node_parent in approve_nodes_parents:
        try:
            approve_node = approve_node_parent.find_element_by_xpath("./a[2]")
            approve = approve_node.get_attribute("title").replace(" ", "")   
        except NoSuchElementException:
            approve = ""
        approves.append(approve)

    # Fetch published date

    dates = []
    date_nodes = driver.find_elements_by_xpath("//div[@class='content clearfix']/div[@class='feed_from W_textb'][1]/a[@class='W_textb']")
    for date_node in date_nodes:
        date = date_node.get_attribute("title")[0:10]
        dates.append(date)

    # Fetch platform

    platforms = []
    platform_node_parents = driver.find_elements_by_xpath("//div[@class='content clearfix']")
    for platform_node_parent in platform_node_parents:
        try:
            platform_node = platform_node_parent.find_element_by_xpath("./div[@class='feed_from W_textb'][1]/a[2]")
            platform = platform_node.text
        except NoSuchElementException:
            platform = ""
        platforms.append(platform)
    
    # End
    
    print("Writing userinfo to local file!")
    info = [names, approves, dates, platforms]
    path = pre_path + "/records.csv"
    with open(path, "a+", newline = "", encoding = "utf-8") as csvfile:
        info_writer = csv.writer(csvfile)
        info_writer.writerows(info)
    csvfile.closed


# Open a web page

# Login to weibo in firefox, search with some key words and copy the url.

url = "Url you copied"
fp = webdriver.FirefoxProfile("C:/Users/01/AppData/Roaming/Mozilla/Firefox/Profiles/od1vlf1z.default")  # This is the firefox profile in my computer, type in yours.
browser = webdriver.Firefox(fp)
browser.get(url)
print("Wetsite opened!")

# End

pages = # Number of pages you get from the search result.
pre_path = "Path of the fold you want to save files"
fetched_pages = 0
for page in range(pages):

    # wait a few seconds
    
    sleep(8)
    
    # wait until the "next page" button present except the last page
    
    if page + 1 < pages:
        try:
            next_page = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@class='page next S_txt1 S_line1']")))
            print("Page " + str(page + 1) + " opened successfully!")
        except TimeoutException:
            print("Page loading time out!")
            break
    else:
        try:
            page_list = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='list']/a[@class='page S_txt1']")))
            print("Page " + str(page + 1) + " opened successfully!")
        except TimeoutException:
            print("Page loading time out!")
            break
    
    fetched_pages = save_comments(browser, pre_path, fetched_pages)
    fetch_userinfo(browser, pre_path)
        
    # click the "next page" button except the last page
        
    if page + 1 < pages:
        next_page.click()
        print("Directing to next page!")

print("Fetching finish!")

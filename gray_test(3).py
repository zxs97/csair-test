#!/usr/local/bin/python3
#conding = utf-8

"""
 南方航空无人机巡检自动化灰度测试
    author:南方航空,csair.com
"""


import json
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# username = ''
# password = ''
HOME_URL = "http://27.184.11.183:8081/outer/v1/accessManage/"

#日志输出文件地址
#LOG_OUTPUT_FILENAME = "/Users/KAILEE/Desktop/csair/py/"
LOG_OUTPUT_FILENAME = "C:\\Users\\poc\\Desktop\\gray_log\\"

global file
file = open(LOG_OUTPUT_FILENAME + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log", "a+")
global isTest
isTest = True

#初始化
def init() :
    driver = webdriver.Chrome()
    #driver.maximize_window()
    return driver

# 第一步 首页
def step_first(driver, startUrl, num) :
    writeLog("测试第 %d 次-执行第一步 start" %num)
    #打开首页
    driver.get(startUrl)
    time.sleep(2)
    driver.add_cookie({'name':'testFrom','value':'likai'})
    driver.refresh()
    #等待加载
    time.sleep(10)
    #获取无人机信息
    UAV = driver.find_element_by_class_name("uav-name").text
    isGray = False
    if UAVS != "UAV-TEST" :
        return isGray
    isGray = True

    content = driver.find_element_by_class_name("zsl-favourable-child-content")
    item = content.find_element_by_class_name("zls-child-uav")
    driver.execute_script("arguments[0].scrollIntoView();", item)#鼠标滑到到此元素
    item.click()
    writeLog("测试第 %d 次-执行第一步 end" %num)
    return isGray

# 第二步 
def step_second(driver, num) :
    writeLog("测试第 %d 次-执行第二步 start" %num)
    time.sleep(5)
    #判断是否有无人机数据
    if isElementPresent(driver, "zls-uav-cell") == False :
        driver.find_element_by_id("single-name").send_keys("UAV-001")
        driver.find_element_by_id("search-submit").click()
        time.sleep(10)
    if isElementPresent(driver, "zls-uav-cell") == False :
        return False
    cell = driver.find_element_by_class_name("zls-uav-cell")
    item = cell.find_element_by_xpath(".//div[@class='fligthR']/ul/li[3]")
    item.click()
    time.sleep(2)
    starting = cell.find_element_by_xpath(".//div[@class='zls-cabin']/ul/li[1]/div/div[@class='cabin-price']/div[1]/div[1]")
    starting.click()
    #点击跳过登录
    time.sleep(5)
    driver.find_element_by_id("noLogin_btn").click()
    writeLog("测试第 %d 次-执行第二步 end" %num)
    return True

# 第三步
def step_third(driver, num) :
    writeLog("测试第 %d 次-执行第三步 start" %num)
    time.sleep(8)
    #提取cookie信息
    cookies = driver.get_cookies()
    grayAbCookies = {"uuid":getCookie(cookies, "gabUuid"), "sid":getCookie(cookies, "gabSid"), "grayCode":getCookie(cookies, "grayValue"), "userId":getCookie(cookies, "userId"), "area":getCookie(cookies, "area")}
    print("grayAbCookies:%s" %grayAbCookies)
    #点击下一步
    driver.find_element_by_id("goNext").click()
    time.sleep(5)
    currentUrl = driver.current_url
    if "/B2C40/newTrips/static/main/page/passengers" in currentUrl :
        return False
    writeLog(currentUrl)
    #写入灰度ABcookies
    driver.add_cookie({"domain":"27.184.11.183:8081", "name":"gabUuid", "value":"" if grayAbCookies["uuid"] == None else grayAbCookies["uuid"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"27.184.11.183:8081", "name":"gabSid", "value":"" if grayAbCookies["sid"] == None else grayAbCookies["sid"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"27.184.11.183:8081", "name":"grayValue", "value":"" if grayAbCookies["grayCode"] == None else grayAbCookies["grayCode"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"27.184.11.183:8081", "name":"userId", "value":"" if grayAbCookies["userId"] == None else grayAbCookies["userId"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"27.184.11.183:8081", "name":"area", "value":"" if grayAbCookies["area"] == None else grayAbCookies["area"], "path":"/", "expires":None})
    driver.refresh()
    writeLog("测试第 %d 次-执行第三步 end" %num)
    return True

# 第五步
def step_fifth(driver, num) :
    writeLog("测试第 %d 次-执行第五步 start" %num)
    writeLog("测试第 %d 次-执行第五步 end" %num)
    return True

def start(driver, startUrl, endUrl, num) :
    writeLog("测试第 %d 次-测试开始" %num)
    result = "SUCCESS"
    isGray = False
    step = 0
    stepResult = True

    try:
        step = 1
        isGray = step_first(driver, startUrl, num)
    except BaseException as error :
        result = "ERROR"
        print(error)

    if result == "SUCCESS" and isGray and stepResult : 
        try:
            step = 2
            stepResult = step_second(driver, num)
        except BaseException as error :
            result = "ERROR"
            print(error)

    if result == "SUCCESS" and isGray and stepResult : 
        try:
            step = 3
            stepResult = step_third(driver, num)
        except BaseException as error :
            result = "ERROR"
            print(error)
    
    afterProcess(driver, result, num, step, endUrl, isGray)

def afterProcess(driver, result, num, step, endUrl, isGray) :
    writeLog("测试第 %d 次-测试结果：%s" %(num, result))
    writeLog("测试第 %d 次-是否灰度：%s" %(num, isGray))
    if result == "ERROR" :
        writeLog("测试第 %d 次-异常页：%d" %(num, step))
    driver.get(endUrl)
    time.sleep(5)
    writeLog("测试第 %d 次-灰度cookie信息：uuid[%s], sid[%s], grayCode[%s], userId[%s], area[%s]" %(num, driver.get_cookie("gabUuid"), driver.get_cookie("gabSid"), driver.get_cookie("grayValue"),driver.get_cookie("userId"),driver.get_cookie("area")))
    writeLog("测试第 %d 次-清除cookie" %num)
    driver.delete_all_cookies()
    writeLog("测试第 %d 次-等待下一次测试..." %num)
def getCookie(cookies, name) :
    if len(cookies) == 0 :
        return ""
    value = ""
    for cookie in cookies :
        if cookie["name"] == name :
            value = cookie["value"]
            break
    return value
def isElementPresent(driver, className) :
    try:
        driver.find_element_by_class_name(className)
        return True
    except BaseException :
        return False
def writeLog(text) :
    timeStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timeStr + " " + text)
    file.write(timeStr + " " + text + "\n")
    file.flush()

def main() :
    #初始化
    driver = init()
    startUrl = HOME_URL
    endUrl = startUrl

    testCount = 5000
    for num in range(1, testCount + 1) :
        start(driver, startUrl, endUrl, num)
    driver.quit
    file.flush()
    file.close()
main()

#conding = utf-8

"""
 南方航空首页自动化测试
    author:南方航空,csair.com
"""

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from random import randint

PAY_SUCCESS = "https://ec.test.csair.com/B2C40/newTrips/static/main/page/success/index.html?orderNo="
PAY_SUCCESS_ONLINE = "https://b2c.csair.com/B2C40/newTrips/static/main/page/success/index.html?orderNo="
global isTest
isTest = True

#刷新规则
def rule(driver):
    i = randint(1,2)
    print(i)
    if i == 1:
        js_a = "abTest.abTestRule( {code: 'ab:bookingflow-1.0.0',condition: {city: '广州市',}})"
        driver.execute_script(js_a)
        print("执行ab规则js")
        print('rule_a')
    else:
        js_b = "abTest.abTestRule( {code: 'ab:bookingflow-1.0.0',condition: {city: '北京市',}})"
        driver.execute_script(js_b)
        print("执行ab规则js")   
        print('rule_b')

#获取cookie
def getCookie(cookies, name) :
    if len(cookies) == 0 :
        return ""
    value = ""
    for cookie in cookies :
        if cookie["name"] == name :
            value = cookie["value"]
            break
    return value


# def open():
#     #打开浏览器输入URL
#     driver = webdriver.Chrome()
#     url1 = "https://www.csair.test.com/cn/index.shtml"
#     driver.get(url1)
#     driver.maximize_window()
#登录
def login(driver):
    time.sleep(5)
    login = driver.find_element_by_link_text("登录")#通过link-text的文字链接定位元素
    login.click()
    print("login")
    #time.sleep(8)
    driver.implicitly_wait(10)
    use_name = driver.find_element_by_class_name("greyfont")
    use_name.click()
    use_name.clear()
    use_name.send_keys("018211480003")
    time.sleep(3)
    print("输入用户名成功")
    pwd1 = driver.find_element_by_id("passWordPH")
    pwd1.click()
    pwd2 = driver.find_element_by_id("passWord")
    pwd2.click()
    pwd2.clear()
    pwd2.send_keys("123123")
    print("输入密码")
    agree = driver.find_element_by_id("loginProtocol")
    agree.click()
    button = driver.find_element_by_class_name("login-btn")
    button.submit()#提交登录信息
    print("登录成功")
    time.sleep(40)#此处发现页面跳转耗时很长，所以这里强制等待
    #回到首页
    home = driver.find_element_by_link_text("首页")
    home.click()
    

def search(driver):
    time.sleep(15)
    driver.find_element_by_id("fDepCity").click()
    driver.find_element_by_id("fDepCity").clear()
    driver.find_element_by_id("fDepCity").send_keys(u"广州")
    driver.implicitly_wait(2)
    print("选择出发地")
    #driver.find_element_by_id("fArrCity").clear()
    driver.find_element_by_id("fArrCity").click()
    driver.find_element_by_id("fArrCity").send_keys(u"北京")
    time.sleep(5)
    print("北京")
    print("选择目的地")
    #选择出发日期
    js = "$('input[id=fDepDate]').removeAttr('readonly')" # jQuery，移除属性将日期设置为可以输入的文本框
    driver.execute_script(js)
    date = driver.find_element_by_id('fDepDate')
    date.clear()
    date.send_keys('2019-07-16')
    print("enter")
    time.sleep(4)
    driver.minimize_window()
    print("重置出发日期")
    driver.find_element_by_class_name("searchFlight").click()

#关闭浏览器
def broswer_quit(driver):
    driver.add_cookie({'name':'testFrom','value':'baozi'})
    time.sleep(5)
    cookie = driver.get_cookies()
    print("打印cookie信息:%s"%cookie)
    driver.delete_all_cookies()#s删除所有的cookie
    print("清除所有的cookie")
    print("等待中...")
    time.sleep(5)
    driver.quit()

#选择航班A
def fly_a(driver):
    driver.maximize_window()
    time.sleep(25)
    air = driver.find_element_by_class_name("current")
    driver.execute_script("arguments[0].scrollIntoView();", air)#鼠标滑到到此元素
    ActionChains(driver).click_and_hold(air).perform()
    print("滑动鼠标显示第一个航班选项")
    time.sleep(10)
    seat = driver.find_element_by_class_name("fligthR").find_element_by_xpath("//*[@id='zls-common']/div[3]/div[2]/ul/li[1]/div[2]/ul/li[4]")
    print("层级定位")
    seat.click()
    #seat.click()#这里的class首次点击会有变化，所以要click两次
    print("定位点击")
    driver.implicitly_wait(15)
    driver.find_element_by_xpath("//*[@id='zls-common']/div[3]/div[2]/ul/li[1]/div[3]/ul/li[1]/div/div[3]/div/div[1]").click()#立即预订
    print("选择座位类型")
    time.sleep(8)
    driver.add_cookie({'name':'testFrom','value':'baozi'})

#选择航班B
def fly_b(driver):
    driver.maximize_window()
    time.sleep(25)
    air = driver.find_element_by_class_name("current")
    driver.execute_script("arguments[0].scrollIntoView();", air)#鼠标滑到到此元素
    ActionChains(driver).click_and_hold(air).perform()
    print("滑动鼠标显示第一个航班选项")
    time.sleep(10)
    seat = driver.find_element_by_xpath("//*[@id='contenter']/div[2]/div[3]/div/div[2]/ul[2]").find_element_by_xpath("//*[@id='contenter']/div[2]/div[3]/div/div[2]/ul[2]/li[5]")
    print("层级定位")
    seat.click()
    print("定位点击")
    driver.implicitly_wait(15)
    driver.find_element_by_xpath("//*[@id='contenter']/div[2]/div[3]/div/div[2]/ul[2]/li[6]/div[1]/div/div[3]/a").click()#立即预订
    print("选择座位类型")
    time.sleep(8)
    driver.add_cookie({'name':'testFrom','value':'baozi'})

#填写信息A
#异常信息
def infor_a(driver):
    
    #快捷填写信息
    passenger = driver.find_element_by_class_name("checkbox")
    driver.execute_script("arguments[0].scrollIntoView();", passenger)#鼠标滑到到此元素
    ActionChains(driver).click_and_hold(passenger).perform()
    time.sleep(3)
    passenger.click()
    print("勾选常用联系人")
    agree = driver.find_element_by_id("pro-check")
    driver.execute_script("arguments[0].scrollIntoView();", agree)#鼠标滑到到此元素
    ActionChains(driver).click_and_hold(agree).perform()
    time.sleep(2)
    agree.click()
    print("同意接受条款")
    #提取cookie信息
    cookies = driver.get_cookies()
    grayAbCookies = {"uuid":getCookie(cookies, "gabUuid"), "sid":getCookie(cookies, "gabSid"), "grayCode":getCookie(cookies, "grayValue"), "userId":getCookie(cookies, "userId"), "area":getCookie(cookies, "area")}
    #提交订单
    submit = driver.find_element_by_id("goNext")
    submit.click()
    print("提交订单")
    time.sleep(5)
    #写入灰度ABcookies
    driver.add_cookie({"domain":"58.248.41.144", "name":"gabUuid", "value":"" if grayAbCookies["uuid"] == None else grayAbCookies["uuid"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"gabSid", "value":"" if grayAbCookies["sid"] == None else grayAbCookies["sid"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"grayValue", "value":"" if grayAbCookies["grayCode"] == None else grayAbCookies["grayCode"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"userId", "value":"" if grayAbCookies["userId"] == None else grayAbCookies["userId"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"area", "value":"" if grayAbCookies["area"] == None else grayAbCookies["area"], "path":"/", "expires":None})
    driver.refresh()
    print("写入cookie")

#填写信息B
def infor_b(driver):
    passenger = driver.find_element_by_id("comm1002048238")
    driver.execute_script("arguments[0].scrollIntoView();", passenger)#鼠标滑到到此元素
    ActionChains(driver).click_and_hold(passenger).perform()
    time.sleep(3)
    passenger.click()
    print("勾选常用联系人B")
    agree = driver.find_element_by_id("protocol-checkbox")
    driver.execute_script("arguments[0].scrollIntoView();", agree)#鼠标滑到到此元素
    ActionChains(driver).click_and_hold(agree).perform()
    time.sleep(2)
    agree.click()
    print("同意接受条款B")
    #提取cookie信息
    cookies = driver.get_cookies()
    grayAbCookies = {"uuid":getCookie(cookies, "gabUuid"), "sid":getCookie(cookies, "gabSid"), "grayCode":getCookie(cookies, "grayValue"), "userId":getCookie(cookies, "userId"), "area":getCookie(cookies, "area")}
    submit = driver.find_element_by_id("submitForm")
    submit.click()
    print("提交订单B")
    time.sleep(5)
    #写入灰度ABcookies
    driver.add_cookie({"domain":"58.248.41.144", "name":"gabUuid", "value":"" if grayAbCookies["uuid"] == None else grayAbCookies["uuid"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"gabSid", "value":"" if grayAbCookies["sid"] == None else grayAbCookies["sid"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"grayValue", "value":"" if grayAbCookies["grayCode"] == None else grayAbCookies["grayCode"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"userId", "value":"" if grayAbCookies["userId"] == None else grayAbCookies["userId"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"area", "value":"" if grayAbCookies["area"] == None else grayAbCookies["area"], "path":"/", "expires":None})
    driver.refresh()
    print("写入cookie")

#获取订单刷新支付
def payment(driver):
    #获取订单号
    time.sleep(3)
    orderNo = driver.find_element_by_xpath("//meta[@name='WT.tx_i']").get_attribute("content")
    print("获取订单号")
    #生成支付成功链接
    paySuccessUrl = (PAY_SUCCESS if isTest else PAY_SUCCESS_ONLINE) + orderNo
    driver.get(paySuccessUrl)
    print("刷新支付")
    time.sleep(5)

# #访问首页登录后退出
# driver = webdriver.Chrome()
# url1 = "https://www.test.csair.com/cn/index.shtml"
# driver.get(url1)
# driver.maximize_window()
# try:
#     login(driver)
# except BaseException:
#     broswer_quit(driver)
#     print("访问首页后退出")



def main():
    print("#访问首页登录后退出")
    try:
        driver = webdriver.Chrome()
        url1 = "https://www.test.csair.com/cn/index.shtml"
        driver.get(url1)
        driver.maximize_window()
        print("登录账号")
        login(driver)
        broswer_quit(driver)
    except BaseException:
        print("登录异常退出")
        broswer_quit(driver)
        
    print("#搜索航班后退出")   
    try:
        driver = webdriver.Chrome()
        url1 = "https://www.test.csair.com/cn/index.shtml"
        driver.get(url1)
        driver.maximize_window()
        time.sleep(3)
        print("刷新规则") 
        rule(driver)       
        print("搜索航班")
        search(driver) 
        print("跳转航班列表页面后退出")
        broswer_quit(driver)
    except BaseException:
        print("搜索航班异常退出")
        broswer_quit(driver)
        
    print("#选择航班后退出")   
    try:
        driver = webdriver.Chrome()
        url1 = "https://www.test.csair.com/cn/index.shtml"
        driver.get(url1)
        driver.maximize_window()   
        time.sleep(3)
        print("登录")
        login(driver)
        print("刷新规则") 
        rule(driver)       
        print("搜索航班")
        search(driver) 
        print("填写页面信息")
        try:
            fly_a(driver)
        except BaseException:
            print("切换流程B") 
            time.sleep(3)         
            fly_b(driver)
        print("进入信息填写页面后退出")
        broswer_quit(driver)
    except BaseException:
        print("选择航班异常退出")
        broswer_quit(driver)
    print("#进入支付页面后退出")
    try:
        driver = webdriver.Chrome()
        url1 = "https://www.test.csair.com/cn/index.shtml"
        driver.get(url1)
        driver.maximize_window()   
        time.sleep(3)
        print("登录")
        login(driver)
        print("刷新规则") 
        rule(driver)       
        print("搜索航班")
        search(driver) 
        print("填写页面信息")
        try:
            fly_a(driver)
        except BaseException:
            print("切换流程B") 
            time.sleep(3)         
            fly_b(driver)
        time.sleep(5)
        print("填写信息页面")
        try:
           time.sleep(5)
           infor_a(driver)
        except BaseException:
            print("切换页面B")
            infor_b(driver)
        print("提交订单进入支付页面后退出")
        broswer_quit(driver)
    except BaseException:
        print("信息填写页面异常退出")
        broswer_quit(driver)

    print("#刷新支付后退出")
    try:
        driver = webdriver.Chrome()
        url1 = "https://www.test.csair.com/cn/index.shtml"
        driver.get(url1)
        driver.maximize_window()   
        time.sleep(3)
        print("登录")
        login(driver)
        print("刷新规则") 
        rule(driver)       
        print("搜索航班")
        search(driver) 
        print("填写页面信息")
        try:
            fly_a(driver)
        except BaseException:
            print("切换流程B") 
            time.sleep(3)         
            fly_b(driver)
        time.sleep(5)
        print("填写信息页面")
        try:
           time.sleep(5)
           infor_a(driver)
        except BaseException:
            print("切换页面B")
            infor_b(driver)
        print("完成支付页面")
        time.sleep(3)
        payment(driver)
        print("刷新支付成功页面后退出")
        broswer_quit(driver)
    except BaseException:
        print("刷新支付异常退出")
        broswer_quit(driver)
        main()

a = 0
while True:
    main()
    a = a+1
    print("执行次数是%s"%a)
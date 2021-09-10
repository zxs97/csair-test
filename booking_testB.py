#conding = utf-8

"""
 南方航空首页下单测试B
    author:南方航空,csair.com
"""

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#conding = utf-8

PAY_SUCCESS = "https://ec.test.csair.com/B2C40/newTrips/static/main/page/success/index.html?orderNo="
PAY_SUCCESS_ONLINE = "https://b2c.csair.com/B2C40/newTrips/static/main/page/success/index.html?orderNo="
global isTest
isTest = True
#定义一个函数
def getCookie(cookies, name) :
    if len(cookies) == 0 :
        return ""
    value = ""
    for cookie in cookies :
        if cookie["name"] == name :
            value = cookie["value"]
            break
    return value


def south(driver):
    #conding = utf-8
    #打开浏览器输入URL
    #driver = webdriver.Chrome()
    #url = "http://www.test.csair.com/cn/index.shtml"
    #driver.get(url)
    #print("访问首页")
    #driver.maximize_window()

    #点击登录
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
    driver.add_cookie({'name':'testFrom','value':'baozi'})

   #执行AB规则js
    js_ab = "abTest.abTestRule( {code: 'ab:bookingflow-1.0.0',condition: {city: '北京'}})"
    driver.execute_script(js_ab)
    print("执行ab规则js")
    #选择往返地
    time.sleep(15)
    driver.find_element_by_id("fDepCity").click()
    #driver.find_element_by_id("fDepCity").send_keys(u"广州广州")#触发报错场景
    #time.sleep(2)
    driver.find_element_by_id("fDepCity").clear()
    driver.find_element_by_id("fDepCity").send_keys(u"广州")
    driver.implicitly_wait(2)
    print("选择出发地")
    #driver.find_element_by_id("fArrCity").clear()
    driver.find_element_by_id("fArrCity").click()
    driver.find_element_by_id("fArrCity").send_keys(u"北京")
    time.sleep(5)
    print("北京")
    #driver.find_element_by_id("fArrCity").clear()
    #driver.find_element_by_id("fArrCity").send_keys(u"北京")
    #time.sleep(3)
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
    #time.sleep(15)
    driver.find_element_by_class_name("searchFlight").click()

    #选择航班
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
    #seat.click()#这里的class首次点击会有变化，所以要click两次
    print("定位点击")
    driver.implicitly_wait(15)
    driver.find_element_by_xpath("//*[@id='contenter']/div[2]/div[3]/div/div[2]/ul[2]/li[6]/div[1]/div/div[3]/a").click()#立即预订
    print("选择座位类型")
    time.sleep(8)
    driver.add_cookie({'name':'testFrom','value':'baozi'})
    #填写旅客信息
  
    #快捷填写信息
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
    time.sleep(3)
    #写入灰度ABcookies
    driver.add_cookie({"domain":"58.248.41.144", "name":"gabUuid", "value":"" if grayAbCookies["uuid"] == None else grayAbCookies["uuid"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"gabSid", "value":"" if grayAbCookies["sid"] == None else grayAbCookies["sid"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"grayValue", "value":"" if grayAbCookies["grayCode"] == None else grayAbCookies["grayCode"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"userId", "value":"" if grayAbCookies["userId"] == None else grayAbCookies["userId"], "path":"/", "expires":None})
    driver.add_cookie({"domain":"58.248.41.144", "name":"area", "value":"" if grayAbCookies["area"] == None else grayAbCookies["area"], "path":"/", "expires":None})
    driver.refresh()
    print("写入cookie")
    
    #获取订单号
    orderNo = driver.find_element_by_xpath("//meta[@name='WT.tx_i']").get_attribute("content")
    print("获取订单号")
    #生成支付成功链接
    time.sleep(8)
    paySuccessUrl = (PAY_SUCCESS if isTest else PAY_SUCCESS_ONLINE) + orderNo
    driver.get(paySuccessUrl)
    print("刷新支付")
    time.sleep(5)
    #选择支付方式
    # time.sleep(8)
    # pay_type = driver.find_element_by_class_name("newPayWayList")
    # driver.execute_script("arguments[0].scrollIntoView();", pay_type)#鼠标滑到到此元素
    # ActionChains(driver).click_and_hold(pay_type).perform()
    # time.sleep(3)
    # payment = driver.find_element_by_xpath("//*[@id='myBalance']")
    # payment.click()
    # print("选择帐户")
    # #pay_pwd
    # time.sleep(3)
    # pay_pwd = driver.find_element_by_xpath("//*[@id='input_psw']")
    # pay_pwd.send_keys("9527")
    # print("输入错误的密码")
    # #pay_submit
    # pay_button = driver.find_element_by_name("upp_pay_btn")
    # pay_button.click()
    # time.sleep(3)
    # print("提交支付")
    # time.sleep(3)
    # result = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/p/font").text
    # print(result)
    
    #payment.click()
    #未有选择支付方式直接支付
    #pay_button = driver.find_element_by_name("upp_pay_btn")
    #driver.execute_script("arguments[0].scrollIntoView();", pay_button)#鼠标滑到到此元素
    #ActionChains(driver).click_and_hold(pay_button).perform()
    #time.sleep(3)
    #alert = driver.switch_to.alert
    #alert.accept()
    #pay_button.click()
    #driver.switch_to.alert.accept()
    #选择支付方式点击支付
    #pay = driver.find_element_by_xpath("/html/body/form/div[1]/div[3]/div[4]/ul[2]/div/div[1]/div[1]/li/img")
    #driver.implicitly_wait(10)
    #pay.click()
    #driver.implicitly_wait(10)
    #pay_button = driver.find_element_by_name("upp_pay_btn")
    #pay_button.click()
    #time.sleep(3)

    # #选择支付方式
    # driver.implicitly_wait(30)
    # pay_type = driver.find_element_by_class_name("newPayWayList")
    # driver.execute_script("arguments[0].scrollIntoView();", pay_type)#鼠标滑到到此元素
    # ActionChains(driver).click_and_hold(pay_type).perform()
    # time.sleep(3)
    # payment = driver.find_element_by_xpath("/html/body/form/div[1]/div[3]/div[3]/ul/li[2]")
    # payment.click()
    # payment.click()
    # #未有选择支付方式直接支付
    # pay_button = driver.find_element_by_name("upp_pay_btn")
    # driver.execute_script("arguments[0].scrollIntoView();", pay_button)#鼠标滑到到此元素
    # ActionChains(driver).click_and_hold(pay_button).perform()
    # time.sleep(3)
    # alert = driver.switch_to.alert
    # alert.accept()
    # pay_button.click()
    # driver.switch_to.alert.accept()
    # #选择支付方式点击支付
    # pay = driver.find_element_by_xpath("/html/body/form/div[1]/div[3]/div[4]/ul[2]/div/div[1]/div[1]/li/img")
    # driver.implicitly_wait(10)
    # pay.click()
    # driver.implicitly_wait(10)
    # pay_button = driver.find_element_by_name("upp_pay_btn")
    # pay_button.click()
    # time.sleep(3)
    #
    # #回到首页
    # time.sleep(10)
    # home = driver.find_element_by_link_text("首页")
    # home.click()
    # #访问灰度入口
    # gray_fly =driver.find_element_by_class_name("nav-tabs")
    # driver.execute_script("arguments[0].scrollIntoView();", gray_fly)#鼠标滑到到此元素
    # ActionChains(driver).click_and_hold(gray_fly).perform()
    # time.sleep(3)
    # flight = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/div[1]/ul/li[1]")
    # flight.click()

def xunhuan():
    from selenium import webdriver
    import time
    #打开浏览器输入URL
    driver = webdriver.Chrome()
    url1 = "https://www.test.csair.com/cn/index.shtml"
    driver.get(url1)
    driver.maximize_window()
    #调用函数
    try:
        south(driver)
        afterProcess(driver, url1)
    except Exception as error:
        print("异常中断,error=%s" %error)
        afterProcess(driver, url1)

def afterProcess(driver, endUrl) :
    driver.get(endUrl)
    time.sleep(3)
    cookie = driver.get_cookies()
    print("打印cookie信息:%s"%cookie)
    driver.delete_all_cookies()#s删除所有的cookie
    print("清除所有的cookie")
    print("等待中...")
    driver.quit()
    driver.close()

i = 0
while i<200:
    xunhuan()
    i = i+1
    print("执行次数是%s"%i)
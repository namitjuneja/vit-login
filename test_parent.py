def verify_student(reg_no = "13BEC0490", pwd = "orangearmour", mob_num = "9811206663"):

    
    import mechanize, json, datetime 
    from bs4 import BeautifulSoup
    from CaptchaParser import CaptchaParser
    from PIL import Image
          
    
    #browser initialise
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
 
    #open website
    response = br.open("https://academics.vit.ac.in/parent/parent_login.asp")
    print br.geturl()

    #select form
    br.select_form("parent_login")

    
    #extracting captcha url
    soup = BeautifulSoup(response.get_data())
    img = soup.find('img', id='imgCaptcha')
    print img['src']
    #retrieving captcha image
    br.retrieve("https://academics.vit.ac.in/parent/"+img['src'], "captcha_parent.bmp")
    print "captcha retrieved"
    img = Image.open("captcha_parent.bmp")

    parser = CaptchaParser()

    captcha = parser.getCaptcha(img)
    print str(captcha)
    #fill form
    br["wdregno"] = str(reg_no)
    br["wdpswd"] = str(pwd)
    br["wdmobno"] = str(mob_num)
    br["vrfcd"] = str(captcha)
    br.method = "POST"
    br.submit()
    print br.geturl()
    if br.geturl()==("https://academics.vit.ac.in/parent/home.asp"):
        print "SUCCESS"
        return {"status":"Success"}
    else :
        print "FAIL"
        return {"status":"Failure"}


def verify_student_data(reg_no, dob, mob_num):
    return verify_student(reg_no, dob, mob_num)

def get_timetable_data(reg_no, dob, mob_num):
    return get_timetable(reg_no, dob, mob_num)

def get_atten_data(reg_no, dob, mob_num):
    return get_atten(reg_no,dob, mob_num)

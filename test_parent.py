def get_class_details(reg_no = "", pwd = "", mob_num = ""):

    
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
    if br.geturl()==("https://academics.vit.ac.in/parent/home.asp"):
        print "SUCCESS"
   

        br.open("https://academics.vit.ac.in/parent/parent_home.asp")

        #opening academic history page

        response = br.open("https://academics.vit.ac.in/parent/student_history.asp")
        soup = BeautifulSoup(response.get_data())



        #extracting past grades

        curr_year = datetime.date.today().year
        curr_month = datetime.date.today().month
        past_grades = {}
        months = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}


        for i in range(1,len(soup('table')[2].findAll("tr"))):
            
            exam_date = soup('table')[2].findAll("tr")[i].findAll("td")[6].getText().encode('utf-8').replace("\xc2\xa0", " ")
            exam_month = months[exam_date[:3]]
            exam_year = int(exam_date[4:8])
            
            course_grade = soup('table')[2].findAll("tr")[i].findAll("td")[5].getText().encode('utf-8').replace("\xc2\xa0", " ")
            
            if curr_month < 6:
                if (exam_year == curr_year - 1) and (course_grade == "A" or course_grade == "S"):
                    course_code = soup('table')[2].findAll("tr")[i].findAll("td")[1].getText().encode('utf-8').replace("\xc2\xa0", " ")        #this part can be reduced
                    course_title = soup('table')[2].findAll("tr")[i].findAll("td")[2].getText().encode('utf-8').replace("\xc2\xa0", " ")
                    past_grades[course_code] = course_title
            elif curr_month > 5:
                if ((exam_year == curr_year and exam_month < 6) or (exam_year == curr_year - 1 and exam_month > 6)) and (course_grade == "A" or course_grade == "S"):
                    course_code = soup('table')[2].findAll("tr")[i].findAll("td")[1].getText().encode('utf-8').replace("\xc2\xa0", " ")        #this part can be reduced
                    course_title = soup('table')[2].findAll("tr")[i].findAll("td")[2].getText().encode('utf-8').replace("\xc2\xa0", " ")
                    past_grades[course_code] = course_title

        #opening timetable page

        response = br.open("https://academics.vit.ac.in/parent/timetable.asp?sem=WS")
        soup = BeautifulSoup(response.get_data())


        #extracting class details
        class_details = {}
        for i in range(1,len(soup('table')[1].findAll("tr")) - 1):
            class_nbr = soup('table')[1].findAll("tr")[i].findAll("td")[1].getText().encode('utf-8').replace("\xc2\xa0", " ")
            course_code = soup('table')[1].findAll("tr")[i].findAll("td")[2].getText().encode('utf-8').replace("\xc2\xa0", " ")
            course_title = soup('table')[1].findAll("tr")[i].findAll("td")[3].getText().encode('utf-8').replace("\xc2\xa0", " ")
            course_mode = soup('table')[1].findAll("tr")[i].findAll("td")[6].getText().encode('utf-8').replace("\xc2\xa0", " ")
            slot = soup('table')[1].findAll("tr")[i].findAll("td")[8].getText().encode('utf-8').replace("\xc2\xa0", " ")
            class_venue = soup('table')[1].findAll("tr")[i].findAll("td")[9].getText().encode('utf-8').replace("\xc2\xa0", " ")
            faculty_name = soup('table')[1].findAll("tr")[i].findAll("td")[10].getText().encode('utf-8').replace("\xc2\xa0", " ")
            class_details[class_nbr] = (slot, course_title, course_code, course_mode, class_venue, faculty_name)

        return {"status":"Success","class_details":class_details, "past_grades":past_grades}
    else :
        print "FAIL"
        return {"status":"Failure"}

###########################################################################################################################################

def get_timetable(reg_no = "", pwd = "", mob_num = ""):

    
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

    # response = br.open("https://academics.vit.ac.in/student/stud_login.asp")
    response = br.open("https://academics.vit.ac.in/parent/parent_login.asp")
    print br.geturl()

    #select form
    br.select_form("parent_login")

    
    #extracting captcha url
    soup = BeautifulSoup(response.get_data())
    img = soup.find('img', id='imgCaptcha')
    
    
    #retrieving captcha image
    br.retrieve("https://academics.vit.ac.in/parent/"+img['src'], "captcha_parent.bmp")
    
    # print str("https://academics.vit.ac.in/parent/"+img['src'], "captcha_parent")

    img = Image.open("captcha_parent.bmp")

    parser = CaptchaParser()

    captcha = parser.getCaptcha(img)   
    
    #fill form
    br["wdregno"] = str(reg_no)
    br["wdpswd"] = str(pwd)
    br["wdmobno"] = str(mob_num)
    br["vrfcd"] = str(captcha)
    br.method = "POST"
    br.submit()
    if br.geturl()==("https://academics.vit.ac.in/parent/home.asp"):
        print "SUCCESS"
   

        br.open("https://academics.vit.ac.in/parent/parent_home.asp")

        #opening timetable page
        response = br.open("https://academics.vit.ac.in/parent/timetable.asp?sem=WS")
        soup = BeautifulSoup(response.get_data())

        #extrating timetable
        time_table = {}
        for i in range(2,7):
            day = {}
            for j in range(1,13):
                day[j] = soup('table')[2].findAll("tr")[i].findAll("td")[j].getText().encode('utf-8').replace("\xc2\xa0", " ")
                if len(day[j]) > 10:
                    pass
                else:
                    day[j] = 0
            time_table[i-1] = day
        return {"status":"Success","timetable":time_table}

    else :
        print "FAIL"
        return {"status":"Failure"}



#########################################################################################################################################

def get_atten(reg_no = "", pwd = "", mob_num = ""):

    
    import mechanize, json, datetime, pytz
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

    # response = br.open("https://academics.vit.ac.in/student/stud_login.asp")
    response = br.open("https://academics.vit.ac.in/parent/parent_login.asp")
    print br.geturl()

    #select form
    br.select_form("parent_login")

    
    #extracting captcha url
    soup = BeautifulSoup(response.get_data())
    img = soup.find('img', id='imgCaptcha')
    
    
    #retrieving captcha image
    br.retrieve("https://academics.vit.ac.in/parent/"+img['src'], "captcha_parent.bmp")
    
    # print str("https://academics.vit.ac.in/parent/"+img['src'], "captcha_parent")

    img = Image.open("captcha_parent.bmp")

    parser = CaptchaParser()

    captcha = parser.getCaptcha(img)   
    
    #fill form
    br["wdregno"] = str(reg_no)
    br["wdpswd"] = str(pwd)
    br["wdmobno"] = str(mob_num)
    br["vrfcd"] = str(captcha)
    br.method = "POST"
    br.submit()
    if br.geturl()==("https://academics.vit.ac.in/parent/home.asp"):
        print "SUCCESS"
   

        br.open("https://academics.vit.ac.in/parent/parent_home.asp")

        
        #attendance page 
        months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
        atten = {}
        response = br.open("https://academics.vit.ac.in/parent/attn_report.asp?sem=WS")
        soup = BeautifulSoup(response.get_data())

        br.select_form(nr=0)
        inputTag = soup.find(attrs={"name": "from_date"})
        from_date = inputTag['value']
        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.datetime.now(tz)
        to_date = str(now.day) + "-" + months[now.month] + "-" + str(now.year)
        
        response = br.open("https://academics.vit.ac.in/parent/attn_report.asp?sem=WS&fmdt=%(from_date)s&todt=%(to_date)s" % {"from_date":from_date, "to_date":to_date} )
        soup = BeautifulSoup(response.get_data())
        tables = soup.findAll("table")
        trs = soup.findAll("table")[len(tables)-2].findAll("tr")
        for i in range(1,len(trs)): #it should be len(trs) -1 but it works w/o -1
            a_course_code = soup.findAll("table")[len(tables)-2].findAll("tr")[i].findAll("td")[1].getText().encode('utf-8').replace("\xc2\xa0", " ")
            a_attend_percentage =  soup.findAll("table")[len(tables)-2].findAll("tr")[i].findAll("td")[8].getText().encode('utf-8').replace("\xc2\xa0", " ")
            if a_course_code not in atten.keys():
                atten[a_course_code] = [a_attend_percentage]
            else:
                atten[a_course_code+"_L"] = [a_attend_percentage]

        

        #marks page
        marks = {}
        response = br.open("https://academics.vit.ac.in/parent/marks.asp?sem=WS")
        soup = BeautifulSoup(response.get_data())

        tables = soup.findAll("table")
        trs = soup.findAll("table")[1].findAll("tr")
       
        for i in range(2,len(trs)): #it should be len(trs) -1 but it works w/o -1
            m_class_nbr = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[1].getText().encode('utf-8').replace("\xc2\xa0", " ")
            m_course_code = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[2].getText().encode('utf-8').replace("\xc2\xa0", " ")

            if (soup.findAll("table")[1].findAll("tr")[i].findAll("td")[5].getText().encode('utf-8').replace("\xc2\xa0", " ")!="N/A"):
                m_cat1_status = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[5].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_cat1_marks = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[6].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_cat2_status = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[7].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_cat2_marks = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[8].getText().encode('utf-8').replace("\xc2\xa0", " ")
                

                m_quiz1_status = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[9].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_quiz1_marks = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[10].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_quiz2_status =soup.findAll("table")[1].findAll("tr")[i].findAll("td")[11].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_quiz2_marks =  soup.findAll("table")[1].findAll("tr")[i].findAll("td")[12].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_quiz3_status =soup.findAll("table")[1].findAll("tr")[i].findAll("td")[13].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_quiz3_marks =  soup.findAll("table")[1].findAll("tr")[i].findAll("td")[14].getText().encode('utf-8').replace("\xc2\xa0", " ")

                m_ass_status = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[15].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_ass_marks = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[16].getText().encode('utf-8').replace("\xc2\xa0", " ")
                marks[m_course_code] = {"cat1":{"status":m_cat1_status, "marks":m_cat1_marks}, "cat2":{"status":m_cat2_status, "marks":m_cat2_marks}, "quiz1":{"status":m_quiz1_status, "marks":m_quiz1_marks}, "quiz2":{"status":m_quiz2_status, "marks":m_quiz2_marks}, "quiz3":{"status":m_quiz3_status, "marks":m_quiz3_marks}, "ass":{"status":m_ass_status, "marks":m_ass_marks}}

            else:
                m_lab_cam_status = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[6].getText().encode('utf-8').replace("\xc2\xa0", " ")
                m_lab_cam_marks = soup.findAll("table")[1].findAll("tr")[i].findAll("td")[7].getText().encode('utf-8').replace("\xc2\xa0", " ") 
                marks[m_course_code+"_L"] = {"status":m_lab_cam_status, "marks" : m_lab_cam_marks}             
           

        return {"status":"Success", "attendance":atten, "marks":marks}

    else :
        print "FAIL"
        return {"status":"Failure"}


def get_class_details_data(reg_no, dob, mob_num):
    return get_class_details(reg_no, dob, mob_num)

def get_timetable_data(reg_no, dob, mob_num):
    return get_timetable(reg_no, dob, mob_num)

def get_atten_data(reg_no, dob, mob_num):
    return get_atten(reg_no,dob, mob_num)

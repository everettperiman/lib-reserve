from datetime import *; from dateutil.relativedelta import *
from datetime import timedelta
from datetime import datetime
from webbot import Browser
import calendar
import time

class everett():
    def __init__(self,start,stop,url):
        self.website_url = url
        self.start = start
        self.stop = stop
        self.next_calendar_date()
        self.time_range(start,stop,self.year,self.month,self.day)
    
    def next_calendar_date(self):
        TODAY = date.today()    
        new = TODAY+relativedelta(weekday=MO)
        self.query_date = new.strftime("%A, %B %d, %Y")
        self.year, self.month, self.day = new.year, new.month, new.day
    
    def time_range(self,start,stop,year,month,day):
        time_list = []
        time_id = 's18022_'
        [(time_list.append((item,0)),time_list.append((item,30))) for item in range(start,stop+1)]
        time_list=time_list[:-1]
        time_str_list = ['{}-{}-{} {}:{}:0.0'.format(year,month,day,item[0],item[1]) for item in time_list]
        datetime_list = [datetime.strptime(item, '%Y-%m-%d %H:%M:%S.%f') for item in time_str_list]
        unix_list = [int(time.mktime(item.timetuple())) for item in datetime_list]
        self.id_list = [time_id+str(item) for item in unix_list]
        print(self.id_list)
        
    def click_all(self):
        for id_ in self.id_list:
            try:
                web.click("input",id=id_)
            except:
                print("Bad Time Slot {}".format(id_))
                
    def ucf_login(self,first,last,email,status,pid):
        web.type(first, into="First Name")
        web.type(last, into="Last Name")
        web.type(email, into="email")
        web.type("nick", into="Group Name")
        web.click(status)
        web.type(pid, into="UCFID")    
        # web.click("Submit my Booking")
                     
if __name__ == "__main__":
    website_url = 'https://ucf.libcal.com/spaces/accessible/2824'
    scraper = everett(9,12,website_url)
    web = Browser()
    web.go_to(scraper.website_url)
    web.click(scraper.query_date)
    web.click("Apply Filters")
    scraper.click_all()
    web.click("Submit Times")
    web.click("Continue")
    scraper.ucf_login("Everett",
                  "Periman",
                  "ejpman@knights.ucf.edu",
                  "Undergraduate Student",
                  "3815000")
    time.sleep(10)
    web.close_current_tab()

    
    
    
    

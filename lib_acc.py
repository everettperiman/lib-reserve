from datetime import *; from dateutil.relativedelta import *
from datetime import timedelta
from datetime import datetime
from webbot import Browser
import calendar
import time

class everett():
    def __init__(self,start,stop,url,room):
        self.website_url = url
        #May take out#####
        self.start = start
        self.stop = stop
        ##################
        next = self.next_calendar_date()
        ts_list = self.timestamp_range(start,stop,next[0],next[1],next[2])
        self.id_list = self.build_ids(room_id=room,timestamps=ts_list)

    def next_calendar_date(self):
        TODAY = date.today()    
        new = TODAY+relativedelta(weekday=MO)
        self.query_date = new.strftime("%A, %B %d, %Y")
        #May take out#####
        self.year, self.month, self.day = new.year, new.month, new.day
        ##################
        next_date = [new.year, new.month, new.day]
        return next_date

 """   Deprecated Method
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
 """

    def timestamp_range(self,start,stop,year,month,day):
        range_list = []
        #Create a list of alternating hour:0 and hour:30 to fill all time slots in range
        [(range_list.append((item,0)),range_list.append((item,30))) for item in range(start,stop+1)]
        #Remove last item in range_list because reserving on and ending on whole hours is desired
        #The range_list above creates an lasthour:30 which needs to be removed
        range_list=range_list[:-1]
        #Convert  range_list items into formatted datetime objects
        datetime_list = [datetime(year,month,day,item[0],item[1]) for item in range_list]
        #Convert datetime objects into timestamps
        timestamp_list = [int(time.mktime(item.timetuple())) for item in datetime_list]
        return timestamp_list

    def build_ids(self,room_id,timestamps):
        ts_ = timestamps
        #Append room id to all the timestamps to build correctly formatted ids for the website
        id_list = [room_id+str(item) for item in ts_]
        #May take out#####
        self.id_list = id_list
        ##################
        return id_list

    def click_all(self):
        for id_ in self.id_list:
            try:
                web.click("input",id=id_)
            except:
                print("Bad Time Slot {}".format(id_))

    def ucf_login(self,first,last,email,status,pid,non_test=None):
        web.type(first, into="First Name")
        web.type(last, into="Last Name")
        web.type(email, into="email")
        web.type("nick", into="Group Name")
        web.click(status)
        web.type(pid, into="UCFID")    
        if non_test:
            web.click("Submit my Booking")
                  
if __name__ == "__main__":
    website_url = 'https://ucf.libcal.com/spaces/accessible/2824'
    #Hour Calls are out of 24 and can only reserve whole hours i.e(9:00-12:00)
    scraper = everett(9,12,website_url,'s18022_')
    #Init browser object
    web = Browser()
    #Goto website
    web.go_to(scraper.website_url)
    #Select next date from drop down box
    web.click(scraper.query_date)
    #Self explanatory
    web.click("Apply Filters")
    #Select all ids that fall in the time range
    scraper.click_all()
    #Self explanatory
    web.click("Submit Times")
    #Self explanatory
    web.click("Continue")
    #Go through all the login boxes and submit request for the room 
    #***Must include non_test=True if you want the script to reserve the room***
    scraper.ucf_login("Everett",
                  "Periman",
                  "ejpman@knights.ucf.edu",
                  "Undergraduate Student",
                  "3815000")
    time.sleep(10)
    web.close_current_tab()
    
    
    
    

from datetime import *; from dateutil.relativedelta import *
from datetime import timedelta
from datetime import datetime
from webbot import Browser
import calendar
import time
import csv

class everett():
    def __init__(self,start,stop,url,room,d_bug=False):
        self.d_bug = d_bug
        self.pull_login()
        self.website_url = url
        next = self.next_calendar_date()
        ts_list = self.timestamp_range(int(self.room_text[0]),
                                       int(self.room_text[1]),
                                       next[0],
                                       next[1],
                                       next[2])
        self.id_list = self.build_ids(room_id=str(self.room_text[2]),timestamps=ts_list)
        
    def pull_login(self):
        with open("login.txt") as login_file:
            room_text = next(csv.reader(login_file))
            login_text = next(csv.reader(login_file))
            print(room_text)
            print(login_text)
        self.room_text = room_text
        self.login_info = login_text
        
    def next_calendar_date(self):
        TODAY = date.today()
        new = TODAY+relativedelta(weekday=MO)
        self.query_date = new.strftime("%A, %B %d, %Y")
        next_date = [new.year, new.month, new.day]
        if self.d_bug:
            print("caldate")
            print(next_date)
        return next_date

    def timestamp_range(self,start,stop,year,month,day):
        #Create a list of alternating hour:0 and hour:30 to fill all time slots in range
        #Remove last item in range_list because reserving on and ending on whole hours is desired
        #The range_list above creates an lasthour:30 which needs to be removed
        #Convert  range_list items into formatted datetime objects
        #Convert datetime objects into timestamps
        range_list = []
        [(range_list.append((item,0)),range_list.append((item,30))) for item in range(start,stop+1)]
        range_list=range_list[:-1]
        datetime_list = [datetime(year,month,day,item[0],item[1]) for item in range_list]
        timestamp_list = [int(time.mktime(item.timetuple())) for item in datetime_list]
        if self.d_bug:
            print("timestamps")
            print(timestamp_list)
        return timestamp_list

    def build_ids(self,room_id,timestamps):
        #Append room id to all the timestamps to build correctly formatted ids for the website
        ts_ = timestamps
        id_list = [room_id+str(item) for item in ts_]
        if self.d_bug:
            print("build ids")
            print(id_list)
        return id_list

    def click_all(self):
        el_free=[]
        el_taken=[]
        for id_ in self.id_list:
            try:
                if (web.exists("input",id=id_) and len(el_free) <= 7):
                    el_free.append(id_)
                    web.click("input",id=id_)
                else:
                    el_taken.append(id_)
            except:
                print("Bad Time Slot {}".format(id_))
        print("Taken Time Slots {}".format(el_taken))
        if self.d_bug:
            print("click loop, {} good, {} bad".format(len(el_free),len(el_taken)))

    def ucf_login(self,non_test=None):
        login_info = self.login_info
        print("login")
        web.type(login_info[0], into="First Name")
        web.type(login_info[1], into="Last Name")
        web.type(login_info[2], into="email")
        web.type("nick", into="Group Name")
        web.click("Undergraduate Student")
        web.type(login_info[3], into="UCFID")
        if non_test:
            web.click("Submit my Booking")

if __name__ == "__main__":
    #Hour Calls are out of 24 and can only reserve whole hours i.e(9:00-12:00)
    #Init browser object
    #Select next date from drop down box
    #Select all ids that fall in the time range
    #Go through all the login boxes and submit request for the room
    #***Must include non_test=True if you want the script to reserve the room***
    website_url = 'https://ucf.libcal.com/spaces/accessible/2824'
    scraper = everett(17,18,website_url,'s18022_')
    web = Browser()
    web.go_to(scraper.website_url)
    web.click(scraper.query_date)
    web.click("Apply Filters")
    scraper.click_all()
    web.click("Submit Times")
    web.click("Continue")
    scraper.ucf_login()
    time.sleep(10)
    web.close_current_tab()

import requests
import re
import datetime
import time

class Holiday:
    _html=""
    api_url=""
    date = []
    name = []
    def get_url(self,y,m):
            url="http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?serviceKey=zRuxSFejoJKPbOZdUuxyIUWJF7R56lxvA5LbRwxQWj8IVxCG2F6aYImQvUJIdzvjM3EDvvYQfrQyIirNaYWkqA%3D%3D"
            year="&solYear="+y
            month="&solMonth="+m
            self.api_url=url+year+month
            return self.api_url

    def get_html(self,url):
            self._html = ""
            resp = requests.get(url)
            if resp.status_code == 200:
                    self._html = resp.text
                    
            return self._html

    def get_date(self):
        #year=["2018","2019","2020"]
        month=["01","02","03","04","05","06","07","08","09","10","11","12"]

        for i in month:
                data = self.get_html(self.get_url(str(datetime.datetime.now().year),i))
                dateName = re.findall('\<dateName\>(.*?)\<\/dateName\>', data)
                locdate = re.findall('\<locdate\>(.*?)\<\/locdate\>', data)
                if locdate!=[]:
                    self.name.extend(dateName)
                    self.date.append(locdate)
        self.date=[y for x in self.date for y in x]
        self.date=list(map(int,self.date))

    def __init__(self):
        self.get_date()
    #메소드추가
    def isHoliday(self, a = None):
        if a is None:
            a = time.strftime('%Y%m%d')
        #a = 20180606 테스트용 현충일
        i = -1
        try:
            i = self.date.index(a)
        except ValueError:
            pass
        if datetime.datetime.now().weekday() >=5:
            i = -2
        return i
    
    def getDayName(self, index):
        if index == -1:
            return None
        else:
            return self.name[index]
        
        
if __name__ == "__main__":       
    h = Holiday()
    print(h.date)
    print(h.name)
    if h.getDayName(h.isHoliday()) is None:
        print("none")
    else:
        print(h.getDayName(h.isHoliday()))


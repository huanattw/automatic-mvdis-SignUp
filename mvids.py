import configparser
from datetime import timedelta, date
import os
import re
import time
import requests
from bs4 import BeautifulSoup as bs


class getTest:
    def __init__(self, information):
        self.info = information
        self.locate = [60, 64]
        self.today = date.today()
        self.dates = [self.today+timedelta(30)]
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        self.BaseURL = "https://www.mvdis.gov.tw/m3-emv-trn/exm/"
        self.locationURL = "{}locations".format(self.BaseURL)
        self.signupURL = "{}/signUp".format(self.BaseURL)
        self.queryURL = "{}/query".format(self.BaseURL)
        self.avail = list()

    def Consolelog(self, msg):
        temp = "{} {} ".format(time.strftime(
            "[%Y-%m-%d %H:%M:%S]", time.localtime()), msg)
        print(temp)

    def LineNotifyLog(self, msg):
        headers = {
            "Authorization": "Bearer " + self.info[5],
            "Content-Type": "application/x-www-form-urlencoded"
        }
        temp = "{} {} ".format(time.strftime(
            "[%Y-%m-%d %H:%M:%S]", time.localtime()), msg)
        params = {"message": temp}
        requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)

    # 取得最新日期區間
    def updateDate(self):
        self.dates.clear()
        self.today = date.today()
        self.dates.append(self.today+timedelta(30))
        for i in range(1, 31):
            self.dates.append(self.today+timedelta(i))

    # 取得場次
    def query(self, dates):
        Y = dates.year-1911
        if (dates.month < 10):
            M = '0{}'.format(dates.month)
        else:
            M = dates.month()

        if(dates.day < 10):
            D = "0{}".format(dates.day)
        else:
            D = dates.day

        tempDate = "{}{}{}".format(Y, M, D)
        self.session.cookies.clear()
        payLoad = {
            'method': 'query',
            'secDateStr': '',
            'secId': '',
            'divid': '',
            'licenseTypeCode': 'A',
            'expectExamDateStr': tempDate,
            '_onlyWeekend': 'on',
            'dmvNoLv1': '60',
            'dmvNo': '64'
        }
        result = self.session.post(self.locationURL, data=payLoad)
        options = re.findall("preAdd\(.{22}\)", result.text)
        for op in options:
            tempOP = op.split('\'')
            info = [tempOP[1], tempOP[3], tempOP[5]]
            if (info not in self.avail):
                self.avail.append(info)

    def preadd(self, infos):
        payLoad = {
            'method': 'preAdd',
            'secDateStr': '',
            'secId': infos[1],
            'divId': infos[2],
            'licenseTypeCode': 'A',
            'expectExamDateStr': infos[0],
            '_onlyWeekend': 'on',
            'dmvNoLv1': self.locate[0],
            'dmvNo': self.locate[1]
        }
        result = self.session.post(self.signupURL, data=payLoad)

    def already(self):
        payLoad = {
            'method': 'query',
            'reservationPK': 0,
            'idNo': self.info[0],
            'birthdayStr': self.info[1]
        }
        result = self.session.post(self.queryURL, data=payLoad)
        if ("取消報名 Cancel" in result.text):
            return True
        else:
            return False


    def getError(self,result):
        errorList = list()
        soup = bs(result,'lxml')
        cities = str(soup.select('#headerMessage')[0])
        ress=cities[88:].split('<br/>')
        for res in ress:
            errorList.append(res.split('</td>')[0])
        return errorList


    # 報名
    def signUp(self, infos):
        payLoad = {
            'method': 'add',
            'secDateStr': infos[0],
            'secId': infos[1],
            'divId': infos[2],
            'dmvNo': self.locate[1],
            'licenseTypeCode': 'A',
            'otp': '',
            'idNo': self.info[0],
            'birthdayStr': self. info[1],
            'name': self.info[2],
            'contactTel': self.info[3],
            'email': self.info[4]
        }
        result = self.session.post(self.signupURL, data=payLoad)

        errors=self.getError(result.text)

        if(self.already()):
            self.Consolelog("已報名成功")
            exit()
        elif len(errors): #with error status -> print && exit 
            for error in errors:
                self.Consolelog(error)
            exit()


    def main(self):
        self.Consolelog("時間區間設定完成")
        while(1 == 1):
            if self.already():
                self.Consolelog("已報名成功")
                exit()
            for dates in self.dates:
                self.query(dates)
            self.Consolelog("場次取得完成 共有 {} 場".format(len(self.avail)))
            for avail in self.avail:
                self.Consolelog("正在報名 {} ".format(avail))
                self.preadd(avail)
                self.signUp(avail)
            self.updateDate()
            self.Consolelog("時間區間設定完成")


if __name__ == "__main__":
    configFilename = 'information.ini'
    if not os.path.isfile(configFilename):
        with open(configFilename, 'a') as f:
            f.writelines(["[Default]\n", "id = your id\n", "birth = yourBirth\n",
                         "name = yourname\n", "phone = yourphone\n", "email = yourmail\n", "token = YourToken\n"])
            print('input your info in infos.ini')
            f.close()
            exit()

    config = configparser.ConfigParser()
    config.read(configFilename)
    info = [config['Default']['id'], config['Default']['birth'], config['Default']
            ['name'], config['Default']['phone'], config['Default']['email'], config['Default']['token']]
    bot = getTest(info)
    bot.main()

#imports
import time,requests,schedule,keyboard
from PyP100 import PyP110
#class
class Controller:
    def __init__(self,down_time,cost_limit) -> None:
        self.down_time : [int] = down_time
        self.cost_limit : float = cost_limit
        self.smart_plug : PyP110.P110= PyP110.P110("192.168.x.xxx","user@email.com","password123") #device ip(can be found in the tapo phone app),tp-link user-mail and password
        self.response = {}
        self.update_response()
        
    def __str__(self) -> str:
        return f"This controller:\ndown time:{self.down_time}\ncost limit:{self.cost_limit}"
    def update_cost_limit_with_prompt(self):
        while True:
            print("Write new cost-limit in the terminal:")
            try:self.cost_limit = float(input())
            except:print("Not valid, try again") 
            else:
                print("value changed")
                break
    def update_down_time(self):
        l1 = []
        i = 0
        if(self.response=="no response"):
            time.sleep(60)
            self.update_response()
        for e in self.response:
            if float(e['SEK_per_kWh'])>float(self.cost_limit):
                l1.append(i)
            i+=1
        self.down_time=l1
        print(f"down time updated:{self.down_time}")#debug
    def update_response(self):
        d=time.localtime()
        s = 'https://www.elprisetjustnu.se/api/v1/prices/20{}/{}-{}_{}.json'.format(time.strftime("%y",d),time.strftime("%m",d),time.strftime("%d",d),'SE3')
        try:
            r = requests.get(s)
        except ConnectionError as e:
            print(e)
            self.response = "no response"
        else: 
            self.response = r.json()
        print("update response made") #debug
#other functions
def controlP110(c:Controller):
    dt = getattr(c,"down_time")
    sp = getattr(c,"smart_plug")
    h = currentHour()
    try:
        on = sp.get_status()
        if h in dt and on == True:
            sp.turnOff()
        elif h not in dt and on == False:
            sp.turnOn()
    except Exception as e:
        print("connection with smart-plug failed")
        print(e)
    print("smartplug connection made")#debug
def scheduler(c:Controller):
    schedule.every().hour.at(":00").do(controlP110,c)
    schedule.every().day.at("00:00").do(c.update_response)
    schedule.every().day.at("00:00").do(c.update_down_time) #debug change these back to 00:00 later 
def currentHour():
    return int(time.strftime("%H",time.localtime()))
    print("current hour fetched")#debug
#main
def main():
    c = Controller(0,1.2) 
    scheduler(c)
    c.update_down_time()
    controlP110(c)
    while True:
        schedule.run_pending()
        if keyboard.is_pressed('s'):
            input()
            c.update_cost_limit_with_prompt()
            c.update_down_time()#no api request needed => less risk of fault
            controlP110(c)
        while getattr(c,"response")=="no response": #not tested, but should go in loop if api connection fails until it works (or just indefinetly if not)
            time.sleep(60)
            c.update_response()
        #print(c)#DEBUG
        time.sleep(1)
main()

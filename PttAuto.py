#coding=utf-8
import telnetlib
import sys
import time
import json
import os
from getch import getch, pause
host = 'ptt.cc'
global account_password
account_password=[]
def login(host, user ,password) :
    global telnet
    telnet = telnetlib.Telnet(host)
    time.sleep(1)
    content = telnet.read_very_eager().decode('big5','ignore')
    if u"系統過載" in content :
        print "系統過載, 請稍後再來"
        sys.exit(0)
        

    if u"請輸入代號" in content:
        print "輸入帳號中..."
        telnet.write(user + "\r\n" )
        time.sleep(1)
        print "輸入密碼中..."
        telnet.write(password + "\r\n")
        time.sleep(5)
        content = telnet.read_very_eager().decode('big5','ignore')
        if u"密碼不對" in content:
           print "密碼不對或無此帳號。程式結束"
           sys.exit()
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"您想刪除其他重複登入" in content:
           #print '刪除其他重複登入的連線....'
           telnet.write("y\r\n")
           time.sleep(10)
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"請按任意鍵繼續" in content:
           #print "資訊頁面，按任意鍵繼續..."
           telnet.write("\r\n" )
           time.sleep(2)
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"您要刪除以上錯誤嘗試" in content:
           #print "刪除以上錯誤嘗試..."
           telnet.write("y\r\n")
           time.sleep(5)
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"您有一篇文章尚未完成" in content:
           #print '刪除尚未完成的文章....'
           # 放棄尚未編輯完的文章
           telnet.write("q\r\n")   
           time.sleep(5)   
           content = telnet.read_very_eager().decode('big5','ignore')
        #print "----------------------------------------------"
        #print "------------------ 登入完成 ------------------"
        #print "----------------------------------------------"
        print "login "+user+" success"
    else:
        print "沒有可輸入帳號的欄位，網站可能掛了"

def disconnect() :
     print "登出中..."
     # q = 上一頁，直到回到首頁為止，g = 離開，再見
     telnet.write("qqqqqqqqqg\r\ny\r\n" )
     time.sleep(3)
     #content = telnet.read_very_eager().decode('big5','ignore')
     #print content
     #print "----------------------------------------------"
     #print "------------------ 登出完成 ------------------"
     #print "----------------------------------------------"
     print "logout success"
     telnet.close()

def post(board, title, content) :
        print '發文中...'
        # s 進入要發文的看板
        telnet.write('s')
        telnet.write((board + '\r\n').encode('big5'))
        time.sleep(1)       
        telnet.write("q")                            
        time.sleep(2)        
        #請參考 http://donsnotes.com/tech/charsets/ascii.html#cntrl
        # Ctrl+P
        telnet.write('\x10') 
        # 發文類別
        telnet.write('1\r\n')
        telnet.write((title + '\r\n').encode('big5'))
        time.sleep(1)
        # Ctrl+X
        telnet.write((content +'\x18').encode('big5') )
        time.sleep(1)
        # 儲存文章
        telnet.write('s\r\n' )
        # 不加簽名檔
        telnet.write('0\r\n' )
        print "----------------------------------------------"
        print "------------------ 發文成功 ------------------"
        print "----------------------------------------------"

def main(host,user,password):
    login(host, user ,password)    
    #post('test', u'發文文字測試', u'這是一篇測試,哇哈哈')
    disconnect()     
def auto_login():
    global account_password
    for temp in account_password:
      user = temp[0]
      password = temp[1]
      main(host,user,password)
def in_menu():
    while(1):
        os.system('clear')
        print "press 1 for auto_login"
        print u"press 2 for 帶風向"
        print "press q for leave"
        command = getch()
        if command == 'S': 
            print 'YES'
        if command == "1" :
            auto_login()
        if command == "q":
            sys.exit()
        pause()
def load_exist_account():
    print "loading account and password..."
    if os.path.exists('account_password.txt') :
        f = open('account_password.txt','r')
        data = [line.strip() for line in open('account_password.txt', 'r')]
        for string in data :
            temp = string.split(' ')
            account_password.append(temp)
    print "finish loading"
if __name__=="__main__" :
    load_exist_account()
    in_menu()
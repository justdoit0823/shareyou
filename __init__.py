# -*- coding: utf-8 -*-

import tornado.web
import tornado.database
from tornado.options import define, options
import sys
from time import strftime

'''This part provide some basic functions and baserequest class'''


#sql define

define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="shareyou", help="blog database name")
define("mysql_user", default="justdoit", help="blog database user")
define("mysql_password", default="", help="blog database password")



class BaseHandler(tornado.web.RequestHandler):

    '''The base request handler class'''

    def initialize(self):
        self.db=tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database, user=options.mysql_user, password=options.mysql_password)

    def get_current_user(self):
        cuser=self.get_secure_cookie("user")
        if(cuser):
            user_sql="select account,id,img from user where account='%s'"%cuser
            user=self.db.get(user_sql)
            return user
        else:
            return None

    def clear_current_user(self):
        self.clear_cookie("user")


    
    
#compare the time
def cmptime(base,now):
    y=now[0]-base[0]
    m=now[1]-base[1]
    d=now[2]-base[2]
    h=now[3]-base[3]
    n=now[4]-base[4]
    s=now[5]-base[5]
    if(y>0):
        return strftime("%Y-%m-%d %X",base)
    if(m>0):
        return strftime("%Y-%m-%d %X",base)
    if(d>0):
        return strftime("%Y-%m-%d %X",base)
    if(h>=1 and n>=0):
        return str(h)+"小时前"
    elif(h>1 and n<0):
        return str(h-1)+"小时前"
    elif(h==1 and n<0):
        return str(60+n)+"分钟前"
    if(n>=1 and s>=0):
        return str(n)+"分钟前"
    elif(n>1 and s<0):
        return str(n-1)+"分钟前"
    elif(n==1 and s<0):
        return str(60+s)+"秒前"
    if(s>0):
        return str(s)+"秒前"


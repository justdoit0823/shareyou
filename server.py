# -*- coding: utf-8 -*-

'''
This file mainly handles web server's execution
'''

__version__ = "0.0.3"

from tornado import httpserver,ioloop,web,template

import tornado.options

import sys,os,time
import signal

from hashlib import sha224,md5
import random

from tornado.options import define,options


define("configfile", default="server.conf", help="config with this file", type=str)
define("port", default=10001, help="run on the given port", type=int)

from __init__ import BaseHandler




#rewrite RequestHandler


class IndexHandler(BaseHandler):

    '''This is the index page request handler class.'''

    def get(self):

        cuser = self.get_current_user()
        indexsql = "select id as bid,title,bloger from blog order by time desc limit 3"
        indexs = self.db.query(indexsql)
        self.render("index.html",cuser=cuser,indexs=indexs)

class AboutHandler(BaseHandler):

    def get(self):

        cuser=self.get_current_user()
        self.render("about.html",cuser=cuser)

class ContactHandler(BaseHandler):

    def get(self):

        cuser=self.get_current_user()
        self.render("contact.html",cuser=cuser)

class DownloadHandler(BaseHandler):

    def get(self):

        cuser=self.get_current_user()
        self.render("download.html",cuser=cuser)

class BlogHandler(BaseHandler):

    '''Blog indexs handler,show a short introduction of each blog.'''

    def get(self):
        cuser=self.get_current_user()
        page=int(self.get_argument("page",1))
        blogsql=("select blog.id as bid,title,content,blog.time,view,review,user.id,bloger "
                 "from blog join user on user.account=blog.bloger order by blog.time desc")
        blogs=self.db.query(blogsql)
        self.render("blog.html",cuser=cuser,blogs=blogs)

class UserBlogDetailHandler(BaseHandler):

    '''show the blog content page.'''

    def get(self,bid):
        cuser=self.get_current_user()
        blog_sql=("select user.id as uid,account,email,blog.id,title,content,bloger from user "
                  "join blog on user.account=blog.bloger where blog.id='%d'")%int(bid)
        blog=self.db.get(blog_sql)
        if(not blog):
            raise web.HTTPError(404,"no resource found.")
        blog.content=blog.content.replace("\\'","'")
        same = cuser and (cuser.id == blog.uid)
        if(not same):
            update_sql="update blog set view=view+1 where id='%d'"%(int(bid))
            self.db.execute(update_sql)
        review_sql=("select user.id as uid,account,img,content,rid,blogreview.time from user "
                    "join blogreview on user.account=blogreview.reviewer where blogreview.id='%d'"
                    "order by blogreview.time desc")%int(bid)
        rows=self.db.query(review_sql)
        for row in rows:
            row.content=row.content.replace("\\'","'")
        self.render("blogcontent.html",cuser=cuser,blog=blog,same=same,rows=rows)

class LoginHandler(BaseHandler):

    '''login website'''

    def get(self):
        goto=self.get_argument("next","/")
        self.render("login.html",goto=goto)

    def post(self):
        #print self.request
        #print self.request.arguments
        mal=self.get_argument("email")
        psw=self.get_argument("password")
        psw=sha224(psw).hexdigest()
        goto=self.get_argument("next","/")
        result=self.db.get("select id,account,active from user where email='%s' and password='%s'"%(mal,psw))
        at=time.strftime("%Y-%m-%d %X",time.localtime())
        ip=self.request.remote_ip
        if(result):
            if(result.active):
                 is_login=self.db.get("select id,account from userstatus where account='%s'"%result.account)
                 if(not is_login):
                     new_lgsql="insert into userstatus(id,account,ip,time) values('%d','%s','%s','%s')"%(result.id,result.account,ip,at)
                 else:
                     up_lgsql="update userstatus set ip='%s',time='%s' where account='%s'"%(ip,at,result.account)
                 self.db.execute(up_lgsql)
                 self.set_secure_cookie("user",result.account.encode("utf-8"),7)
                 self.redirect(goto)
            else:
                 tip="请完成邮箱激活"
                 #json=dict(msg=tip,goto='/user/action/login')
        else:
            tip="用户名或密码错误"
            #json=dict(msg=tip,goto='/user/action/login')
        self.write(tip)

class LogoutHandler(BaseHandler):

    '''logout website'''

    def get(self):
        cuser=self.get_current_user()
        ip=self.request.remote_ip
        self.clear_current_user()
        goto=self.get_argument("next","/")
        at=time.strftime("%Y-%m-%d %X",time.localtime())
        upsql="update userstatus set ip='%s',time='%s' where id='%d'"%(ip,at,cuser.id)
        self.db.execute(upsql)
        self.redirect(goto)

# rewrite template module

class HeaderModule(web.UIModule):

    '''The header module in the website pages.'''

    def render(self,user=None):

        return self.render_string("modules/header.html",user=user)

class BlogIndexModule(web.UIModule):

    '''The blog each index part page module.'''

    def render(self,blog):

        return self.render_string("modules/bloglist.html",blog=blog)

class FooterModule(web.UIModule):

    '''The footer module in the website pages.'''

    def render(self):

        return self.render_string("modules/footer.html")


#define modules table

MODULES = dict(
    Header = HeaderModule,
    Footer = FooterModule,
    BlogIndex = BlogIndexModule
    )

#server stop by signal SIGQUIT

def serverstop(signum,frame):
	
    exit(0)
	
 
        
#rewrite Application

class MyApplication(web.Application):

    '''The website application class'''

    def __init__(self):

        HandlerList=[
        (r"/", IndexHandler),
        (r"/about",AboutHandler),
        (r"/contact",ContactHandler),
        (r"/download",DownloadHandler),
        (r"/blog", BlogHandler),
        (r"/blog/([0-9]+)",UserBlogDetailHandler),
        (r"/user/action/login", LoginHandler),
        (r"/user/action/logout", LogoutHandler)
        ]
        settings=dict(
        cookie_secret="14124^3vvsdsdls;l;la;lwoeskfjs++kjks",
        login_url="/user/action/login",
        template_path=os.path.join(os.path.dirname(sys.argv[0]),"template"),
        static_path=os.path.join(os.path.dirname(sys.argv[0]),"static"),
        ui_modules=MODULES,
        gzip=True,
        )
        web.Application.__init__(self,HandlerList,debug=False,**settings)
        
        
def main():

    #load config file here for some arguments.
    tornado.options.parse_config_file(os.path.join(os.path.dirname(sys.argv[0]),options.configfile))
    tornado.options.parse_command_line()
    signal.signal(signal.SIGQUIT,serverstop)
    application = MyApplication()
    http_server = httpserver.HTTPServer(application,xheaders=True)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":

    main()

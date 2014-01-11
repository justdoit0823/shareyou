shareyou
========

	An open website,which id developed for communicating with others.The url is http://www.shareyou.net.cn/


file structure
==============

	shareyou-----
				|- __init__.py
				|- README.md
				|- server.conf
				|- server.py
				|- static----
				|			|- css----------------------
				|			|- js---					|- bootstrap.css
				|					|- bootstrap.js		|- common.css
				|					|- jquery.js		|- default.css
				|					|- kindeditor.js
				|- template--
							|- about.html
							|- blog.html
							|- blogcontent.html
							|- contact.html
							|- download.html
							|- index.html
							|- login.html
							|- modules---
										|- bloglist.html
										|- footer.html
										|- header.html
										
										
project structure
=================

	web server---
				|- frontend----------
				|					|- bootstrap
				|- backend---
							|- web framework(tornado)
							|- database (mysql)
							|- load balance (nginx)
							|- server machine os (centos)
							

other files don't push github
=============================

	server.conf (write your own config file for your web server.)
	
	schema.sql (write your own database tables's structure.)
	
	images (use iamges which your server needs.)
	


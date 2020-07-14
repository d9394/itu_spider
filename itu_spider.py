#!/usr/bin/env python
#coding=utf8

import re  
import urllib2
#import string
import pymysql
from time import sleep,ctime
import os
import sys
if sys.getdefaultencoding() != 'utf8' :
	reload(sys)
	sys.setdefaultencoding('utf8')
	
mysql_config = {
	"host": "localhost",
	"port": 3306,
	"user": "itu",
	"passwd": "..................",
	"db": "itu",
	"charset": "utf8"
}

repair = {
	"S5A - S5Z" : "S5       ",
}
country = {
	"United States":"United States of America",
	"England":"United Kingdom",
	"Scotland":"United Kingdom",
	"Hawaii":"United States of America",
	"So Africa":"South Africa",
	"Alaska":"United States of America",
	"New Jersey W, New York":"United States of America",
	"Sicily":"Italy",
	"Kingman Reef":"United States of America",
	"Isle of Man":"United Kingdom",
	"Guernsey":"United Kingdom",
	"Jersey":"United Kingdom",
	"Wales":"United Kingdom",
	"Kaliningrad":"Russia",
	"No Cook Is":"New Zealand",
	"So Cook Is":"New Zealand",
	"Zaire":"Congo",
	"Phillippines":"Philippines",
	"Cocos Keeling":"Australia",
	"Agalega":"Mauritius",
	"Malagasy Rep":"Madagascar",
	"Oregon W, Washington W, Wyoming":"United States of America",
	"California":"United States of America",
	"British Columbia":"Canada",
	"Alberta":"Canada",
	"Labrador":"Canada"
}
ITU = {
	"36": "Africa",
	"37": "Africa",
	"08": "North America",
	"28": "Europe",
	"11": "North America",
	"61": "Oceania",
	"75": "North America",
	"10": "North America",
	"57": "Africa",
	"62": "Oceania",
	"14": "South America",
	"53": "Africa",
	"67": "Antarctica",
	"72": "Antarctica",
	"68": "Africa",
	"60": "Oceania",
	"46": "Africa",
	"64": "Asia",
	"39": "Africa",
	"41": "Asia",
	"49": "Asia",
	"07": "North America",
	"63": "South America",
	"13": "South America",
	"15": "South America",
	"56": "Oceania",
	"03": "North America",
	"04": "North America",
	"09": "North America",
	"52": "Africa",
	"12": "South America",
	"45": "Asia",
	"73": "Antarctica",
	"65": "Oceania",
	"44": "Asia",
}

if __name__=='__main__':  
	global cursor, db
	try:
		db=pymysql.connect( **mysql_config )
	except Exception as e:
		print ("Mysql connect error! or %s" % e)
	else:
		try:
			cursor=db.cursor(pymysql.cursors.DictCursor)
		except Exception as e:
			print "Create cursor error! or %s" % e
			
		else:
			url= 'https://img.hcharts.cn/mapdata/custom/world-palestine.js'
			req= urllib2.Request(url)
			data = urllib2.urlopen(req).read()
#			p=re.compile(r'"hc-key":"(?P<hckey>\w*)","hc-a2":"\w*","name":"(?P<name>([A-Z]|[a-z]|\s)*)"', re.S)
			p=re.compile(r'"hc-key":"(?P<hckey>\w*)","hc-a2":"\w*","name":"(?P<name>([A-Z]|[a-z]|\s)*)".*?"continent":"(?P<continent>([A-Z]|[a-z]|\s|\(|\))*)"', re.S)
			t=[]
			for m in p.finditer(data) :
				t.append(m.groupdict())
			if not os.path.exists("/dev/shm/ITU.html"):
				url = 'https://www.qsl.net/yb0zdc/ITU.html'
				os.system("wget -O /dev/shm/ITU.html " + url)
			itu_file=open("/dev/shm/ITU.html", "r")
			data = itu_file.read()
			itu_file.close()
			os.system("rm -f /dev/shm/ITU.html")
			for ii in repair :
				if data.find(ii) :
					print(u"repair %s to %s" %(ii, repair[ii]))
				data = data.replace(ii, repair[ii])
			
			perfixdata=[]
			p3={}
			p = re.compile(r'(?P<prefix>([0-9]|[A-Z]).{1,32})(  |[A-Z] )(?P<country>[A-Z].*) CQ (?P<cq>([0-9]{1,2}|\,| )*) ITU (?P<itu>([0-9]{1,2}|\,| )*)')
			ref=re.compile(r'(-See-.{2,3}|-(([0-9]|[A-Z]){1,3}/[A-Z]{1,2})|-([0-9]|[A-Z]){1,4}) ',re.I)
			print "Start Scan."
			for m in p.finditer(data) :
				k = m.groupdict()
				p5=re.sub(ref,'',k['country']).replace('-',' ').replace('See','').strip()
				p6=""
				p8=""
				for p7 in t :
					if country.has_key(p5) :
						p9=country[p5]
						p5=p5+"("+p9+")"
					else :
						p9=p5
					if ((p9.find(p7['name'])>=0) or (p7['name'].find(p9)>=0)) : 
						p6=p7['hckey']
						break
				p1 = k['prefix'].split(',')
				for n in p1 :
					n = n.strip()
					if len(n)==1 :
						n = n + "0A-" + n + "9Z"
					elif len(n)==2 :
						if ord(n[1:2])>64 :
							n = n + "0-" + n + "9"
						else :
							n = n + "0-" + n + "Z"
					if n.find('-')>0 :
						p2 = n.split('-')
#						print "prefix %s " % p2
						start=p2[0].strip()
						end=p2[1].strip()
						if len(start)==1 :
							start = start + "0A"
						elif len(start)==2 :
							if ord(start[1:2])<64 :
								start = start + "A"
							else :
								start = start + "0" 
						if len(end)==1 :
							end = end + "9Z"
						elif len(end)==2 :
							if ord(end[1:2])<64 :
								end = end + "Z"
							else :
								end = end + "9"
						if start[2:3]=="A" and end[2:3]=="Z" and ord(start[1:2])>64 :
							start=start[0:2]+"0"
							end=end[0:2]+"9"
#						print "S:%s E:%s" % (start,end)
						for q1 in range(ord(start[1:2]),ord(end[1:2])+1) :
							if q1>=58 and q1<=64 :  #跳过符号
								continue
							for q2 in range(ord(start[2:3]),ord(end[2:3])+1) :
								if q2>=58 and q2<=64 :   #跳过符号
									continue
								p4=start[0:1]+chr(q1)+chr(q2)
#								print "prefix= %s" % p4
								if not p3.has_key(p4) or 1 :
									for q3 in k['cq'].split(',') :
										for q4 in k['itu'].split(',') :
											p8=p7['continent']
											if k['itu'] in ITU:
												p8=ITU[k['itu']]
											p3.update({p4:[p4,p5,q3.strip(),q4.strip(),p6,p8]})
					else :
#						print "prefix= %s" % n
						if not p3.has_key(n) or 1 :
							for q3 in k['cq'].split(',') :
								for q4 in k['itu'].split(',') :
									p8=p7['continent']
									if k['itu'] in ITU:
										p8=ITU[k['itu']]
									p3.update({n:[n,p5,q3.strip(),q4.strip(),p6,p8]})
#			print p3
			print "Total perfix: %d " % len(p3)
			itu_export={}
			for country in p3 :
				perfixdata.append(p3[country])
				itu_export[p3[country][0]] = p3[country][5].replace("Africa", "AF").replace("Europe","EU").replace("South America","SA").replace("North America", "NA").replace("Asia", "AS").replace("Oceania", "OC").replace("Antarctica", "AN")
				#亚洲:Asia 欧洲：Europe 非洲：Africa 拉丁美洲：Latin America/South America 北美洲：North America 大洋洲：Oceania 南极洲：Antarctica 缩写：[AF]非洲, [EU]欧洲, [AS]亚洲, [OA]大洋洲, [NA]北美洲, [SA]南美洲, [AN]南极洲。 
				if p3[country][5] == '':
					print p3[country]
#			print perfixdata
			if len(perfixdata)>100 :
				sql='truncate table perfix;'
				try:
					cursor.execute(sql)
					db.commit()
					print "Truncate perfix data."
				except Exception as e: 
					print "roolback %s with %s " % (sql,e)
					db.rollback()
				else :
					sql='insert into perfix (perfix , country, cqzone, ituzone, map_country, continent) values ( %s, %s, %s , %s, %s, %s);'
					try:
						cursor.executemany(sql, perfixdata)
						db.commit()
						print "Success Insert new perfix data"
					except Exception as e: 
						print "roolback %s with %s " % (sql,e)
						db.rollback()
			sql="UPDATE perfix a SET a.continent=( SELECT c.continent FROM ( SELECT b.continent as continent , b.cqzone as cqzone FROM perfix b WHERE  b.continent<>'' and b.map_country<>'' ) c where c.cqzone=a.cqzone  limit 0,1) WHERE a.continent=''"
			try:
				cursor.execute(sql)
				db.commit()
				print "Success Repair perfix continent"
			except Exception as e: 
				print "roolback %s with %s " % (sql,e)
				db.rollback()
			#继续添加生成TXT功能
			itu_file=open("/xxxx/ITU_file.txt", "w")
			itu_file.write(str(itu_export))
			itu_file.close()
			


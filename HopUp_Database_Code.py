import os
import urlparse
import psycopg2

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["JumpUpDB_URL"])

def create_project_table():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("create table if not exists PROJECT(ProjectID Integer,ProjectTitle text,UserName text,ProjectCategory text,ProjectSubCategory text,ProjectCountry text,ProjectImage text,ProjectDescription text,ProjectLocation text,ProjectFundDuration text,ProjectFundGoal text,Remaining text,StartTime text)")
    conn.commit()
    conn.close()

def add_project(pid,ptitle,un,pcat,psubcat,pcountry,pimage,pdesc,ploc,pfunddur,pfundgoal,rem,st):
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("insert into PROJECT values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(pid,ptitle,un,pcat,psubcat,pcountry,pimage,pdesc,ploc,pfunddur,pfundgoal,rem,st))
    conn.commit()
    conn.close()

def view_projects():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("select * from PROJECT")
    rows = curs.fetchall()
    conn.close()
    return rows

def search_projects_by_title(ptitle):
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("select * from PROJECT where ProjectTitle = %s",(ptitle,))
    rows = curs.fetchall()
    conn.close()
    return rows

def create_reward_table():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("create table if not exists REWARD(RewardID Integer,RewardTitle text,ProjectTitle text,UserName text,PledgedAmount integer,RewardDescription text,ExpectedMonth integer,ExpectedYear integer,ShippingDetails text,RewardLimit integer)")
    conn.commit()
    conn.close()

def add_reward(rid,rtitle,ptitle,un,pa,rdesc,expmonth,expyear,shippingDetails,rlimit):
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("insert into REWARD values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(rid,rtitle,ptitle,'  ',pa,rdesc,expmonth,expyear,shippingDetails,rlimit))
    conn.commit()
    conn.close()

def view_rewards():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("select * from REWARD")
    rows = curs.fetchall()
    conn.close()
    return rows

def create_personal_info_table():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("create table if not exists PERSONAL_INFO(InfoId integer,UserName text,ProfileImage text,FbUrl text,WebsiteUrl text,Location text,GitUrl text,Biography text)")
    conn.commit()
    conn.close()

def add_personal_info(infoid,un,pi,fb,web,loc,git,bio):
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("insert into PERSONAL_INFO values(%s,%s,%s,%s,%s,%s,%s,%s)",(infoid,' ',pi,fb,web,loc,git,bio))
    conn.commit()
    conn.close()

def view_personal_info():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("select * from PERSONAL_INFO")
    rows = curs.fetchall()
    conn.close()
    return rows

def create_bank_account_info_table():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("create table if not exists ACCOUNT(AId integer,UserName text,email text,fn text,ln text,dob text,homeaddress text,routingnumber text,accountnumber text)")
    conn.commit()
    conn.close()

def add_bank_account_info(aid,un,email,fn,ln,dob,add,rounum,accnum):
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("insert into ACCOUNT values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(aid,' ',email,fn,ln,dob,add,rounum,accnum))
    conn.commit()
    conn.close()

def view_bank_account_info():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("select * from ACCOUNT")
    rows = curs.fetchall()
    conn.close()
    return rows

def create_project_detailed_info_table():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("create table if not exists PROJECTDETAILS(PDID integer,ProjectTitle text,ProjectVideo text,ProjectDesc text)")
    conn.commit()
    conn.close()

def add_project_detailed_info(pdid,pt,pvideo,pdesc):
    conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
    curs = conn.cursor()
    curs.execute("insert into PROJECTDETAILS values(%s,%s,%s,%s)",(pdid,pt,pvideo,pdesc))
    conn.commit()
    conn.close()

def view_project_detailed_info():
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("select * from PROJECTDETAILS")
    rows = curs.fetchall()
    conn.close()
    return rows

def search_projects_by_username(un):
    conn = psycopg2.connect(database=url.path[1:] user=url.username password=url.password host=url.hostname port=url.port)
    curs = conn.cursor()
    curs.execute("select * from PROJECT where UserName = %s",(un,))
    rows = curs.fetchall()
    conn.close()
    return rows

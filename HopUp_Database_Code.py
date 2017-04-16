import psycopg2

def create_project_table():
    conn = psycopg2.connect("dbname='HopUp' user='postgres' password='postgres123' host='localhost' port='5432'")
    curs = conn.cursor()
    curs.execute("create table if not exists PROJECT(ProjectTitle text,ProjectCategory text,ProjectSubCategory text,ProjectCountry text,ProjectImage BYTEA,ProjectDescription text,ProjectLocation text,ProjectFundDuration integer,ProjectFundGoal text)")
    conn.commit()
    conn.close()

def insert_project(ptitle,pcat,psubcat,pcountry,pimage,pdesc,ploc,pfunddur,pfundgoal):
    conn = psycopg2.connect("dbname='HopUp' user='postgres' password='postgres123' host='localhost' port='5432'")
    curs = conn.cursor()
    curs.execute("insert intp PROJECT values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(ptitle,pcat,psubcat,pcountry,psycopg2.Binary(pimage),pdesc,ploc,pfunddur,pfundgoal))
    conn.commit()
    conn.close()

def view_projects():
    conn = psycopg2.connect("dbname='HopUp' user='postgres' password='postgres123' host='localhost' port='5432'")
    curs = conn.cursor()
    curs.execute("select * from PROJECT")
    rows = curs.fetchall()
    conn.close()
    return rows

def search_projects_by_title(ptitle):
    conn = psycopg2.connect("dbname='HopUp' user='postgres' password='postgres123' host='localhost' port='5432'")
    curs = conn.cursor()
    curs.execute("select * from PROJECT where ProjectTitle = %s",(ptitle,))
    rows = curs.fetchall()
    conn.close()
    return rows

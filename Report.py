"""
============================
author:YAN GAO
student ID:1995106
============================
"""
import cx_Oracle as cx


def report(cursor,sql,fileName):
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
    except Exception as e:
        print(e)
        return

    title = [i[0] for i in cursor.description]

    # first line
    firstLine = '-'*len(title)*20+'\n'

    # table head
    sttr = ''
    for i,h in enumerate(title):
        if len(h) > 20:
            s = h[:20].center(20)
        else:
            s = h.center(20)
        s = ('|' if i==0 else '')+ s[1:len(s)]+'|'
        sttr = sttr + s

    sttr = sttr+'\n'+('-'*len(title)*20)+'\n'

    # containt
    sstr = ''
    for i in res:
        for j,c in enumerate(i):
            if isinstance(c,str):
                ss = c.ljust(20) if len(c)<=20 else c[:20].ljust(20)
            if isinstance(c,int):
                ss = str(c).rjust(20) if len(str(c))<=20 else str(c)[:20].rjust(20)
            ss = ('|' if j==0 else '') + ss[1:len(ss)] +'|'
            sstr = sstr + ss
        sstr = sstr +'\n'+('-'*len(title)*20)+'\n'

    str_all = firstLine + sttr +sstr

    # wirte output
    crtFile(fileName,str_all)

def crtFile(filename,cont):
    try:
        with open(filename,'w') as f:
            f.write(cont)
    except Exception as e:
        print(e)


conn =  cx.connect('SYSTEM/orcl1234@localhost:1521/orcl')
cur = conn.cursor()
# testcase1
sql = "select min(A.dept_name) as name, count(*) as total from departments A inner join dept_emp B on A.dept_no=B.dept_no group by A.dept_no"
filename = "totalDepartment.txt"
report(cur,sql,filename)

# testcase2
sql1 = "select emp_no,to_char(birth_date) as birthday,first_name,last_name from employees where emp_no < 10012"
filename1 = "employeeInfo.txt"
report(cur,sql1,filename1)

# others testcases
sql_any = input("Enter a sql query:")
file_any = input("Enter output file Name:")
report(cur,sql_any,file_any)


cur.close()
conn.commit()
conn.close()

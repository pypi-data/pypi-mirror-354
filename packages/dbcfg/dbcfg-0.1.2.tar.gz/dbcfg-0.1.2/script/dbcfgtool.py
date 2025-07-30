import sys

from dbcfg import *
#import dbcfg

def main():
    c=c_commandarg(globals(),"dbcfg工具、样例")
    c.main()

def read():
    '读配置文件，显示基础信息'
    if len(sys.argv)<3:
        print("需要附加一个参数指定配置文件名")
        return
    dbc=dbcfg(sys.argv[2],ehm=1)    #读取指定的配置文件里的配置信息
#   dbc=dbcfg.use(sys.argv[1],ehm=1)    #如果使用import dbcfg引入包，就需要使用use函数
    dbc.connect()
    print(f"dbc.dbname={dbc.dbname}")
    cfg=dbc.cfg()           #返回指定名称的配置，不指定使用name为""的那一个
    print(f"cfg={cfg}")
    dbc.test()

def readdb():   #'读数据代码样例'
    字段=dbc.jg1("select 字段1 from 表 where 一些条件")  #返回结果只有一行数据用jg1

    字段1,字段2=dbc.jg1("select 字段1,字段2 from 表 where 一些条件") #jg1支持多字段

    结果=dbc.jg1("select 字段1,字段2 from 表 where 一些条件")  #jg1多字段另一种用法
    字段1,字段2=结果

    字段=dbc.jg1(f"select 字段1 from 表 where 字段2='{字段2筛选值}'")  #where条件可以用f格式串加入参数
    
    for 字段1,字段2 in dbc.execute("select 字段1,字段2 from 表 where 一些条件"): #循环读取多条数据
        print(字段1,字段2)

    for 字段1, in dbc.execute("select 字段1 from 表 where 一些条件"): #注意如果返回结果只有一个字段要加个逗号，不然返回的是数组
        print(字段1)

def wiki(): #wiki机器人读配置示例代码
    import mwclient
    dbc=dbcfg("wiki")
    cfg=dbc.cfg()
    site = mwclient.Site(cfg["d"]["server"], scheme=cfg["d"]["scheme"],path=cfg["d"]["path"])
    site.login(cfg["d"]["user"],cfg["d"]["password"])

if __name__ == "__main__":
    main()

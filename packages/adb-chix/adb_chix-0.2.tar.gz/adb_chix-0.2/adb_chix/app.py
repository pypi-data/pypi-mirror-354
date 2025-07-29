from flask import Flask,render_template,request
import subprocess
from datetime import datetime
IP ='127.0.0.1'
app=Flask(__name__)
#禁用模板缓存
app.config['TEMPLATES_AUTO_RELOAD'] = True  

#主页面
@app.get('/')
def index():
    return render_template('index.html')

# 修改电池电量界面
@app.get('/setlve')
def setlevel():
    return render_template('setlevel.html')


# 添加通话记录
@app.get('/addlist')
def addlist():
    return render_template('addlist.html')



# 执行配对
@app.get('/pair')
def iscon():
    rs=''
    pair_port=request.args.get('pair_port')
    pair=request.args.get('pair')
    res=subprocess.run(['adb','pair',f"{IP}:{pair_port}"],capture_output=True,text=True,input=pair+"\n")
    if "Successfully" in res.stdout:
        rs='ok'
    else:
        rs=res.stderr
    return rs

#执行连接
@app.get('/connect')
def connect():
    print(123)
    rs=''
    port=request.args.get('port')
    res=subprocess.run(['adb','connect',f"{IP}:{port}"],
                       capture_output=True,
                       text=True
                       ,encoding='utf-8')
    
    if res.returncode!=0:
       return 'error'
    if 'connected' in res.stdout:
        return 'ok'
    else:
        return 'error'

# 检测连接
@app.get('/isconnect')
def isconnect():
    res=subprocess.run(['adb','devices'],capture_output=True,text=True,encoding='utf-8')
    if 'device' in res.stdout.split():
        return 'yes'
    else:
        return 'no'
    



# 修改电池相关----------------------------------4
@app.get("/getlevel")
def getlv():
    return getLevel()

@app.get('/setlevel')
def setlv():
    level = request.args.get('level')
    if not level:
        return 'level is null'
    setLevel(level)
    print(1)
    return 'ok'+level

@app.get('/resetlevel')
def resetlv():
    resetLevel()
    return 'reset'

def connectAdb():
    res = subprocess.check_output(["adb","devices"]).decode('utf-8')
    if "device" in res:
        print('connected')
    else:
        print("no connect")
        quit()
        return
    
#获取电池电量
def getLevel():
    res = subprocess.check_output(["adb","shell","dumpsys","battery","|","grep","level"]).decode('utf-8')
    better_level=res.split(':')[1].strip()
    return better_level

# 修改电池电量
def setLevel(level):
    res = subprocess.check_output(["adb","shell","dumpsys","battery","set","level",str(level)]).decode('utf-8')
    print(res)
    
# 重置电池电量
def resetLevel():
    res = subprocess.check_output(["adb","shell","dumpsys","battery","reset"]).decode('utf-8')
    print(res)
# 修改电池相关-------END---------------------------4


# 添加通话记录--------------------------------------
@app.get('/add')
def add():
    sjh=request.args.get('sjh')
    thsc=request.args.get('thsc')
    # 通话时间转时间戳
    timeStr = request.args.get('thsj')
    thsj=int(datetime.strptime(timeStr,"%Y-%m-%d %H:%M").timestamp()*1000)
    # 执行adb
    res=subprocess.run([
        'adb','shell',
        'content','insert','--uri','content://call_log/calls',
        '--bind',f'number:s:{sjh}',
        '--bind','type:i:1',
        '--bind',f'date:l:{thsj}',
        '--bind',f'duration:i:{thsc}',
        '--bind','new:i:1',
        '--bind','is_read:i:1'
    ],capture_output=True,text=True)
    print(res.stderr)
    return f"{sjh},{thsc},{thsj}"
#---------------------------------------------------------

def run_server(host='0.0.0.0',port=8088):
    app.run(host=host,port=port)

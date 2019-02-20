import json
import requests
import time


supportedISOs = []
supportedShutterSpeeds = []

url = 'http://192.168.1.1:80'

def execute(command,req,retryCount=100):
    for i in range(0,retryCount):
        result = requests.post(url+'/'+command,json=req)
        try:
            r = result.json()
            if r['state'] != 'error':
                return True,r
        except:
            print('Failed, retrying',command,req,'\n')
        print('busy... retry',i,command,req)
        time.sleep(1)

    return False,None

def setCameraISO(iso):
    print('setCameraISO',iso)
    setISO = {'name':'camera.setOptions','parameters':{'options':{'iso':iso}}}
    return execute('osc/commands/execute',setISO)

def setCameraShutterSpeed(shutterSpeed):
    print('setCameraShutterSpeed',shutterSpeed)
    setShutterSpeed = {'name':'camera.setOptions','parameters':{'options':{'shutterSpeed':shutterSpeed}}}
    return execute('osc/commands/execute',setShutterSpeed)

def takePicture():
    print('takePicture')
    captureImage = {'name':'camera.takePicture','parameters':{}}
    return execute('osc/commands/execute',captureImage)

def init():
    global supportedISOs,supportedShutterSpeeds

    setManualMode = {'name':'camera.setOptions','parameters':{'options':{'exposureProgram':1}}}
    result = execute('osc/commands/execute',setManualMode)
    print(result)
    
    getSupportedISOs = {'name':'camera.getOptions','parameters':{'optionNames':['isoSupport']}}
    success,results = execute('osc/commands/execute',getSupportedISOs)
    if success==False:
        return False

    supportedISOs = results['results']['options']['isoSupport']

    getSupportedShutterSpeeds = {'name':'camera.getOptions','parameters':{'optionNames':['shutterSpeedSupport']}}
    success,results = execute('osc/commands/execute',getSupportedShutterSpeeds)
    if success==False:
        return False

    supportedShutterSpeeds = results['results']['options']['shutterSpeedSupport']
    print(supportedShutterSpeeds)

def captureDay():
    init()

    setCameraShutterSpeed(4e-05)
    for iso in supportedISOs:
        setCameraISO(iso)
        takePicture()

def captureNight():
    init()

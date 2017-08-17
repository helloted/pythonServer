
class DeviceServerError():

    code = 100
    msg = 'base error'

    def __init__(self,code,msg):
        self.code = code
        self.msg = msg

ERROR_DataBase = DeviceServerError(code=101, msg='DataBase error, please try it again later')
ERROR_No_Such_Device = DeviceServerError(code=102, msg='No such device')
ERROR_Upload_Token_Incorrect = DeviceServerError(code=103, msg='Token is invalid, please re-upload')
ERROR_Device_Offline = DeviceServerError(code=104, msg='This device was offline')
ERROR_Deal_SN_NotVerify = DeviceServerError(code=105, msg='Deal_SN_NotVerify')


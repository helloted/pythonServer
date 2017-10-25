
class DeviceServerError():

    code = 100
    msg = 'base error'

    def __init__(self,code,msg):
        self.code = code
        self.msg = msg

ERROR_DataBase = DeviceServerError(code=101, msg='DataBase error, please try it again later')
ERROR_No_Such_Device = DeviceServerError(code=102, msg='No such device')
ERROR_Sign_Valid = DeviceServerError(code=103, msg='Init Sign Valid')
ERROR_Upload_Token_Incorrect = DeviceServerError(code=104, msg='Token is invalid, please re-upload')
ERROR_Device_Offline = DeviceServerError(code=105, msg='This device was offline')
ERROR_Deal_SN_NotVerify = DeviceServerError(code=106, msg='Deal SN NotVerify')
ERROR_Deal_Para_Error = DeviceServerError(code=107, msg='Deal upload success,but para failed')
ERROR_CMD_Error = DeviceServerError(code=108, msg='Can not send this cmd before init connect')
ERROR_Deal_Received_Failed = DeviceServerError(code=109, msg='Deal received failed, please re-post this deal again')



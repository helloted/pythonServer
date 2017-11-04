
class WebServerError():

    code = 100
    msg = 'base error'

    def __init__(self,code,msg):
        self.code = code
        self.msg = msg

ERROR_DataBase = WebServerError(code=101, msg='DataBase error, please try it again later')
ERROR_Para_Error = WebServerError(code=102, msg='Parameter error')
ERROR_Time_Out_Error = WebServerError(code=103, msg='Timeout error')
ERROR_Push_Device_Failed = WebServerError(code=104, msg='Can not push this message to device')
ERROR_Deal_Not_Exist = WebServerError(code=105, msg='This deal not exist')
ERROR_No_Such_Deivce = WebServerError(code=106, msg='No such device')
ERROR_No_Such_Event = WebServerError(code=107, msg='No such event')
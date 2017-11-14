
class AppError():

    code = 100
    msg = 'base error'

    def __init__(self,code,msg):
        self.code = code
        self.msg = msg

ERROR_Parameters = AppError(code=101, msg='Request parameters are not correct')
ERROR_Token_Invalid = AppError(code=102, msg='Token is invalid, please re-login')
ERROR_DataBase = AppError(code=103, msg='DataBase error, please try it again later')
ERROR_Authorization = AppError(code=104, msg='This operation need authorization')
ERROR_Login_First = AppError(code=105, msg='Please login before this operation')

ERROR_Phone_Exists = AppError(code=121, msg='Phone number is already exists')
ERROR_Phone_Formats= AppError(code=122, msg='The formats of phone number is incorrect')
ERROR_Verification_Code = AppError(code=123, msg='Verification code is not correct')
ERROR_Login_Failed = AppError(code=124, msg='Phone number or the password is incorrect')
ERROR_User_Null = AppError(code=125, msg='User is not found')
ERROR_Store_Null = AppError(code=126, msg='Store is not found')
ERROR_Store_ReFavorite = AppError(code=127, msg='Store can\'t be favorited twice')
ERROR_Article_Null = AppError(code=128, msg='Article is not found')
ERROR_Comment_Null = AppError(code=129, msg='Comment is not found')
ERROR_Article_ReLike= AppError(code=130, msg='Article can\'t be liked twice')
ERROR_Article_ReFavorite = AppError(code=131, msg='Article can\'t be favorited twice')
ERROR_QRCode_Repeated = AppError(code=132, msg='This Qr code has been already scan')
ERROR_QRCode_Invalid = AppError(code=133, msg='This Qr code is invalid')
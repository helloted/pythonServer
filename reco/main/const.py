# -*- coding: UTF-8 -*-
# Filename: const.py
# 定义一个常量类实现常量的功能


# 订单中可能用到的字段(不可修改)
ORDER_SERIAL_NUM = "serial_num"
ORDER_TITLE = "title"
ORDER_SHOP_NAME = "shop_name"
ORDER_EMAIL = "email"
ORDER_MOBILE_PHONE = "mobile_phone"
ORDER_LANDLINE_PHONE = "landline_ohone"
ORDER_CASHIER = "cashier"
ORDER_ORDER_ID = "order_id"
ORDER_TIME = "time"
ORDER_TOTAL = "total"
ORDER_SUBTOTAL = "subtotal"
ORDER_TAX = "tax"
ORDER_ITEMS = "items"
ORDER_SN = "sn"
ORDER_QR = "qr"
ORDER_TXT = "txt_data"
ORDER_IS_ORDER = "is_order"
ORDER_IS_VALID_ORDER = "is_valid_order"

# 商品中可能用到的字段
GOOD_NAME = "name"                      # 商品名
GOOD_QTY = "quantity"                   # 份数
GOOD_UNIT_PRICE = "unit_price"          # 单价
GOOD_SUBTOTAL = "subtotal"              # 单价*份数
GOOD_SUBGOOD_LIST = "subgood_list"      # 单价*份数
# 商品中搭配商品
SUBGOOD_NAME = "subgood_name"                   # 搭配商品 名字
SUBGOOD_QTY = "subgood_quantity"                # 搭配商品 份数
SUBGOOD_UNIT_PRICE = "subgood_unit_price"       # 搭配商品 单价
SUBGOOD_TOTAL_PRICE = "subgood_total_price"     # 搭配商品 总价


# 解析keys
RECO_SERIAL_NUM = "serial_num"
RECO_CMD_NO = "cmd_no"
RECO_CUT_CMD_NO = "cut_cmd_no"
RECO_ORDER_KEYS = "order_keys"
RECO_TITLE_KEYS = "title_keys"
RECO_ID_KEYS = "id_keys"
RECO_TIME_KEYS = "time_keys"
RECO_EMAIL_KEYS = "email_keys"
RECO_MOBILE_PHONE_KEYS = "mobile_phone_keys"
RECO_LANDLINE_PHONE_KEYS = "landline_phone_keys"
RECO_GOOD_NO = "good_no"
RECO_SUBGOOD_NO = "subgood_no"
RECO_SUBTOTAL_KEYS = "subtotal_keys"
RECO_TAX_KEYS = "tax_keys"
RECO_TOTAL_KEYS = "total_keys"
RECO_CAPTURE_DATA = "capture_data"


# 正则表达式 -- 用于去掉reg_exp中所有特殊字符
REG_EXP_SPECIAL_CHAR = "[`~!@#$%^&*()\-=_+\[\]{}\\|;':\",.<>/?]"

# 印尼手机号码
REG_EXP_MOBILE_PHONE = "(08|8)\d{10}"

# 邮箱
REG_EXP_EMAIL = "[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+"





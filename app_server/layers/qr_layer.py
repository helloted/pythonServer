from flask import Blueprint
from app_server.utils.request_handle import request_unpack,login_required
from flask import request
from super_models.order_model import Order
from super_models.lottery_model import Lottery
from app_server.response import errors
from app_server.models import SessionContext

node_qr=Blueprint('qr_layer',__name__,)


@node_qr.route('/scan', methods=['POST'])
@request_unpack
@login_required
def qr_list():
    body = request.json
    article_id = body.get('article_id')
    with SessionContext() as session:
        print ''


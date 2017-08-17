#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
APP—Server的入口
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from flask import Flask
from app_server.layers.user_layer import node_user
from app_server.layers.homepage_layer import node_homepage
from app_server.layers.store_layer import node_store
from app_server.layers.article_layer import node_article
from app_server.layers.mine_layer import node_mine


app = Flask(__name__)

# app.logger.setLevel(logging.ERROR)

app.register_blueprint(node_user, url_prefix='/user')
app.register_blueprint(node_homepage, url_prefix='/homepage')
app.register_blueprint(node_store, url_prefix='/store')
app.register_blueprint(node_article, url_prefix='/article')
app.register_blueprint(node_mine, url_prefix='/mine')



if __name__ == '__main__':
    app.run(port=5008)
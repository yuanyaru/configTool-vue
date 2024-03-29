#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, jsonify, render_template
from flask_cors import CORS  # 解决跨域问题
from iceCon import ice_con
import sys
import Ice
Ice.loadSlice("./ice-sqlite.ice")
# Ice.loadSlice("/code/tool/configTool/ice-sqlite.ice")
from staproperty import sta_blu, get_station_property
from yxproperty import yx_blu
from ycproperty import yc_blu
from ykproperty import yk_blu
from ytproperty import yt_blu
from soeproperty import soe_blu

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__, template_folder="./dist",
            static_folder="./dist",
            static_url_path=""
            )
app.config['SECRET_KEY'] = 'secret!'
app.register_blueprint(sta_blu)
app.register_blueprint(yx_blu)
app.register_blueprint(yc_blu)
app.register_blueprint(yk_blu)
app.register_blueprint(yt_blu)
app.register_blueprint(soe_blu)

cors = CORS(app, resources={r"/getStaTree": {"origins": "*"}})
cors = CORS(app, resources={r"/getTableHeader": {"origins": "*"}})
cors = CORS(app, resources={r"/getLianludata": {"origins": "*"}})
cors = CORS(app, resources={r"/getYCdata": {"origins": "*"}})
cors = CORS(app, resources={r"/getYXdata": {"origins": "*"}})
cors = CORS(app, resources={r"/getYKdata": {"origins": "*"}})
cors = CORS(app, resources={r"/getYTdata": {"origins": "*"}})
cors = CORS(app, resources={r"/getSOEdata": {"origins": "*"}})


def get_property_table():
    DataCommand = ice_con()
    status, stationtable, yctable, yxtable, yktable, yttable, soetable = \
        DataCommand.RPCGetPropertyTable()
    table = [stationtable, yctable, yxtable, yktable, yttable, soetable]
    return table


@app.route('/getTableHeader', methods=['GET'])
def getTableHeader():
    tableHeader = get_property_table()
    response = {
        'tableHeader': tableHeader,
    }
    return jsonify(response)


@app.route('/getStaTree', methods=['GET'])
def getStaTree():
    station = get_station_property()
    staLen = len(station)
    staNames = []
    for i in range(staLen):
        staNames.append(station[i].name)
    response = {
        'staLen': staLen,
        'staNames': staNames,
    }
    return jsonify(response)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

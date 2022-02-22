#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from iceCon import ice_con
import json
import Ice
Ice.loadSlice("./ice-sqlite.ice")
# Ice.loadSlice("/code/tool/configTool/ice-sqlite.ice")
import YCArea

yc_blu = Blueprint('yc', __name__)


# 查找(遥测属性)
@yc_blu.route('/getYCdata', methods=['GET'])
def get_yc_property_send():
    stationId = request.args.get("stationId")
    station = json.loads(stationId)
    DataCommand = ice_con()
    status, result = DataCommand.RPCGetYCProperty(station)
    ycproperty = []
    for i in range(len(result)):
        ycproperty.append({"ID": result[i].ID, "name": result[i].name,
                           "describe": result[i].describe, "unit": result[i].unit,
                           "kval": round(result[i].kval, 7), "bval": round(result[i].bval, 7),
                           "address": result[i].address, "uplimt": result[i].uplimt,
                           "downlimt": result[i].downlimt})
    response = {
        'ycproperty': ycproperty,
        'lenycp': len(result),
    }
    return jsonify(response)


# 添加、修改(遥测属性)
@yc_blu.route('/setYc', methods=['POST'])
@cross_origin(supports_credentials=True)
def set_yc_property():
    DataCommand = ice_con()
    data = request.get_json()
    stationId = data["station"]
    YcProperty = data["selectRecords"]
    ycproperty = []
    for i in range(len(YcProperty)):
        ID = YcProperty[i]["ID"]
        name = YcProperty[i]["name"]
        describe = YcProperty[i]["describe"]
        unit = YcProperty[i]["unit"]
        kval = YcProperty[i]["kval"]
        bval = YcProperty[i]["bval"]
        address = YcProperty[i]["address"]
        uplimt = YcProperty[i]["uplimt"]
        downlimt = YcProperty[i]["downlimt"]

        if ID == "":
            ID = 1000
        if name == "":
            name = "请添加遥测名称"
        if describe == "":
            describe = "请描述遥测"
        if unit == "":
            unit = "请添加单位"
        if kval == "":
            kval = 1.0
        if bval == "":
            bval = 0.0
        if address == "":
            address = "0"
        if uplimt == "":
            uplimt = 2000.0
        if downlimt == "":
            downlimt = 0.0
        ycpstruct = YCArea.DxPropertyYC(int(ID), name.encode("utf-8"),
                                        describe.encode("utf-8"), unit.encode("utf-8"),
                                        round(float(kval), 7), round(float(bval), 7),
                                        address.encode("utf-8"), float(uplimt),
                                        float(downlimt))
        ycproperty.append(ycpstruct)
    status = DataCommand.RPCSetYCProperty(stationId, ycproperty)
    response = {
        'status': status
    }
    return jsonify(response)


# 删除(遥测属性)
@yc_blu.route('/deleteYc', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_yc_data():
    DataCommand = ice_con()
    IDs = request.get_json()
    station = IDs["station"]
    ycIDs = IDs["ids"]
    pIDs = []
    for i in range(len(ycIDs)):
        pIDs.append(long(ycIDs[i]))
    status = DataCommand.RPCDelYCProperty(station, pIDs)
    response = {
        'status': status
    }
    return jsonify(response)

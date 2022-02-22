#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from iceCon import ice_con
import json
import Ice
Ice.loadSlice("./ice-sqlite.ice")
# Ice.loadSlice("/code/tool/configTool/ice-sqlite.ice")
import SOEArea

soe_blu = Blueprint('soe', __name__)


# 查找(SOE属性)
@soe_blu.route('/getSOEdata', methods=['GET'])
def get_soe_property_send():
    stationId = request.args.get("stationId")
    station = json.loads(stationId)
    DataCommand = ice_con()
    status, result = DataCommand.RPCGetSOEProperty(station)
    soeproperty = []
    for i in range(len(result)):
        soeproperty.append({"ID": result[i].ID, "name": result[i].name,
                           "describe": result[i].describe, "level": result[i].level})
    response = {
        'soeproperty': soeproperty,
        'lensoep': len(result),
    }
    return jsonify(response)


# 添加、修改(SOE属性)
@soe_blu.route('/setSoe', methods=['POST'])
@cross_origin(supports_credentials=True)
def set_soe_property():
    DataCommand = ice_con()
    data = request.get_json()
    stationId = data["station"]
    SoeProperty = data["selectRecords"]
    soeproperty = []
    for i in range(len(SoeProperty)):
        ID = SoeProperty[i]["ID"]
        name = SoeProperty[i]["name"]
        describe = SoeProperty[i]["describe"]
        level = SoeProperty[i]["level"]

        if ID == "":
            ID = 1000
        if name == "":
            name = "请添加SOE名称"
        if describe == "":
            describe = "请描述SOE"
        if level == "":
            level = 1
        soepstruct = SOEArea.DxPropertySOE(int(ID), name.encode("utf-8"),
                                           describe.encode("utf-8"), int(level))
        soeproperty.append(soepstruct)
    status = DataCommand.RPCSetSOEProperty(stationId, soeproperty)
    response = {
        'status': status
    }
    return jsonify(response)


# 删除(SOE属性)
@soe_blu.route('/deleteSoe', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_soe_data():
    DataCommand = ice_con()
    IDs = request.get_json()
    stationId = IDs["station"]
    soeIDs = IDs["ids"]
    pIDs = []
    for i in range(len(soeIDs)):
        pIDs.append(long(soeIDs[i]))
    status = DataCommand.RPCDelSOEProperty(stationId, pIDs)
    response = {
        'status': status
    }
    return jsonify(response)

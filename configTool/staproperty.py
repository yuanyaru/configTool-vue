#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from iceCon import ice_con
import Ice
Ice.loadSlice("./ice-sqlite.ice")
# Ice.loadSlice("/code/tool/configTool/ice-sqlite.ice")
import StationArea

sta_blu = Blueprint('station', __name__)


def get_station_property():
    DataCommand = ice_con()
    status, result = DataCommand.RPCGetStationProperty()
    return result


# 查找(厂站属性)
@sta_blu.route('/getLianludata', methods=['GET'])
def get_station_property_send():
    result = get_station_property()
    staproperty = []
    for i in range(len(result)):
        staproperty.append({"ID": result[i].ID, "name": result[i].name,
                            "describe": result[i].describe, "ruleID": result[i].ruleID,
                            "address": result[i].address, "PORT": result[i].PORT,
                            "role": result[i].role})
    response = {
        'staproperty': staproperty,
        'lenstap': len(result),
    }
    return jsonify(response)


# 添加、修改(厂站属性)
@sta_blu.route('/setStation', methods=['POST'])
@cross_origin(supports_credentials=True)
def set_station_property():
    DataCommand = ice_con()
    data = request.get_json()
    station = data["selectRecords"]
    stationProperty = []
    for i in range(len(station)):
        ID = station[i]["ID"]
        name = station[i]["name"]
        describe = station[i]["describe"]
        ruleID = station[i]["ruleID"]
        address = station[i]["address"]
        PORT = station[i]["PORT"]
        role = station[i]["role"]

        if ID == "":
            ID = 100
        if name == "":
            name = "请填写厂站名"
        if describe == "":
            describe = "请描述厂站"
        if ruleID == "":
            ruleID = 1
        if address == "":
            address = "请添加地址信息"
        if PORT == "":
            PORT = 60000
        if role == "":
            role = 1
        stationInfo = StationArea.DxPropertyStation(int(ID), name.encode("utf-8"), describe.encode("utf-8"),
                                                    int(ruleID), address.encode("utf-8"), int(PORT), int(role))
        stationProperty.append(stationInfo)
    status = DataCommand.RPCSetStationProperty(stationProperty)
    # print status
    response = {
        'status': status
    }
    return jsonify(response)


# 删除(厂站属性)
@sta_blu.route('/deleteStation', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_station_data():
    DataCommand = ice_con()
    stationIDs = request.get_json()
    staIDs = []
    for i in range(len(stationIDs["ids"])):
        staIDs.append(long(stationIDs["ids"][i]))
    status = DataCommand.RPCDelStationProperty(staIDs)
    response = {
        'status': status
    }
    return jsonify(response)

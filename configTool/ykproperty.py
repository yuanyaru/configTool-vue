#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from iceCon import ice_con
import json
import Ice
Ice.loadSlice("./ice-sqlite.ice")
# Ice.loadSlice("/code/tool/configTool/ice-sqlite.ice")
import YKArea

yk_blu = Blueprint('yk', __name__)


# 查找(遥控属性)
@yk_blu.route('/getYKdata', methods=['GET'])
def get_yk_property_send():
    stationId = request.args.get("stationId")
    station = json.loads(stationId)
    DataCommand = ice_con()
    status, result = DataCommand.RPCGetYKProperty(station)
    ykproperty = []
    for i in range(len(result)):
        ykproperty.append({"ID": result[i].ID, "name": result[i].name,
                           "describe": result[i].describe, "ASDU": result[i].ASDU,
                           "wordPos": result[i].wordPos, "bitPos": result[i].bitPos,
                           "bitLength": result[i].bitLength, "EnablePoint": result[i].EnablePoint,
                           "EnableValue": result[i].EnableValue, "address": result[i].address})
    response = {
        'ykproperty': ykproperty,
        'lenykp': len(result),
    }
    return jsonify(response)


# 添加、修改(遥控属性)
@yk_blu.route('/setYk', methods=['POST'])
@cross_origin(supports_credentials=True)
def set_yk_property():
    DataCommand = ice_con()
    data = request.get_json()
    stationId = data["station"]
    YkProperty = data["selectRecords"]
    ykproperty = []
    num = len(YkProperty) / 8000
    print num
    j = 0
    while j < num:
        for i in range(8000*j, 8000*j+8000):
            ID = YkProperty[i]["ID"]
            name = YkProperty[i]["name"]
            describe = YkProperty[i]["describe"]
            ASDU = YkProperty[i]["ASDU"]
            wordPos = YkProperty[i]["wordPos"]
            bitPos = YkProperty[i]["bitPos"]
            bitLength = YkProperty[i]["bitLength"]
            EnablePoint = YkProperty[i]["EnablePoint"]
            EnableValue = YkProperty[i]["EnableValue"]
            address = YkProperty[i]["address"]

            if ID == "":
                ID = 1000
            if name == "":
                name = "请添加遥控名称"
            if describe == "":
                describe = "请描述遥控"
            if ASDU == "":
                ASDU = 0
            if wordPos == "":
                wordPos = 0
            if bitPos == "":
                bitPos = 0
            if bitLength == "":
                bitLength = 1
            if EnablePoint == "":
                EnablePoint = 0
            if EnableValue == "":
                EnableValue = 0
            if address == "":
                address = "0"
            ykpstruct = YKArea.DxPropertyYK(int(ID), name.encode("utf-8"),
                                            describe.encode("utf-8"), int(ASDU),
                                            int(wordPos), int(bitPos),
                                            int(bitLength), int(EnablePoint),
                                            int(EnableValue), address.encode("utf-8"))
            ykproperty.append(ykpstruct)
        status = DataCommand.RPCSetYKProperty(stationId, ykproperty)
        print len(ykproperty)
        ykproperty[:] = []
        j = j + 1
        print j
        if status == 1:
            continue
        else:
            break
    for i in range(8000*j, len(YkProperty)):
        ID = YkProperty[i]["ID"]
        name = YkProperty[i]["name"]
        describe = YkProperty[i]["describe"]
        ASDU = YkProperty[i]["ASDU"]
        wordPos = YkProperty[i]["wordPos"]
        bitPos = YkProperty[i]["bitPos"]
        bitLength = YkProperty[i]["bitLength"]
        EnablePoint = YkProperty[i]["EnablePoint"]
        EnableValue = YkProperty[i]["EnableValue"]
        address = YkProperty[i]["address"]

        if ID == "":
            ID = 1000
        if name == "":
            name = "请添加遥控名称"
        if describe == "":
            describe = "请描述遥控"
        if ASDU == "":
            ASDU = 0
        if wordPos == "":
            wordPos = 0
        if bitPos == "":
            bitPos = 0
        if bitLength == "":
            bitLength = 1
        if EnablePoint == "":
            EnablePoint = 0
        if EnableValue == "":
            EnableValue = 0
        if address == "":
            address = "0"
        ykpstruct = YKArea.DxPropertyYK(int(ID), name.encode("utf-8"),
                                        describe.encode("utf-8"), int(ASDU),
                                        int(wordPos), int(bitPos),
                                        int(bitLength), int(EnablePoint),
                                        int(EnableValue), address.encode("utf-8"))
        ykproperty.append(ykpstruct)
    status = DataCommand.RPCSetYKProperty(stationId, ykproperty)
    print len(ykproperty)
    response = {
        'status': status
    }
    return jsonify(response)


# 删除(遥控属性)
@yk_blu.route('/deleteYk', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_yk_data():
    DataCommand = ice_con()
    IDs = request.get_json()
    station = IDs["station"]
    ykIDs = IDs["ids"]
    pIDs = []
    for i in range(len(ykIDs)):
        pIDs.append(long(ykIDs[i]))
    status = DataCommand.RPCDelYKProperty(station, pIDs)
    response = {
        'status': status
    }
    return jsonify(response)

#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from iceCon import ice_con
import json
import Ice
Ice.loadSlice("./ice-sqlite.ice")
# Ice.loadSlice("/code/tool/configTool/ice-sqlite.ice")
import YTArea

yt_blu = Blueprint('yt', __name__)


# 查找(遥调属性)
@yt_blu.route('/getYTdata', methods=['GET'])
def get_yt_property_send():
    stationId = request.args.get("stationId")
    station = json.loads(stationId)
    DataCommand = ice_con()
    status, result = DataCommand.RPCGetYTProperty(station)
    ytproperty = []
    for i in range(len(result)):
        ytproperty.append({"ID": result[i].ID, "name": result[i].name,
                           "describe": result[i].describe, "unit": result[i].unit,
                           "kval": result[i].kval, "bval": result[i].bval,
                           "address": result[i].address, "uplimt": result[i].uplimt,
                           "downlimt": result[i].downlimt})
    response = {
        'ytproperty': ytproperty,
        'lenytp': len(result),
    }
    return jsonify(response)


# 添加、修改(遥调属性)
@yt_blu.route('/setYt', methods=['POST'])
@cross_origin(supports_credentials=True)
def set_yt_property():
    DataCommand = ice_con()
    data = request.get_json()
    stationId = data["station"]
    YtProperty = data["selectRecords"]
    ytproperty = []
    num = len(YtProperty) / 8000
    print num
    j = 0
    while j < num:
        for i in range(8000*j, 8000*j+8000):
            ID = YtProperty[i]["ID"]
            name = YtProperty[i]["name"]
            describe = YtProperty[i]["describe"]
            unit = YtProperty[i]["unit"]
            kval = YtProperty[i]["kval"]
            bval = YtProperty[i]["bval"]
            address = YtProperty[i]["address"]
            uplimt = YtProperty[i]["uplimt"]
            downlimt = YtProperty[i]["downlimt"]

            if ID == "":
                ID = 1000
            if name == "":
                name = "请添加遥调名称"
            if describe == "":
                describe = "请描述遥调"
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
            ytpstruct = YTArea.DxPropertyYT(int(ID), name.encode("utf-8"),
                                            describe.encode("utf-8"), unit.encode("utf-8"),
                                            float(kval), float(bval),
                                            address.encode("utf-8"), float(uplimt),
                                            float(downlimt))
            ytproperty.append(ytpstruct)
        status = DataCommand.RPCSetYTProperty(stationId, ytproperty)
        print len(ytproperty)
        ytproperty[:] = []
        j = j + 1
        print j
        if status == 1:
            continue
        else:
            break
    for i in range(8000*j, len(YtProperty)):
        ID = YtProperty[i]["ID"]
        name = YtProperty[i]["name"]
        describe = YtProperty[i]["describe"]
        unit = YtProperty[i]["unit"]
        kval = YtProperty[i]["kval"]
        bval = YtProperty[i]["bval"]
        address = YtProperty[i]["address"]
        uplimt = YtProperty[i]["uplimt"]
        downlimt = YtProperty[i]["downlimt"]

        if ID == "":
            ID = 1000
        if name == "":
            name = "请添加遥调名称"
        if describe == "":
            describe = "请描述遥调"
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
        ytpstruct = YTArea.DxPropertyYT(int(ID), name.encode("utf-8"),
                                        describe.encode("utf-8"), unit.encode("utf-8"),
                                        float(kval), float(bval),
                                        address.encode("utf-8"), float(uplimt),
                                        float(downlimt))
        ytproperty.append(ytpstruct)
    status = DataCommand.RPCSetYTProperty(stationId, ytproperty)
    print len(ytproperty)
    response = {
        'status': status
    }
    return jsonify(response)


# 删除(遥调属性)
@yt_blu.route('/deleteYt', methods=['POST'])
@cross_origin(supports_credentials=True)
def delete_yt_data():
    DataCommand = ice_con()
    IDs = request.get_json()
    stationId = IDs["station"]
    ytIDs = IDs["ids"]
    pIDs = []
    for i in range(len(ytIDs)):
        pIDs.append(long(ytIDs[i]))
    status = DataCommand.RPCDelYTProperty(stationId, pIDs)
    response = {
        'status': status
    }
    return jsonify(response)

# -*- coding:utf-8 -*-
# utils.py
# by 赵鹏程 2020.12.23

from segmentation.utils import *
import requests
import json
import numpy as np
import cv2

def client_rest(path, pathBack):

    # 图片的本地保存路径，人像和背景
    # path = "./test_images/girl3.jpg"
    # pathBack = "./test_images/b1.jpg"

    # 目标主机url与接口
    URL = "http://localhost:8501/v1/models/export:predict"
    headers = {"content-type": "application/json"}

    # 设定核卷积大小
    size = 512

    # 图像伸缩，边缘扩充，适配不同尺寸图片
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB).astype(np.uint8)
    _, pad, signal = padding(resize_image(img, size), size, 3, True)
    img = padding(resize_image(img, size), size, 3).astype(np.float64)
    img /= 255.0

    # 原生ndarray数据无法转换成json，需要先转换成为list数据
    img = img.tolist()

    body = {
        "signature_name": "predict_image",
        "instances": [
            {"image": img}
        ]
    }
    r = requests.post(URL, data=json.dumps(body), headers=headers)

    # 将生成的掩码和原图匹配
    prediction = r.json()['predictions'][0]
    mask = np.array(prediction)
    imgx = cv2.imread(path)
    mask[mask * 255 > 128] = 255
    mask[mask * 255 <= 128] = 0

    if signal == 2:
        new_mask = cv2.resize(mask[:, pad:-pad], (imgx.shape[1], imgx.shape[0]), interpolation=cv2.INTER_CUBIC)
    elif signal == 1:
        new_mask = cv2.resize(mask[pad:-pad, :], (imgx.shape[1], imgx.shape[0]), interpolation=cv2.INTER_CUBIC)
    else:
        new_mask = cv2.resize(mask, (imgx.shape[1], imgx.shape[0]), interpolation=cv2.INTER_CUBIC)

    new_mask[new_mask > 128] = 255
    new_mask[new_mask <= 128] = 0

    # 滤波与膨胀操作优化边缘
    new_mask = np.float32(new_mask)
    new_mask = cv2.medianBlur(new_mask, 5)
    new_mask = cv2.dilate(new_mask, None, iterations=1)

    imgx[new_mask != 255] = 255

    # 截取背景图片到合适的大小
    background = resize_background_image(new_mask, cv2.imread(pathBack))
    back_height = background.shape[0]
    back_width = background.shape[1]
    new_mask_height = new_mask.shape[0]
    new_mask_width = new_mask.shape[1]
    startX = int((back_width - new_mask_width) / 2)
    endX = startX + new_mask_width
    startY = int((back_height - new_mask_height) / 2)
    endY = startY + new_mask_height
    background = background[startY:endY, startX:endX]
    background[new_mask == 255] = [0, 0, 0]

    # 将两张图片合并
    combine_img = background + imgx

    # 展示结果
    # cv2.imshow('mask2', combine_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 将图片转化成标准RGB格式
    # combine_img = cv2.cvtColor(combine_img, cv2.COLOR_BGR2RGB)

    return combine_img



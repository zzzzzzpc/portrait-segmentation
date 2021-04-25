# -*- coding:utf-8 -*-
# utils.py
# by 赵鹏程 2020.12.20

import cv2
import numpy as np

def resize_image(img, reshape_size = 224):
    '''改变图片大小
    通过opencv并根据网络中的核卷积大小设定被分割图像尺寸
    
    Args:
        img:输入图像，ndarray格式，type为unit8
        reshape_size:图像大小尺寸设定，默认为224，本模型为512
    
    Returns:
        返回被opencv处理过尺寸的图片
    
    Raises:
        可能的IOError,修改输入的图片格式
    '''
    max_shape = np.max(img.shape)
    ratio = (max_shape / reshape_size).astype(np.float64)

    new_width = np.round((img.shape[1] / ratio)).astype(np.int)
    new_height  = np.round((img.shape[0] / ratio)).astype(np.int)
   
    return cv2.resize(img, (new_width, new_height))

def padding(img, dimension= 224, channel = 3, show_pad = False ):
    '''填充图片边缘
    
    如果图像不满足核维度，将图片边缘填充到指定维度
    
    Args:
        img:输入图像，ndarray格式，type为unit8
        dimension:核维度，此处模型应为512，默认为224
        channel:图像通道数
        show_pad:是否显示图片填充边缘
        
    Return:
        返回填充过后的图片
    '''
    empty = np.zeros((dimension, dimension,channel)).astype(np.int)
    width = img.shape[0]
    height = img.shape[1]
    
    diff_width  = (dimension - width)//2
    diff_height = (dimension - height)//2
    signal = 0
    
    if ( width == dimension and height != dimension):
        empty[:, diff_height:(height+diff_height),:] = img.astype(np.int)
        signal = 2
    elif ( width != dimension and height == dimension):
        empty[ diff_width:(width+diff_width), : ,:] = img.astype(np.int)
        signal = 1
    elif ( width <= dimension and height <= dimension ):
        empty[diff_width:(diff_width+width), diff_height:(diff_height+height),:] = img.astype(np.int)
        signal = 0
    if show_pad:
        if signal == 1:
            return empty, diff_width, signal
        elif signal == 2:
            return empty, diff_height, signal
        return empty,-1,-1
    else:
        return empty

def resize_background_image(img, back_img):
    '''根据需要截取的人像调整背景图像的大小
    
    如果原图像尺寸大于人像尺寸那么直接返回背景图片，
    如果小于则调整到与背景图片一致的大小
    
    Args:
        img:输入的人像图像
        back_img:输入的背景图像
    
    return:
        处理过的图像
    '''
    height = img.shape[0]
    width = img.shape[1]
    back_height = back_img.shape[0]
    back_width = back_img.shape[1]

    if (height <= back_height and width <= back_width):
	    return back_img
	
    if (height >= back_height):
        back_height = height
    
    if (width >= back_width):
        back_width = width
        
    return cv2.resize(back_img, (back_width, back_height), interpolation = cv2.INTER_AREA)

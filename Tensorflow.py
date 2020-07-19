from absl import app
import numpy as np
import tensorflow as tf
import os

def detect_voc2012(imagePath):
    model = tf.saved_model.load('./serving/voc2012/1/')
    fileList = os.listdir(imagePath)
    cklist = []
    delist = []
    for imagename in fileList:
        if chuli(model, imagePath + imagename):
            cklist.append(imagename)
        else:
            delist.append(imagename)
    return cklist, delist
def chuli(model, img_path):
    img_raw = tf.image.decode_image(
        open(img_path, 'rb').read(), channels=3)
    img = tf.expand_dims(img_raw, 0)
    img = transform_images(img, 416)
    infer = model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
    outputs = infer(img)
    class_names = [c.strip() for c in open('./serving/voc2012/voc2012.names').readlines()]
    # class_names = [c.strip() for c in open('./serving/yolov3/coco.names').readlines()]
    boxes, scores, classes, nums = outputs["yolo_nms"], outputs[
        "yolo_nms_1"], outputs["yolo_nms_2"], outputs["yolo_nms_3"]
    arr = ['aeroplane', 'bicycle', 'bird', 'boat', 'bus', 'car', 'motorbike', 'person', 'train']
    # arr = ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat']
    for i in range(nums[0]):
        if class_names[int(classes[0][i])] in arr and np.array(scores[0][i]) > 0.4:
            # print(class_names[int(classes[0][i])])
            return True
    return False

def transform_images(x_train, size):
    x_train = tf.image.resize(x_train, (size, size))
    x_train = x_train / 255
    return x_train


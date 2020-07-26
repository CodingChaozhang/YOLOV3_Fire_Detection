import xml.etree.ElementTree as ET
import os
import cv2

annotations = "./Annotations/"
imgs = "./JPEGImages"
classes = ["fire"]

# 获取xml的名称列表
annotations_xml = os.listdir(annotations)

# 归一化
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
	
def convert_annotation(annotation_id, output_file):
    in_file = open('Annotations/%s.xml'%(annotation_id))
    print(annotation_id)
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find("size")
    img = cv2.imread(os.path.join(imgs,annotation_id+".jpg"))
    h = img.shape[0]
    w = img.shape[1]
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text # 类别
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls) # 类别的索引
        xmlbox = obj.find('bndbox') # 边框区域
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))  # 得到的是两点坐标
        bb = convert((w,h), b)  # 将两点坐标转换成 x y w h
        output_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')  # 写入到文件夹

if __name__ == "__main__":
    # 对xml名称列表遍历
    for annotation_name in annotations_xml:
        annotation_id = annotation_name[:-4]
        output_file = open("labels/%s.txt"%(annotation_id),"w")
        convert_annotation(annotation_id, output_file)
        output_file.write('\n')
        output_file.close()

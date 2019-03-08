import os
import sys
import xml.etree.ElementTree as ET

xml_annotation_dir= sys.argv[1]
out_dir = sys.argv[2]

classes = ["1", "2"]
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    id, ext = image_id.split('.')
    
    in_file = open(os.path.join(xml_annotation_dir, '%s' %( image_id)), 'r')
    out_file = open(os.path.join(out_dir, '%s.txt'%(id)), 'w')
    print("in_file: %s" %in_file)

    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        try:
            difficult = obj.find('difficult').text
        except Exception as e:
            difficult = '0'
        
        cls = obj.find('name').text
        print(cls)
        
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    in_file.close()
    out_file.close()

for id in os.listdir(xml_annotation_dir):
	if id.split('.')[-1] == 'xml':
		convert_annotation(id)


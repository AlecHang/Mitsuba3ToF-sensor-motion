import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import re, os

def update_sensor_transformation(input_xml_path, output_xml_path, velocity, t):
    # 使用ElementTree解析XML文件
    tree = ET.parse(input_xml_path)
    root = tree.getroot()

    # 查找sensor标签
    sensor = root.find('sensor')
    if sensor is None:
        raise ValueError("No 'sensor' tag found in the XML file.")

    # 查找原始的transform标签
    transformation = sensor.find('transform[@name="to_world"]')
    if transformation is None:
        raise ValueError("No 'transform' tag with name='to_world' found in the sensor.")

    # 创建animation标签
    animation = ET.SubElement(sensor, 'animation', attrib={'name': 'to_world'})

    # 创建第一个transform（时间t=0）
    transform0 = ET.SubElement(animation, 'transform', attrib={'time': '0'})
    for child in transformation:
        new_child = ET.Element(child.tag, attrib=child.attrib)
        new_child.text = child.text
        for sub_child in child:
            new_child.append(sub_child)
        transform0.append(new_child)

    # 计算位移并创建第二个transform（时间t=0.0015）
    displacement = velocity * t
    transform1 = ET.SubElement(animation, 'transform', attrib={'time': str(t)})
    for child in transformation:
        new_child = ET.Element(child.tag, attrib=child.attrib)
        new_child.text = child.text
        for sub_child in child:
            new_child.append(sub_child)
        transform1.append(new_child)
    ET.SubElement(transform1, 'translate', attrib={
        'x': str(displacement[0]),
        'y': str(displacement[1]),
        'z': str(displacement[2])
    })

    # 移除原来的transformation标签
    sensor.remove(transformation)

    # 使用minidom美化XML
    xml_str = ET.tostring(root, encoding="utf-8")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")

    # 去掉多余的空行
    pretty_xml = re.sub(r'\n\s*\n', '\n', pretty_xml)

    # 写入到文件（去掉多余的XML声明）
    with open(output_xml_path, "w") as f:
        f.write(pretty_xml.replace('<?xml version="1.0" ?>', ""))

def list_xml_files(input_dir):
    xml_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".xml"):
                xml_files.append(os.path.join(root, file))
    return xml_files

def ensure_output_path(input_file, input_dir, output_dir):
    rel_path = os.path.relpath(input_file, input_dir)
    output_file = os.path.join(output_dir, rel_path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    return output_file

def batch_update_sensor_transformation(input_dir, output_dir, velocity, t):
    try:
        xml_files = list_xml_files(input_dir)
        if not xml_files:
            print("没有找到 XML 文件")
            return

        for input_xml_path in xml_files:
            output_xml_path = ensure_output_path(input_xml_path, input_dir, output_dir)
            try:
                update_sensor_transformation(input_xml_path, output_xml_path, velocity, t)
                print(f"成功处理文件：{input_xml_path}")
            except Exception as e:
                print(f"处理文件 {input_xml_path} 时出错：{e}")
    except Exception as e:
        print(f"批量处理任务失败：{e}")






# 示例用法
input_path = '/Users/liyuan/projects/Mitsuba3ToF/scenes/cornell-box_volumetric/scene_v3_transient.xml'
output_path = '/Users/liyuan/projects/Mitsuba3ToF/scenes/cornell-box_volumetric/scene_v3_transient_sensor_move.xml'
velocity = np.array([1000, 0, 0])
t = 0.0015
#update_sensor_transformation(input_path, output_path, velocity, t)

# 示例用法
input_dir = "/Users/liyuan/projects/Mitsuba3ToF/tof_tutorials/scenes_animation/domino"
output_dir = "/Users/liyuan/projects/Mitsuba3ToF/tof_tutorials/scenes_animation/domino_sensor_move"
velocity = np.array([100, 0, 0])
t = 0.0015
batch_update_sensor_transformation(input_dir, output_dir, velocity, t)
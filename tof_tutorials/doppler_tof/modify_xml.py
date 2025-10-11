import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import re, os

import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import re
import os

def update_transformation(input_xml_path, output_xml_path, velocity, t):
    # 提取文件名中的数字num
    filename = os.path.basename(input_xml_path)
    match = re.search(r'(\d+)', filename)
    num = int(match.group()) if match else 0

    # 解析XML文件
    tree = ET.parse(input_xml_path)
    root = tree.getroot()

    # 定义处理单个标签的函数
    def process_tag(parent_tag):
        # 找到所有符合条件的父标签（例如 sensor 或 emitter）
        parents = root.findall(parent_tag)
        if not parents:
            return

        for parent in parents:
            transforms = parent.findall('transform')
            if not transforms:
                continue  # 跳过没有 transform 的 parent

            for transform in transforms:
                # 创建animation标签
                animation_name = transform.get('name') or 'to_world'
                animation = ET.SubElement(parent, 'animation', attrib={'name': animation_name})

                # 创建第一个transform（时间t=0）
                transform0 = ET.SubElement(animation, 'transform', attrib={'time': '0'})
                # 复制原始transform的内容
                for child in transform:
                    new_child = ET.Element(child.tag, attrib=child.attrib)
                    new_child.text = child.text
                    for sub_child in child:
                        new_child.append(sub_child)
                    transform0.append(new_child)
                # 添加平移信息
                translate0 = {
                    'x': str(velocity[0] * t * num),
                    'y': str(velocity[1] * t * num),
                    'z': str(velocity[2] * t * num)
                }
                ET.SubElement(transform0, 'translate', attrib=translate0)

                # 创建第二个transform（时间t=0.0015）
                transform1 = ET.SubElement(animation, 'transform', attrib={'time': str(t)})
                # 复制原始transform的内容
                for child in transform:
                    new_child = ET.Element(child.tag, attrib=child.attrib)
                    new_child.text = child.text
                    for sub_child in child:
                        new_child.append(sub_child)
                    transform1.append(new_child)
                # 添加平移信息
                translate1 = {
                    'x': str(velocity[0] * t * (num + 1)),
                    'y': str(velocity[1] * t * (num + 1)),
                    'z': str(velocity[2] * t * (num + 1))
                }
                ET.SubElement(transform1, 'translate', attrib=translate1)

                # 移除原来的transform标签
                parent.remove(transform)

    # 处理sensor和emitter
    process_tag('sensor')
    process_tag('emitter')

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

def batch_update_transformation(input_dir, output_dir, velocity, t):
    try:
        xml_files = list_xml_files(input_dir)
        if not xml_files:
            print("没有找到 XML 文件")
            return

        for input_xml_path in xml_files:
            output_xml_path = ensure_output_path(input_xml_path, input_dir, output_dir)
            try:
                update_transformation(input_xml_path, output_xml_path, velocity, t)
                print(f"成功处理文件：{input_xml_path}")
            except Exception as e:
                print(f"处理文件 {input_xml_path} 时出错：{e}")
    except Exception as e:
        print(f"批量处理任务失败：{e}")





'''
# 示例用法
input_path = '/Users/liyuan/projects/Mitsuba3ToF/scenes/cornell-box/scene_v3_doppler copy.xml'
output_path = '/Users/liyuan/projects/Mitsuba3ToF/scenes/cornell-box/scene_v3_doppler copy_sensor_move.xml'
velocity = np.array([1000, 0, 0])
t = 0.0015
update_transformation(input_path, output_path, velocity, t)
'''

# 示例用法
input_dir = "/Users/liyuan/projects/new_mitsuba3tof/Mitsuba3ToF-sensor-motion/tof_tutorials/scenes_animation/domino"
output_dir = "/Users/liyuan/projects/new_mitsuba3tof/Mitsuba3ToF-sensor-motion/tof_tutorials/scenes_animation/domino_sensor_move"
velocity = np.array([100, 0, 0])
t = 0.0015
batch_update_transformation(input_dir, output_dir, velocity, t)

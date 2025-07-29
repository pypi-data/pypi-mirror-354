import argparse
import configparser
import csv
import json
import os


def entry():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="将CSV数据转换为基于配置的JSON文件")
    parser.add_argument('--csv', type=str, required=True, help='输入CSV文件路径')
    args = parser.parse_args()

    csv_file_path = args.csv
    output_dir = 'output_jsons'
    config_file = 'jsonconfig.conf'

    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    # 获取文件名模板和内容模板
    filename_template = config['filename']['template']
    content_template = config['content']['template']

    # 尝试解析 content_template 为 JSON 结构
    try:
        content_template_parsed = json.loads(content_template)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON template in config is not valid JSON: {e}")

    # 替换函数
    def replace_placeholders(template, data):
        if isinstance(template, dict):
            return {replace_placeholders(k, data): replace_placeholders(v, data) for k, v in template.items()}
        elif isinstance(template, list):
            return [replace_placeholders(item, data) for item in template]
        elif isinstance(template, str):
            try:
                return template.format(**data)
            except KeyError as e:
                raise KeyError(f"Missing key in CSV data for placeholder: {e}")
        else:
            return template

    # 读取CSV并生成JSON文件
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # 构建文件名
            filename = filename_template.format(**row)
            filepath = os.path.join(output_dir, filename)

            # 替换模板中的占位符
            json_data = replace_placeholders(content_template_parsed, row)

            # 写入JSON文件
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(json_data, jsonfile, ensure_ascii=False, indent=4)

    print("✅ 所有JSON文件已成功生成。")


if __name__ == '__main__':
    entry()

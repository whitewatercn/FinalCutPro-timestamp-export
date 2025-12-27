#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并版脚本：从 Final Cut Pro X XML (FCPXML) 提取时间标记（支持 `<marker>` 和 `<chapter-marker>`）
用法:
  python main.py -i Info.fcpxml -o FCPtimemarker.txt
"""

import os
import re
import argparse


def fraction_to_float(fraction_string):
    """将 X/Y 或 单独数字 转换为秒（float）。失败时返回 0.0。"""
    try:
        if '/' in fraction_string:
            numerator, denominator = fraction_string.split('/')
            return float(numerator) / float(denominator)
        else:
            return float(fraction_string)
    except Exception:
        return 0.0


def format_time(seconds):
    """把秒数转换为 MM:SS 格式字符串"""
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return '{:02d}:{:02d}'.format(minutes, secs)


def extract_markers(path):
    """从文件中提取 `<chapter-marker>` 时间标记（按文件出现顺序），
    如果多个 chapter-marker 的 `value` 相同，只保留第一次出现的项。
    返回字符串列表 "MM:SS comment"（按文件中首次出现的顺序）。"""
    seen_values = set()
    markers = []

    # 匹配完整的 <chapter-marker ... start="...s" ... value="..." ...>
    # 使用 DOTALL 以便 value 包含换行的情况也能被匹配
    pattern = re.compile(r'<chapter-marker\b[^>]*\bstart="([^"]+?)s"[^>]*\bvalue="([^"]*?)"[^>]*>', re.DOTALL)

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    for m in pattern.finditer(content):
        start = m.group(1).strip()
        value = m.group(2).strip()

        # 只保留首次出现的 value
        if value in seen_values:
            continue
        seen_values.add(value)

        secs = fraction_to_float(start)
        markers.append((secs, f'{format_time(secs)} {value}'.strip()))

    # 返回按文件顺序收集的条目（pattern.finditer 返回文件中匹配的顺序）
    return [line for _, line in markers]


def resolve_input_path(input_path):
    """如果 input_path 是一个文件夹（例如 .fcpxmld 包），尝试定位 Info.fcpxml，
    否则返回文件路径或抛出 FileNotFoundError。"""
    if os.path.isdir(input_path):
        info = os.path.join(input_path, 'Info.fcpxml')
        if os.path.isfile(info):
            return info
        # 回退：查找第一个以 .fcpxml 结尾的文件
        for entry in os.listdir(input_path):
            if entry.lower().endswith('.fcpxml'):
                return os.path.join(input_path, entry)
        raise FileNotFoundError(f'在文件夹 {input_path} 中未找到 Info.fcpxml 或其他 .fcpxml 文件')
    else:
        if os.path.isfile(input_path):
            return input_path
        raise FileNotFoundError(f'输入文件 {input_path} 不存在')


def main():
    parser = argparse.ArgumentParser(description='从 FCPXML 或 .fcpxmld 包提取时间标记并写入文本文件')
    parser.add_argument('-i', '--input', default='./Info.fcpxml', help='输入 FCPXML 文件或 .fcpxmld 包路径')
    parser.add_argument('-o', '--output', default='./FCPtimemarker.txt', help='输出文本文件路径')
    args = parser.parse_args()

    try:
        input_path = resolve_input_path(args.input)
    except FileNotFoundError as e:
        print(f'错误: {e}')
        return

    if input_path != args.input:
        print(f'解析到 FCPXML 文件: {input_path}')

    markers = extract_markers(input_path)
    with open(args.output, 'w', encoding='utf-8') as out:
        for line in markers:
            out.write(line + '\n')

    print(f'已写入 {len(markers)} 条时间标记到 {args.output}')


if __name__ == '__main__':
    main()

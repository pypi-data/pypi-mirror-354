import os
import shutil
import datetime
import subprocess
import re

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# setup_dir = "/mnt/f/wsl/chfs/公共配置/公共代码库/package/"
setup_dir = r"D:\code\打包\poxiao"
def update_version_in_setup():
    # 获取当前日期和时间作为版本号
    now = datetime.datetime.now()
    version = f"0.{now.strftime('%y%m%d')}.{now.strftime('%H')}"

    # 读取 setup.py 文件内容
    with open(f'{setup_dir}/setup.py', 'r', encoding='utf-8') as file:
        setup_content = file.read()

    # 使用正则表达式找到 version 的值并替换为当前日期和时间
    updated_content = re.sub(r"version\s*=\s*['\"]\d+\.\d+\.\d+['\"]", f"version = '{version}'", setup_content)

    # 写回 setup.py 文件
    with open('setup.py', 'w', encoding='utf-8') as file:
        file.write(updated_content)

    logging.info(f"版本号已更新为 {version}。")


def build_package():
    # 执行 setup.py sdist bdist_wheel
    subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], check=True)

    # 删除多余的文件和目录
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('poxiaoai.egg-info'):
        shutil.rmtree('poxiaoai.egg-info')
    if os.path.exists('dist'):
        # 删除 dist 目录中除 .whl 文件外的所有文件
        for item in os.listdir('dist'):
            if not item.endswith('.whl'):
                os.remove(os.path.join('dist', item))


def move_whl_to_package():
    # 创建 package 目录（如果不存在）
    package_dir = 'package'
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)

    # 创建 simple/poxiaoai 目录（如果不存在）
    simple_dir = '/mnt/f/wsl/chfs/公共配置/公共代码库/simple/poxiaoai'
    simple_dir = r'D:\code\打包\poxiao\package\poxiaoai'
    if not os.path.exists(simple_dir):
        os.makedirs(simple_dir)

    # 移动 .whl 文件到 package 目录
    if os.path.exists('dist'):
        for item in os.listdir('dist'):
            if item.endswith('.whl'):
                destination_path = os.path.join(package_dir, item)
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                    print(f"已删除旧文件 {destination_path}")
                shutil.move(os.path.join('dist', item), package_dir)
                print(f"{item} 已移动到 {package_dir}/")

                # 移动 .whl 文件到 simple/poxiaoai 目录
                simple_destination_path = os.path.join(simple_dir, item)
                print(f"simple_destination_path:{simple_destination_path}")
                if os.path.exists(simple_destination_path):
                    os.remove(simple_destination_path)
                    print(f"已删除旧文件 {simple_destination_path}")
                shutil.move(os.path.join(package_dir, item), simple_dir)
                print(f"{item} 已移动到 {simple_dir}/")

    # 删除 dist 目录（如果需要）
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    return simple_dir


if __name__ == '__main__':
    update_version_in_setup()
    build_package()
    path = move_whl_to_package()
    logging.info(f"构建完成。.whl 文件已移动到 {path} 目录。")
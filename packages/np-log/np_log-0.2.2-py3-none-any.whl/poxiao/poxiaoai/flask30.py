import heapq
import logging
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Thread

import schedule
from flask import Flask, request, jsonify

import flask30_shell

app = Flask(__name__)
# 存储启动时的文件目录

# 全局的时间点对应的优先级队列
time_priority_queues = {}
executor = ThreadPoolExecutor(max_workers=5)  # 设置线程池，最多同时运行 5 个线程
# 创建一个线程池执行器的字典，用于每个 deviceNum 的任务执行
thread_pools = defaultdict(lambda: ThreadPoolExecutor(max_workers=1))


# 添加任务到优先级队列
def add_task_to_queue(time_str, priority, task_name, params, device_num):
    # 如果该时间点还没有任务队列，则创建一个
    if time_str not in time_priority_queues:
        time_priority_queues[time_str] = []
        # 对应时间点调度任务
        schedule_task(time_str)

    # 将任务按优先级添加到队列中
    heapq.heappush(time_priority_queues[time_str], (priority, task_name, params, device_num))
    print(f"任务已添加: {task_name}, 时间: {time_str}, 优先级: {priority},设备号: {device_num}")


# 定义任务执行函数
def run_priority_tasks(time_str):
    # print(f"开始执行 {time_str} 的优先级任务...")
    # logging.error(f"开始执行 {time_str} 的优先级任务...")

    if time_str in time_priority_queues:
        queue = time_priority_queues[time_str]

        # 将任务按 deviceNum 分组
        tasks_by_device = defaultdict(list)
        while queue:
            priority, task_name, params, device_num = heapq.heappop(queue)
            tasks_by_device[device_num].append((priority, task_name, params))

        # 针对每个 deviceNum 创建/使用线程池来执行任务
        for device_num, tasks in tasks_by_device.items():
            for priority, task_name, params in tasks:
                print(
                    f"添加任务-->优先级放入设备编号线程中:{task_name}, 优先级: {priority}, 参数: {params}, 设备编号: {device_num}")
                logging.error(
                    f"添加任务-->优先级放入设备编号线程中:{task_name}, 优先级: {priority}, 参数: {params}, 设备编号: {device_num}")

                # 使用线程池执行任务
                thread_pools[device_num].submit(exec_shell_inner, task_name, params, device_num)

        # current_time = datetime.now()
        # print(f"【{current_time}, {time_str} 的任务执行完成。】")
        # logging.error(f"{current_time}, {time_str} 的任务执行完成。")


@app.route('/startTask', methods=['POST'])
def add_task():
    data = request.json
    task_name = data['task_name']
    priority = data['priority']
    time_str = data['time_str']
    device_num = data['device_num']
    params = data['params']
    # 添加任务到对应的优先级队列
    add_task_to_queue(time_str, priority, task_name, params, device_num)

    return jsonify({"message": f"任务 {task_name} 已添加，时间: {time_str}, 优先级: {priority}"}), 200


"""_syno 为必填后缀，该方法标识为该任务立即执行"""


@app.route('/startTask_syno', methods=['POST'])
def start_task():
    # 提交异步任务到线程池
    executor.submit(exec_shell_inner, "立即执行无任务名", request.json, "立即执行")
    return jsonify({'success': 'true', 'message': 'Task is running in the background.'}), 200


# 定时任务调度器的线程
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# 启动调度器线程
scheduler_thread = Thread(target=run_scheduler)
scheduler_thread.start()


def exec_shell_inner(task_name, json_data, execution_type):
    # 指定新的工作目录路径
    image_dir = app.config['BASE_DIR']
    os.chdir(image_dir)
    # 更改当前工作目录
    # 执行你的任务
    flask30_shell.exec_shell(task_name, json_data, execution_type)


# 定时任务：在指定时间执行优先级队列中的任务
def schedule_task(time_str):
    schedule.every().day.at(time_str).do(run_priority_tasks, time_str)


def create_timestamped_log_file(log_dir):
    # 获取当前时间并格式化为时间戳 (例如: 2024-10-11_15-30-00)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 构建带有时间戳的日志文件名 (例如: app1_2024-10-11_15-30-00.log)
    log_file_name = f'app1_{timestamp}.log'

    # 构建完整的日志文件路径
    log_file_path = os.path.join(log_dir, log_file_name)

    return log_file_path


@app.route('/')
def home():
    logging.info("Second Flask Service is Running!")  # 日志信息
    return "Second Flask Service is Running!"


if __name__ == '__main__':
    # 检查是否传入了 log_dir 参数
    if len(sys.argv) < 2:
        print("请提供日志目录路径。")
        sys.exit(1)

    # 从启动参数中获取 log_dir
    log_dir = sys.argv[1]
    port = sys.argv[2]
    base_dir = sys.argv[3]
    app.config['BASE_DIR'] = base_dir
    print(log_dir)
    print(port)
    print(f"当前文件目录:{app.config['BASE_DIR']}")
    log_file_path = create_timestamped_log_file(log_dir)
    print(f"日志文件路径：{log_file_path}")
    # 检查并创建日志目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 删除之前可能存在的配置
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    file = open(log_file_path, encoding="utf-8", mode="a")
    logging.basicConfig(
        stream=file,
        # 设定日志记录最低级别
        level=logging.DEBUG,
        datefmt='%Y/%m/%d %H:%M:%S',
        format='%(asctime)s - %(message)s'
    )
    app.run(host='0.0.0.0', port=port)

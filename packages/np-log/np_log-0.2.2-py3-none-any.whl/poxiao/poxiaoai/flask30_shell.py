import logging



def exec_shell(task_name, params, device_num):
    # print(f"{datetime.now()}【开始执行任务】设备号：{device_num}-任务名：{task_name} ")
    # logging.error(f"{datetime.now()}【开始执行任务】设备号：{device_num}-任务名：{task_name}")  # 日志信息

    logging.error(params)

    name = params.get('opt_type', '')  # 调用时，如果为空，则取默认值
    dev_num = params.get('device_num', '')
    app_name = params.get('app_name', '')

    if name == '打招呼':
        pass
    elif name == '消息回复':
        pass

    logging.error(f'BOSS{name}-脚本执行完毕')

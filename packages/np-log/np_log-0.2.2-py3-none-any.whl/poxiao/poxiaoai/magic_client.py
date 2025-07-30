import requests
import time
from np_log import setup_logging

logger = setup_logging('magic_api',console_level="error")
# logging = setup_logging('magic_api')

# 全局变量 - 基础URL
BASE_URL = 'http://192.168.31.125:9999'

class RequestClient:
    def __init__(self, timeout=10, retries=3, retry_delay=2):
        self.timeout = timeout
        self.retries = retries  # 最大重试次数
        self.retry_delay = retry_delay  # 每次重试间隔时间（秒）

    def post(self, endpoint, params=None, data=None, json=None, headers={'Content-Type': 'application/json'}):
        # 检查 endpoint 是否以 '/' 开头
        if not endpoint.startswith('/'):
            endpoint = f"/{endpoint}"
        url = f"{BASE_URL}{endpoint}"
        # logger.info(f"Sending POST request to {url}")
        # logger.debug(f"Request data: {data}")
        # logger.debug(f"Request json: {json}")
        # logger.debug(f"Request headers: {headers}")

        for attempt in range(self.retries):
            try:
                response = requests.post(url, params=params,  data=data, json=json, headers=headers, timeout=self.timeout)
                response.raise_for_status()  # 如果状态码不是200，抛出HTTPError
                # logger.info(f"Response status code: {response.status_code}")
                # logger.debug(f"Response content: {response.text}")
                return response
            except requests.exceptions.RequestException as err:
                logger.error(f"Attempt {attempt + 1} failed: {err}")
                if attempt < self.retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("All retries failed.")
                    raise  # 抛出最后的异常

    def get(self, endpoint, params=None, headers=None):
        # 检查 endpoint 是否以 '/' 开头
        if not endpoint.startswith('/'):
            endpoint = f"/{endpoint}"
        url = f"{BASE_URL}{endpoint}"
        # logger.info(f"Sending GET request to {url}")
        # logger.debug(f"Request params: {params}")
        # logger.debug(f"Request headers: {headers}")

        for attempt in range(self.retries):
            try:
                response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
                response.raise_for_status()  # 如果状态码不是200，抛出HTTPError
                # logger.info(f"Response status code: {response.status_code}")
                # logger.debug(f"Response content: {response.text}")
                return response
            except requests.exceptions.RequestException as err:
                logger.error(f"Attempt {attempt + 1} failed: {err}")
                if attempt < self.retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("All retries failed.")
                    raise  # 抛出最后的异常

    def call_api(self, endpoint, method='get', params=None, json_data=None):
        """
        通用API调用函数
        :param endpoint: API端点
        :param method: 请求方法(get/post)
        :param params: 请求参数
        :param json_data: JSON数据
        :return: API响应或None
        """
        try:
            if method.lower() == 'get':
                response = self.get(endpoint, params=params)
            else:
                response = self.post(endpoint, params=params, json=json_data)
            if response.status_code == 200:
                # data = response.json().get("data", "")
                return response.json().get("data", "")
            else:
                logger.error(f"API调用失败({endpoint}): {response.text}")
        except Exception as e:
            logger.error(f"API调用异常({endpoint}): {str(e)}")
        return None

def magic_api(endpoint, method='get', params=None, json_data=None):
    client = RequestClient()
    return client.call_api(endpoint, method, params=params, json_data=json_data)
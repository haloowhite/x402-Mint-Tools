import json
import time
from typing import Any

import json_repair
import requests
from loguru import logger


class X402Monitor:
    """
    X402 服务监控类
    用于监控 x402scan.com 上新上线的服务，当检测到新服务时发送通知
    """

    def __init__(self, cache_file_path: str = "x402_services_cache.json"):
        """
        初始化监控实例
        :param cache_file_path: 缓存文件路径，用于存储已监控的服务ID
        """
        self.cache_file_path = cache_file_path
        self.monitored_services = self.read_local_cache(cache_file_path)

    def read_local_cache(self, file_path):
        """
        读取本地缓存文件，首次运行会尝试将第一次请求到的数据写入本地缓存
        该文件用于存储已监控过的 servers，避免重复通知
        :param file_path:
        :return:
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"本地缓存已加载 -> {file_path}")
            return data
        except FileNotFoundError:
            logger.info("首次运行，未找到本地缓存文件...")
            return []

    def write_local_cache(self, file_path, data):
        """
        写入本地缓存文件
        该文件用于存储已监控过的 servers，避免重复通知
        :param file_path:
        :param data:
        :return:
        """
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"本地缓存已更新, 共{len(data)}条记录 -> {file_path}")

    def get_single_value_by_key(self, json_obj: dict, target_key: str) -> Any:
        """
        辅助函数 -> 从 JSON 对象中获取指定 key 的第一个值
        :param json_obj:
        :param target_key:
        :return:
        """
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                if key == target_key:
                    return value
                elif isinstance(value, (dict, list)):
                    result = self.get_single_value_by_key(value, target_key)
                    if result is not None:
                        return result
        elif isinstance(json_obj, list):
            for item in json_obj:
                result = self.get_single_value_by_key(item, target_key)
                if result is not None:
                    return result
        return None

    def get_public_services(self, page=0, page_size=20):
        """
        获取 x402scan.com 上的公共服务列表
        :param page: 页码，从0开始
        :param page_size: 每页服务数量
        :return: 解析后的服务数据
        """
        # 获取公共服务列表
        params = {
            "batch": "1",
            "input": json.dumps({
                "0": {
                    "json": {
                        "pagination": {
                            "page_size": page_size,
                            "page": page  # 页码参数
                        }
                    }
                }
            })
        }

        for _ in range(3):
            try:
                response = requests.get(
                    "https://www.x402scan.com/api/trpc/public.sellers.bazaar.list",
                    params=params,
                    headers={
                        "accept": "*/*",
                        "trpc-accept": "application/jsonl",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                    }
                )
                return json_repair.loads(response.text)
            except:
                continue

    def service_parser(self, service_resp: dict):
        """
        解析服务响应数据，提取服务列表和分页信息
        :param service_resp: 从 API 获取的原始响应数据
        :return: (服务列表, 是否有下一页)
        """
        service_list = self.get_single_value_by_key(service_resp, "items")
        has_next = self.get_single_value_by_key(service_resp, "hasNextPage")
        return service_list, has_next

    def send_notification(self, service_info: str):
        """
        发送新服务上线通知
        TODO: 需要用户自行实现通知发送功能，可以接入微信、钉钉、Telegram 等

        :param service_info: 要发送的服务信息字符串
        :return: None
        """
        logger.debug("当前未配置相关通知服务，请自行实现 send_notification 方法")
        logger.success(service_info)

    def monitor(self, loop_time_interval: int = 30):
        """
        启动监控程序
        首次运行会初始化本地缓存，之后每隔指定时间检查一次新服务

        :param loop_time_interval: 监控轮询间隔时间（秒）
        """
        if not self.monitored_services:
            logger.info("首次运行，正在初始化本地缓存，请稍候...")
            page_size = 10000  # 设置一个较大的页数上限，确保获取所有服务
            services_resp = self.get_public_services(page=0, page_size=page_size)
            service_list, has_next = self.service_parser(services_resp)
            service_id_list = [j['id'] for i in service_list for j in i['origins']]
            self.write_local_cache(self.cache_file_path, service_id_list)
            self.monitored_services = self.read_local_cache(self.cache_file_path)
            logger.success("已缓存所有现有 x402 服务，监控程序即将启动...")
        while True:
            page_size = 500
            page = 0
            has_next = True
            while has_next:
                logger.debug(f"正在获取第 {page} 页的服务列表...")
                try:
                    services_data = self.get_public_services(page=page, page_size=page_size)
                    service_list, has_next = self.service_parser(services_data)
                except Exception as e:
                    logger.error(f"获取服务列表失败: {e}")
                    break
                for service in service_list:
                    for origin in service['origins']:
                        service_id = origin['id']
                        if service_id not in self.monitored_services:
                            message = (
                                f"监控到新上线的 x402 服务!\n"
                                f"名称: {' | '.join([i['title'] or '暂无' for i in service['origins']])}\n"
                                f"服务描述: {' | '.join([i['description'] or '暂无' for i in service['origins']])}\n"
                                f"服务域名: {' | '.join([i['origin'] or '暂无' for i in service['origins']])}\n"
                                f"收款地址: {' | '.join(service['recipients'] or '暂无')}\n"
                                f"服务链接: https://www.x402scan.com/server/{origin['id']}\n"
                            )
                            logger.debug(f"检测到新服务上线: {service}")
                            print("================ 新服务上线 (DEBUG) ================")
                            print(message)
                            print("===================================================")
                            self.send_notification(message)
                            self.monitored_services.append(service_id)
                            self.write_local_cache(self.cache_file_path, self.monitored_services)
                page += 1
            logger.info(f"本轮监控完成，等待 {loop_time_interval} 秒后进行下一轮监控...")
            time.sleep(loop_time_interval)


if __name__ == '__main__':
    # 主程序入口
    # 配置每轮监控间隔时间，单位：秒
    loop_time_interval = 30

    # 创建监控实例并开始监控
    x_402_monitor = X402Monitor()
    x_402_monitor.monitor(loop_time_interval)

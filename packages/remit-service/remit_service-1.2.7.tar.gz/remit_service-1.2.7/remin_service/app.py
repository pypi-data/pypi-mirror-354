import asyncio

from remin_service.log import logger
import os
import threading
from fastapi.staticfiles import StaticFiles
from remin_service.base.controller import Controller
from remin_service.base.base_app import RemitFastApi
from remin_service.base.base_router import BaseRemitAPIRouter
from remin_service.helper.config_helper import ConfigLoad
from .config import Config, ServiceConfig, NaNosConfig


class FastSkeletonApp:

    _instance_lock = threading.Lock()
    app = None
    init_routes = None

    @classmethod
    def instance(cls, init_routes, title="Et Admin API接口文档管理系统"):
        with FastSkeletonApp._instance_lock:
            if not hasattr(FastSkeletonApp, "_instance"):
                FastSkeletonApp._instance = FastSkeletonApp(init_routes, title)

        return FastSkeletonApp._instance

    def __init__(
            self,
            init_routes,
            __file__,
            resources_path=None,
            static_dir=f"{os.path.dirname(__file__)}/static",
            middleware_func=None
    ):
        if not __file__:
            raise Exception("__file__ is required")
        if not resources_path:
            raise Exception("No resources path provided")
        self.service_path = os.path.dirname(__file__)
        ConfigLoad.instance(resources_path, self.service_path).load()
        self.app = RemitFastApi(
            docs_url=None,
            redoc_url=None,
            api_router_class=BaseRemitAPIRouter,
            title="Api接口",
            version='1.0'
        )

        self.nacos_client = None
        if NaNosConfig.discovery and NaNosConfig.discovery.server_addr:
            from nacos import NacosClient
            self.nacos_client = NacosClient(
                server_addresses=NaNosConfig.discovery.server_addr,
                namespace=NaNosConfig.discovery.namespace
            )

        self.config = Config
        self.app.HOST = ServiceConfig.ip
        self.app.PORT = ServiceConfig.port
        self.app.ServerName = ServiceConfig.service_name
        self.app.AppBaseDir = self.service_path
        self.static_dir = static_dir
        self.middleware_func = middleware_func

        # 路由配置
        self.init_routes = init_routes
        Controller.init_app(self.app)
        self.init()

    def init(self):

        self.app.mount(
            '/static',
            StaticFiles(directory=self.static_dir),
            name='static'
        )
        from .config import NaNosConfig, ServiceConfig

        if NaNosConfig.discovery and NaNosConfig.discovery.server_addr:
            self.nacos_client.add_naming_instance(
                ServiceConfig.service_name, ServiceConfig.get_ip(), ServiceConfig.port,
                cluster_name=NaNosConfig.discovery.cluster_name,
                group_name=NaNosConfig.discovery.group
            )
            logger.info("Nacos 注册成功...")

            async def long_running_task():
                """一个长时间运行的异步任务示例"""
                while True:
                    self.nacos_client.send_heartbeat(
                        service_name=ServiceConfig.service_name,
                        ip=ServiceConfig.get_ip(),
                        port=ServiceConfig.port,
                        cluster_name=NaNosConfig.discovery.cluster_name,
                        group_name=NaNosConfig.discovery.group
                    )
                    await asyncio.sleep(10)  # 每30秒执行一次

            @self.app.on_event("startup")
            async def startup_event():
                logger.info("启动长时间运行的任务...")
                asyncio.create_task(long_running_task())

            @self.app.on_event("shutdown")
            async def shutdown_event():
                self.nacos_client.remove_naming_instance(
                    ServiceConfig.service_name, ServiceConfig.get_ip(), ServiceConfig.port,
                    cluster_name=NaNosConfig.discovery.cluster_name,
                    group_name=NaNosConfig.discovery.group
                )

        # 批量导入注册路由
        self.init_routes(self.app)

        # 注册中间件
        if self.middleware_func:
            self.middleware_func(self.app)

        @self.app.on_event("startup")
        async def startup_event():
            logger.info(f"[Api] 【{self.app.ServerName}】-【{self.config.active}】服务启动")

        @self.app.on_event("shutdown")
        async def shutdown_event():
            logger.info(f"[Api] 【{self.app.ServerName}】-【{self.config.active}服务关闭")



from setuptools import setup, find_packages


setup(
    name="remit_service",
    version="1.2.7",
    author="beixiaobei",
    author_email="1113855149@qq.com",
    description="扩展Fastapi的微服务框架, 支持 Class Route、Class View、配置注入装饰器",
    packages=find_packages(
        include=[
            "remin_service", "remin_service.*"
        ]
        # exclude=[
        #     "src",
        # ]
    ),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    package_data={
        'remin_service': ['static/**', "README.md"],  # 包含所有 .py 文件
    },
    install_requires=[
        "fastapi==0.115.6",
        "uvicorn==0.28.1",
        "loguru==0.7.3",
        "PyYAML==6.0.2",
        "PyYAML==6.0.2",
        "python-nacos==0.1.1"
    ],
    python_requires=">=3.10",
    include_package_data=True
)
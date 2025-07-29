# remit-service
**remit-service**是基于FastApi框架扩展出支持多配置文件、配置注入的框架

- 类试图
- 类路由
- 蓝图路由
- 服务管理
- 多配置文件
- 配置注入

## 配置介绍

### 单体项目配置文件介绍

所有的配置都是已yaml支持

主配置文件`project/resources/config.yaml`

**resources**文件目录这是必须存在的, 这是存储资源文件的必须目录, 加载配置文件首先会定位resources目录

```yaml
config:
  # 激活环境， 获取ENV环境变量，如果不存在赋值env
  active: !env ${ENV, dev}
```

环境配置文件`project/resources/config.dev.yaml`
```yaml
service:
  ip: 0.0.0.0           # 项目启动ID
  port: 9045            # 项目启动端口
  service_name: test    # 服务启动名称
```

----
### 多服务项目配置文件介绍

主配置文件`project/resources/config.yaml`
```yaml
config:
  # 激活环境， 获取ENV环境变量，如果不存在赋值env
  active: !env ${ENV, dev}
  # 跟随启动服务的配置文件
  include: !config ${service:True}
```
- include：引入配置文件
  - `!config ${service:True}`: 加载当前启动服务的配置文件

服务配置文件`project/a_service/resources/config.dev.yaml`
```yaml
service:
  ip: 0.0.0.0           # 项目启动ID
  port: 9045            # 项目启动端口
  service_name: a       # 服务启动名称
```

## 项目启动

### 定义视图
视图文件`project/view/a.py`
```python
from remin_service.base.controller import Controller, RequestGet

@Controller(prefix="", tags=["测试接口"])
class DocsView:

  @RequestGet(path="/a")
  async def get_documentation(
          self,
  ):
    pass
```

路由注册`project/init_router.py`
```python
from remin_service.base.load_router import register_nestable_blueprint_for_log

def init_routes(fastapi_app):
  # 此处必须用__name__, 否则会自动引入两次
  register_nestable_blueprint_for_log(
    fastapi_app, __name__, api_name='a'
  )
```

项目启动文件`project/main.py`
```python
import os
import uvicorn
from remin_service.app import FastSkeletonApp
from init_router import init_routes
resources_path = os.path.dirname(__file__)

app = FastSkeletonApp(
    init_routes,
    __file__,
    resources_path=resources_path
).app

if __name__ == '__main__':
  if __name__ == '__main__':
    uvicorn.run(app=app, host=app.HOST, port=app.PORT)

```


## 配置注入
视图文件`project/a_service/resources/config.dev.yaml`
```yaml
service:
  ip: 0.0.0.0           # 项目启动ID
  port: 9045            # 项目启动端口
  service_name: a       # 服务启动名称

test:
  a: a
  b: b
```

注入文件`project/**/config.py`
```Python
from pydantic import BaseModel
from remin_service.config import ImportConfig

@ImportConfig("test")
class Test(BaseModel):
  a: str
  b: str
```
  
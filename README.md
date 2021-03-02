## 使用WSL2+docker-compose+vsCode创建的python开发环境 
  示例代码是使用fastAPI搭配postgreSQL ORM构建的入门示例接口,
  
  实现简单用户接口、文件上传，接口详情部署完成后查看
  <a href="http://127.0.0.1:8001/api/v2/redocs" target="_blank">交互式文档</a>
  
  结合fastAPI框架方便的 API 调试，生成 API 文档，
  
  可快捷高效开发项目，支持热加载，保存文件即看见效果，无需操作docker。


---

## 运行方式

- git clone后cd到目录直接执行
```shell
  docker-compose up -d
```

正常情况下访问

<a href="http://127.0.0.1:8001" target="_blank">127.0.0.1:8001</a> 将显示 Hello World!

<a href="http://127.0.0.1:8001/api/v2/docs" target="_blank">127.0.0.1:8001/api/v2/docs</a>  &nbsp;&nbsp; &nbsp;   <a href="http://127.0.0.1:8001/api/v2/redocs" target="_blank">交互式文档</a>

<a href="http://127.0.0.1:8001/api/v2/redocs" target="_blank">127.0.0.1:8001/api/v2/redocs</a>

进入交互式API文档，测试示例接口如用户注册接口，测试相关接口功能是否正常。



如若无法正常访问 可能是pip没有升级成功导致有些依赖包没安装成功 执行
```docker
    docker-compose exec miniprogram /bin/bash
    
    进入容器升级pip 然后重新安装更新依赖库 执行
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U pip
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    退出容器
    exit
    
    然后重启容器
    docker-compose restart miniprogram
    如若还是不行查看docker-compose日志或进入容器执行程序查看报错信息，如缺少依赖包就手动安装
     docker-compose logs -f miniprogram
     或进入容器执行
     uvicorn main:app
     查看报错信息并解决
```
     
    
----


FROM python:3.8

MAINTAINER colinxia<543384208@qq.com>

WORKDIR /app

## RUN pip install pip -U && pip install -r requirements.txt
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
## CMD ["uvicorn","app.main:app","--reload","--host","0.0.0.0","--port","15400"]
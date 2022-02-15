# AIVTuber1.0-CoupletBot

<img src="https://gitee.com/AICollector/picgo/raw/master/AIVTUBER.PNG" alt="AIVTUBER" style="zoom: 50%;" />

## 项目简介

受复旦大学自然语言处理入门练习项目-**[nlp-beginner](https://github.com/FudanNLP/nlp-beginner)**中任务三任务五启发，利用BiLSTM训练大规模对联语料，并将训练的模型部署到本地推理环境。服务器端部署直播间监测程序，监测直播间观众发言，存储到云服务器的弹幕数据库中。本地推理环境监测弹幕数据库更新，并对有效的上联进行推理，调用百度云语音合成API响应观众发言。

## 直播平台

BiliBili

## 项目架构

### Train

Train文件下包含了训练模型所需的代码，训练出来的模型需要拷贝到Infer下用于模型推理。训练数据集为经过清洗，删除敏感词汇的对联数据集：[对联数据集](https://github.com/v-zich/couplet-clean-dataset)。使用四库全书的预训练词向量：[中文词向量大全](https://github.com/Embedding/Chinese-Word-Vectors)

### Server

Server文件下为监测程序。需要首先下载并部署项目[ProxyPool](https://github.com/Python3WebSpider/ProxyPool)。开启IP代理池，以防止直播平台封ip。创建mysql数据库bili-live，并开放3306端口。 直播间的roomid可以在Bilibili直播网页版的网址找到。`tcheck.py`为百度的文本敏感词检测API，防止Bot回复恶意的评论。

````python
'''
文本审核接口
'''
AK=''  # 填写自己的密钥
SK=''  # 填写自己的密钥
````

运行：

```
python pipline.py
```

进行监测任务，在直播间进行测试，若发送弹幕后数据库存储弹幕则监测程序没有问题。

### Infer

Infer为部署在本地的推理程序。`tts.py`为语音合成的API。需要填写自己的密钥：

```python
API_KEY = ''
SECRET_KEY = ''
```

运行：

```
python infer.py
```

模型加载需要1min左右，若可以与远程数据库联通并且能够响应数据库中的上联数据则测试成功。






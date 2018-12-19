### 作业需求:

1. 在之前开发的FTP基础上，开发支持多并发的功能
2. 必须用到队列Queue模块，实现线程池
3. 允许配置最大并发数，比如允许只有10个并发用户

### 更新
在原代码的基础上，做了以下更新：
1. 添加线程池模块Mypool，并基于线程池重构了服务器代码
2. 写数据部分加锁DB_LOCK，防止文件操作冲突
3. 以上两项均在config_server中配置
    
#### 可用账户
laowang|1234|100
luffy|1234|100
lee|1234|1000

#### 可用命令
```
      #  首次登陆认证通过之后会在data/user_data下建立用户目录
    ls # 查看当前目录
    cd xxx # 进入xxx目录
    cd .. # 返回上级目录  若在用户home下，此命令无效
    mkdir xxx # 在当前目录下创建xxx目录
    rm xxx # 可删除文件也可删除文件夹xxx
    put xxx  # 将文件xxx上传到当前目录下 xxx为完整路径名
    get xxx zzz #将xxx下载到本地 data_client/local_data下
      #   直接关闭客户端，服务端服务线程会继续完成信息的更新
      #   断点续传未实现
```

#### 目录结构
```
.
├── bin
│   ├── run_client.py      客户端启动
│   └── run_server.py      服务端启动
├── conf                      配置
│   ├── config_client.py
│   ├── config_server.py
│   └── __init__.py
├── core
│   ├── auth
│   │   ├── auth_client.py
│   │   ├── auth_server.py
│   │   └── __init__.py
│   ├── client
│   │   ├── FTPClient.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── server
│       ├── FTPServer.py
│       └── __init__.py
├── data                  数据文件夹
│   ├── account_data
│   │   ├── user_tbl
│   │   └── user_tbl_2
│   └── user_data
│       ├── laowang
│       ├── lee
│       │   └── mydata
│       └── wang
│           └── zz
├── data_client
│   └── local_data
└── readme.md

```


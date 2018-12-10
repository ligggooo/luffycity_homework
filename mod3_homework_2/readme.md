#### 要求：

1. 用户加密认证
    > 密码非明文传输
2. 允许同时多用户登录
    > 服务端支持多线程
3. 每个用户有自己的家目录 ，且只能访问自己的家目录
    > 在data/user_data目录下有每个用户的子目录
4. 对用户进行磁盘配额，每个用户的可用空间不同
    > 配额与账户绑定，存文件和删除文件时可用空间会更新，上传文件超过可用空间的文件会被服务器拒绝
    
    > 支持 vol方法查看配额和空间占用信息
5. 允许用户在ftp server上随意切换目录
    > 实现了cd mkdir rm方法，切换目录仅限于用户自己的根目录下
6. 允许用户查看当前目录下文件
    > 实现了ls方法
7. 允许上传和下载文件，保证文件一致性(md5)
    > put方法上传文件，服务器端会验证md5且会将结果通知客户端
    
    > get方法下载文件，客户端会验证md5
8. 文件传输过程中显示进度条
    > 上传下载都会显示进度条
9. 附加功能：支持文件的断点续传
    > 此功能未实现
    
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


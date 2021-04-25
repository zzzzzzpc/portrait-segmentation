# portrait-segmentation

使用U-net网络实现的人像分割系统，采用flask搭建了迷你的界面并且将模型部署于Tensorflow Serving。

❗模型文件我稍后上传。

## 目录结构

- /
   - segmentation
        - client_rest.py
        - utils.py
   - static
        - css
        - images
   - templates
        - index.html
        - index_ok.html
   - app.py
   - README.md
   - requirements.txt
   

segmentation：保存了人像分割图像预处理与后处理的函数，包括和服务器通信部分的代码。  
static：css样式，images文件夹会临时保存上传的图片以及最终模型输出的图片。  
templates：保存了index.html和index_ok.html，分别对应上传和上传成功之后的页面。  
app.py：完成图片上传的读取和保存。

## How to use❓

### 安装Tensonflow Serving

首先将模型部署于Tensorflow Serving，我使用的是Ubuntu18.04 LTS版本，如果你使用了Mac或者Win系统，其步骤应该大同小异：

在Ubuntu中安装docker（其他系统见[此处](https://docs.docker.com/get-docker/)）：

```bash
sudo apt-get update
```

下载相应包：

```bash
sudo apt-get install \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common
```

添加GPG key：

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

确认一下你目前使用的key：

```bash
sudo apt-key fingerprint 0EBFCD88
```

如果配置正确，你会看到：

```bash
pub   rsa4096 2017-02-22 [SCEA]
      9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid           [ unknown] Docker Release (CE deb) <docker@docker.com>
sub   rsa4096 2017-02-22 [S]
```

设置使用稳定版本的docker库：

```bash
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

更新索引，下载docker：

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

确认docker是否安装成功，运行hello world实例程序，如果安装成功，应该输出hello world文本：

```bash
sudo docker run hello-world
```

在docker中安装tensorflow serving：

```bash
docker pull tensorflow/serving
```

使用下面的命令查看已经安装的镜像：

```bash
docker image ls
```

使用下面命令查看运行或者曾经运行的容器：

```bash
docker ps -a
```

### 部署模型

首先将模型文件目录“export”上传到服务器的/home/user/目录下（user是你自己的用户名称）

执行代码，监听8501端口，使用restful api：

```bash
docker run -p 8501:8501 \
--mount type=bind,\
source=/home/user/export,\
target=/models/export/ \
-e MODEL_NAME=export -t tensorflow/serving &
```

### Run

python3.6环境下（我建议使用环境管理工具）：

```bash
pip install -r requirements.txt
python app.py
```


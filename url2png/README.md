# URL to image

代码地址：[https://github.com/liuzl/py_misc/tree/master/url2png](https://github.com/liuzl/py_misc/tree/master/url2png)

## 运行平台

在Windows、Mac、Ubuntu系统均可运行。

## 所需软件

* chrome浏览器
* [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/home)
  * 下载安装对应系统的程序，并设置`PATH`环境变量
  * ubuntu系统可直接`sudo apt install chromium-chromedriver`
* python3*（推荐使用Anaconda安装python3）*
  * selenium
  * PIL

## 使用方法

```sh
# python url2png.py <url> <pngfilename>
# 图片默认会存储到results目录
python url2png.py 'https://en.wikipedia.org/wiki/John_von_Neumann' John_von_Neumann.png
```

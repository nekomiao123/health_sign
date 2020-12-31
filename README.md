# 健康打卡脚本

## 说明

**本打卡脚本仅供学习交流使用，请勿过分依赖。开发者对使用或不使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。**

## 1.0版本简介 （healthsign.py就是1.0版本）

此脚本使用的是python + selenium库的方式进行模拟人工打卡，并使用了chrome driver去控制chrome浏览器

## 食用说明

- 需要先安装selenium

```
pip install selenium
```

- 在电脑上安装[chromedriver](http://www.testclass.net/selenium_python/selenium3-browser-driver)和chrome浏览器

- 值得注意的是chromedriver的版本号要和chrome一致才行（在chrome浏览器设置里面的About Chrome就可以看到chrome版本号了）
- 打开healthsign.py文件，在usernames的列表里面以字符串的形式填入学号运行即可

## 2.0版本会直接抓包执行（healthsign2.py就是2.0版本）

## 2.0来了 

这一版本直接用requests的方式执行，更加高效便捷

## 食用说明

- 需要先安装requests

```
pip install requests
```

- 开发环境是python 3.8.2 
- 这一个版本直接跑就可以了

## 注意事项

有些会报错 说某些数据不存在 

去google浏览器里面按F12进入开发者模式 然后按下图的图标 变成手机模式 打卡一次 以后就好了（我也不知道为什么）

![image-20201226205958468](https://cdn.jsdelivr.net/gh/nekomiao123/pic/img/image-20201226205958468.png)

## 3.0 来了（healthsign3.py就是3.0）

我写完2.0，用了第一天就发现2.0有问题，只有在当天打过卡之后，我才能得到历史数据（总的来说，就是我写了个寂寞）

3.0就这么出世了

### 食用说明

- 需要先安装requests

```
pip install requests
```

- 开发环境是python 3.8.2 
- 这一个版本直接跑就可以了
- 文字会提示是否已经打过卡（目前测试样例很少，但应该是准确的）

### 图示

![](https://cdn.jsdelivr.net/gh/nekomiao123/pic/img/image-20201228185614331.png)

### github action
文件里面那个healthsign3_ac.py就是专门用在github action的文件

# 未完成情况

多多测试代码是否完善
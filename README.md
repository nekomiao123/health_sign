# 健康打卡脚本
## 1.0版本简介 

此脚本使用的是python + selenium库的方式进行模拟人工打卡，并使用了chrome driver去控制chrome浏览器

## 食用说明

- 需要先安装selenium

```
pip install selenium
```

- 在电脑上安装[chromedriver](http://www.testclass.net/selenium_python/selenium3-browser-driver)和chrome浏览器

- 值得注意的是chromedriver的版本号要和chrome一致才行（在chrome浏览器设置里面的About Chrome就可以看到chrome版本号了）
- 打开healthsign.py文件，在usernames的列表里面以字符串的形式填入学号运行即可

## 2.0版本会直接抓包执行 预计后期可以部署在github action上

未完待续
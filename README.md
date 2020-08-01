# yunpan_be
某到处存在妥协的django后台

| 版本 |   日期    | 描述 |  作者   |
| :--: | :-------: | :--: | :-----: |
| v0.1 | 2020-8-2 | 后台第一版施工完成 | 颜屹豪-17308195 |

## 安装依赖项
默认已经安装python，目前仅需额外安装django  
```pip install -r requirement.txt```

## 创建表结构
```
python manage.py makemigrations
python manage.py migrate
```

## 启动后台
```
python clear.py
python manage.py runserver
```
clear会定期清理tmp_files下的过期文件，目前暂定10分钟

## API文档
[API文档](https://github.com/NoManWorkingITPJMnage/Blog/blob/master/final/%E9%9C%80%E6%B1%82%E8%AF%B4%E6%98%8E%E4%B9%A6.md)

# yunpan_be
某到处存在妥协的django后台

| 版本 |   日期    | 描述 |  作者   |
| :--: | :-------: | :--: | :-----: |
| v0.1 | 2020-8-2 | 后台第一版施工完成 | StarashZero 颜屹豪-17308195 |

## 安装依赖项
默认已经安装python，目前仅需额外安装django  
```pip install -r requirement.txt```

## 创建表结构
```
python manage.py makemigrations
python manage.py migrate
```

## 创建文件夹
data_files（数据文件）、tmp_files（临时文件）

## 启动后台
```
python clear.py
python manage.py runserver
```
clear会定期清理tmp_files下的过期文件，目前暂定10分钟

## API文档
[API文档](https://github.com/NoManWorkingITPJMnage/Blog/blob/master/final/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1.yml)

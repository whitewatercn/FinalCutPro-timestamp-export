# FCPexport
用来将final cut pro导出的xml文件中的时间轴转化为`X分：X秒 内容`，方便上传播客平台

# 具体用法
在final cut pro中打完时间轴（注意需要使用章节chapter标记，就是黄色这个）


<img width="501" alt="image" src="https://github.com/user-attachments/assets/99e528fb-593e-451f-9b8a-bd2ca4c06d08">

选择文件-导出xml，即可导出一个`.fcpxmld`文件包

![image](https://github.com/whitewatercn/FCPexport/assets/58654928/f02551f7-0324-4963-b969-62f916aecbe0)



运行`python main.py -i xxx.fcpxml文件的路径`，比如
```shell
python main.py -i '/Users/ww/coding/FinalCutPro-timestamp-export/针灸第一期.fcpxmld' 
```

即可获得一个`FCPtimemarker.txt`文件，打开就是比较通用的的时间轴啦
```
00:02 小白尽话论新系列！
00:32 嘉宾介绍：来自杏林印象的James和来自茶余课后的惊奇队长
03:03 最近杏林在做什么？博物馆展览日北中医牌面！
03:03 最近杏林印象在做什么？
```

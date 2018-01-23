## 知识问答助手

#### 支持（百万英雄、冲顶大会、芝士超人、一直播等平台）

## 编译提示：

- python3.6 
- pip install requrements.txt
- pip install XXX

## 配置

Run —>  Terminal输出如下

```
Hiro答题助手启动，请打开config.ini配置ORC key 与vm_name
识别出错时请打开\screenshots\text_area.png查看并修改windows.py中的截取参数！

自动搜索，请注意看题
```

1）工程中使用的网易MuMu模拟器，打开不同APP需要更改config.ini文件中的vm_name

2）注意windows.py如下部分

```
    image = Image.open(source_file)
    wide = image.size[0]
    #region = image.crop((20, 125, wide- 20, 370)) #西瓜视频
    #region = image.crop((20, 180, wide-20, 460)) # test
    #region = image.crop((20, 160, wide - 20, 440))  # UC
    #region = image.crop((20, 160, wide - 20, 440))  # 花椒
    #region = image.crop((20, 160, wide-20, 410)) #一直播
    #region = image.crop((20, 120, wide-20, 300)) #冲顶
    #region = image.crop((0, 230, wide, 430))  # yy
    region = image.crop((20, 120, wide - 20, 320)) #芝士
    region.save(text_area_file)
```

此处配置截图区域，保留一行#注释掉其他行

如果文字识别出错，打开\screenshots\text_area.png查看截取区域是否正确

3）百度ORC配置一下三项

```
app_id=10714687

app_key=qM7V4pcKihGVMfUoaeaS1ykx

app_secret=4a0REeAIaCVuqct59Qd9hTe2eAGGF1ie
```

## 实现

1. 获取模拟器图像
2. 截图题区
3. 百度ORC识图（返回问题与选项）
4. 按F2搜索

## 效果演示

![pig1](/Users/NUAA_Hiro/Desktop/pig1.jpg)

共三个部分

1. 题库输出（根据问题关键词或答案查询题库）

2. 百度知道API输出（个人经验，只对部分提醒正确率较高，对于否定选择以及逻辑判断题无效）

3. 百度搜索摘要（完整句子中的信息才是有效信息）此处进行一下搜索

   > Search question
   >
   > if null search question + "key(for key in keys)"

题库输出演示

![pig2](/Users/NUAA_Hiro/Desktop/pig2.jpg)

#### 注意：彩色字体输出使用的termcolor库，目前测试只在Pycharm中能显示颜色字体

### 自动搜题脚本

- 500 Star 分享自动识别出题脚本，免人工操作
- 资助20元分享自动识别出题脚本
- 资助50代搭建全部环境

### 资助

![fig3](/Users/NUAA_Hiro/Downloads/fig3.png)
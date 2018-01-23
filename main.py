# -*- coding:utf-8 -*-


"""

    问答助手~

"""
import time
import codecs
from datetime import datetime
import win32gui
from argparse import ArgumentParser

import operator
from pyhooked import Hook, KeyboardEvent
from terminaltables import AsciiTable
from termcolor import colored

from core.crawler.query import abquery
from core.crawler.baiduzhidao import baidu_count


from core.ocr import get_text_from_image_hanwang, get_text_from_image_baidu
from core.windows import analyze_current_screen_text

import configparser

conf = configparser.ConfigParser()
conf.read("config.ini",encoding="utf8")

data_directory = conf.get('config',"data_directory")

vm_name = conf.get('config',"vm_name")

app_name = conf.get('config',"app_name")

search_engine = conf.get('config',"search_engine")

hot_key = conf.get('config',"hot_key")

enable_chrome = conf.get('config',"enable_chrome")

# ocr_engine = 'baidu'
ocr_engine = conf.get('config',"ocr_engine")

### baidu orc
app_id = conf.get('config',"app_id")
app_key = conf.get('config',"app_key")
app_secret = conf.get('config',"app_secret")

### 0 表示普通识别
### 1 表示精确识别
api_version = conf.get('config',"api_version")

### hanwang orc
hanwan_appcode = conf.get('config',"hanwan_appcode")

def pre_process_question(qus):
    """
    strip charactor and strip ?
    :param question:
    :return:

    """
    now = datetime.today()
    for char, repl in [("“", ""), ("”", ""), ("？", ""), ("《", ""), ("》", ""), ("我国", "中国"),
                       ("今天", "{0}年{1}月{2}日".format(now.year, now.month, now.day)),
                       ("今年", "{0}年".format(now.year)),
                       ("这个月", "{0}年{1}月".format(now.year, now.month))]:
        qus = qus.replace(char, repl)

    return qus
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def main():
    args = parse_args()
    timeout = args.timeout
    start = time.time()
    text_binary = analyze_current_screen_text(
        label=vm_name,
        directory=data_directory
    )
    if ocr_engine == 'baidu':
        # print("百度OCR!!!\n")
        keyword = get_text_from_image_baidu(image_data=text_binary, app_id=app_id, app_key=app_key,
                                            app_secret=app_secret, api_version=api_version, timeout=5)

        
    else:
        print("汉王 OCR\n")
        keyword = get_text_from_image_hanwang(image_data=text_binary, appcode=hanwan_appcode)

    if not keyword:
        print("Error-1 \n")
        # print("题目出现的时候按F2，我就自动帮你去搜啦~\n")
        return

    question = keyword[0:len(keyword) - 3]
    answers = keyword[len(keyword) - 3:]

    questions = "".join([e.strip("\r\n") for e in question if e])

    # 去掉题目索引
    for char, repl in [("11.", ""), ("12.", ""),("11、", ""), ("12、", ""), ("1.", ""),("2.", ""),
                       ("3.", ""),("4.", ""),("5.", ""), ("6.", ""), ("7.", ""), ("8.", ""),
                       ("9.", ""), ("10.", ""), ("1、", ""), ("2、", ""), ("3、", ""), ("4、", ""),
                       ("5、", ""), ("6、", ""), ("7、", ""), ("8、", ""),("9、", ""), ("10、", "")]:
        questions = questions.replace(char, repl)

    print("-"*72)
    print("问题: | "+questions)
    end3 = time.time()
    print("-"*50 +"{:4f} 秒".format(end3 - start)+"-"*10 )

    if len(questions) < 2:
        print("没识别出来，随机选吧!!!\n")
        return

    search_question = pre_process_question(questions)

    # ---------------题库关键词输出
    p_ans = []
    for i in range(0, 3):
        for char1, repl1 in [("A.", ""), ("B.", ""), ("C.", ""),
                             ("A、", ""), ("B、", ""), ("C、", ""),
                             ("A：", ""), ("B：", ""), ("C：", ""),
                             ("A:", ""), ("B:", ""), ("C:", "")]:
            answers[i] = answers[i].replace(char1, repl1)

        p_ans.append(answers[i])
    keys = p_ans[:]
    q_key = ""
    if (questions.find("《") != -1) & (questions.rfind("》") != -1):
        q_key = extraContext(questions, "《", "》")
    elif questions.find("\"") != -1:
        pii = questions.find("\"")
        pii1 = questions[pii + 1:].find("\"")
        if pii1 != -1:
            q_key = questions[pii + 1:pii + 1 + pii1]
        else:
            q_key = questions[pii + 1:pii + 5]
    elif questions.find("“") != -1:
        piii = questions.find("“")
        piii1 = questions[piii + 1:].find("”")
        if piii1 != -1:
            q_key = questions[piii + 1:piii + 1 + piii1]
        else:
            q_key = questions[piii + 1:piii + 5]
    elif questions.find("的")!= -1:
        q_key = questions[questions.find("的") - 2 :questions.find("的") + 2 ]
    elif questions.find("是") != -1:
        q_key = questions[questions.find("是") - 4:questions.find("是") ]
    elif questions.find("哪") != -1:
        q_key = questions[questions.find("哪") - 2:questions.find("哪") + 3]
    else:
        q_key = questions[len(questions)/2 : len(questions)/2+4]

    ansl = 0
    if keys:
        fh = codecs.open('dict\dict.txt', "r", "utf-8")
        for line in fh.readlines():
            mao = 0
            if line.find(q_key)!= -1:
                for key in keys:
                    if (mao == 0) & ( line.find(str(key))!= -1) & (len(str(key)) > 1):
                        if (len(str(key)) < 3)& ( is_number(key)):
                            break
                        print(colored(line,"blue"))
                        ansl = 1
                        mao = 1
    if ansl == 0:
        print(colored("《题库》未收录，查询失败!!!!!","red"))
    else:
        print("问题: | " + questions)
    end2 = time.time()
    print("-"*50 +"{:4f} 秒".format(end2 - start)+"-"*10 )


    # ---------------百度知道API

    summary = baidu_count(search_question, p_ans, timeout=timeout)
    summary_li = sorted(
        summary.items(), key=operator.itemgetter(1), reverse=True)
    data = [("《选项关联度》", "")]
    for a, w in summary_li:
        data.append((a, w))
    table = AsciiTable(data)
    print(table.table)
    end1 = time.time()
    print("-" * 50 + "{:4f} 秒".format(end1 - start) + "-" * 10)
    print("-------百度查询摘要-------")

    abquery(questions, p_ans,q_key)

    end = time.time()
    print("-" * 50 + "{:4f} 秒".format(end - start) + "-" * 10)

def handle_events(args):
    if isinstance(args, KeyboardEvent):
        if args.current_key == hot_key and args.event_type == 'key down':
            print("Searching......")
            main()
        elif args.current_key == 'Q' and args.event_type == 'key down':
            hk.stop()
            print('退出啦~')

def parse_args():
    parser = ArgumentParser(description="Hiro_QA_Helper")
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=5,
        help="default http request timeout"
    )
    return parser.parse_args()

def extraContext(str,f1,f2):
    left = str.find(f1)
    right = str.rfind(f2)
    return str[left+1:right]

if __name__ == "__main__":

   # multiprocessing.freeze_support()
    hld = win32gui.FindWindow(None, vm_name)
    if hld > 0:
        print('Hiro答题助手启动，请打开config.ini配置ORC key 与vm_name\n'+
              '识别出错时请打开\screenshots\text_area.png查看并修改windows.py中的截取参数！\n\n'
              +'自动搜索，请注意看题')
        hk = Hook()
        hk.handler = handle_events
        hk.hook()
    else:
        print('咦，你没打开' + vm_name + '吧!请打开' + vm_name + '并重启下start.bat')

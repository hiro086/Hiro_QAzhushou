# coding:utf8

from urllib.parse import quote
from termcolor import colored


from core.crawler import html_tools as To



def abquery(qus, ans, key):
    '''
    对百度、Bing 的搜索摘要进行答案的检索
    需要加问句分类接口）
    '''
    flag = 0
    # 抓取百度前10条的摘要
    soup_baidu = To.get_html_baidu('https://www.baidu.com/s?wd=' + quote(qus))

    for i in range(1, 10):
        if soup_baidu == None:
            break
        results = soup_baidu.find(id=i)
        if results == None:
            break
        mao = 0
        for a in ans:
            pi = results.get_text().find(a[:len(a)-1])
            if (pi != -1) & (mao == 0):
                rt = results.get_text().strip().replace('\n', '')
                if rt[:pi].find(key) != -1:
                    pj = rt[:pi].find(key)
                    print(rt[:pj]+ colored(key, "red") +rt[pj+ len(key):pi] + colored(a, "red") + rt[pi + len(a):] + "\n")
                elif rt[pi+len(a)+1:].find(key) != -1:
                    pj1 = rt[pi+len(a)+1:].find(key)
                    print(rt[:pi]+colored(a,"red")+rt[pi+len(a)+1:pj1]+colored(key,"red")+rt[pj1 + len(key) + 1:]+"\n")
                mao = 1
                flag = 1

    if flag == 0:
        for a in ans:
            soup_baidu_qa = To.get_html_baidu('https://www.baidu.com/s?wd=' + quote(qus+"  \""+a+"\""))
            for i in range(1, 3):
                if soup_baidu_qa == None:
                    break
                results2 = soup_baidu_qa.find(id=i)
                if results2 == None:
                    break
                pi = results2.get_text().find(a[:len(a)-1])
                rt = results2.get_text().strip().replace('\n', '')
                print(rt[pi-20:pi] + colored(a, "red") + rt[pi + len(a) + 1:pi + len(a) + 20] + "\n")

                #if count <2 直接执行查询



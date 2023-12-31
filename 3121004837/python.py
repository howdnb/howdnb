from simhash import Simhash
import jieba
import sys
import re

#调用line_profiler库对函数进行性能分析
from line_profiler_pycharm import profile

# 获取文件内容
def get_file(path):
    with open(path,'r',encoding="UTF-8") as f:
       line = f.readline()
       str=""
       while line:
           str=str+line
           line=f.readline()
    return str

#将获取到的文本内容使用jieba库进行分词并进行过滤
def cut(str):
    str=jieba.cut(str)
    result=[]
    for flag in str:     #将文本中除英文和中文外的其它过滤掉
        if(re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]",flag)):
            result.append(flag)
        else:
            pass
    return result

#通过使用simhash库计算两个文本相似度
def calculate_similarity(text1,text2):
    a_simhash = Simhash(text1)
    b_simhash = Simhash(text2)
    max_hashbit = max(len(bin(a_simhash.value)), len(bin(b_simhash.value)))
    # 汉明距离
    distince = a_simhash.distance(b_simhash)
    print(distince)
    similar = 1 - distince / max_hashbit
    return similar

#从命令行中启动
if __name__=='__main__':
    if len(sys.argv)!=4:
        print("传入参数数量错误！")
        exit()

    #使用sys库获取命令行参数
    path1=sys.argv[1]
    path2=sys.argv[2]
    path3=sys.argv[3]

    #调用函数获取文件内容
    str1=get_file(path1)
    str2=get_file(path2)

    #调用函数过滤内容并分词
    text1=cut(str1)
    text2=cut(str2)

    #调用函数计算余弦相似度
    similarity=calculate_similarity(text1,text2)
    print(f"文章相似度为：%.2f"%similarity)

    #将结果保存在指定的输出文件中
    with open(path3,'w',encoding="UTF-8") as f:
        f.write("文章相似度为：%.2f"%similarity)

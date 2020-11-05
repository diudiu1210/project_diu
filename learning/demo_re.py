
"""
正则表达式是一种通用的字符串匹配技术，是不会因为编程语言不一样而发生变化的
想要查找某种特征的，具有一定规则的字符串，都是可以尝试使用正则表达式。
jsonpath，xpath解析相关

匹配的方式：只是python当中的封装
-match
-search
-findall
todo:正则表达式中，不要随意打空格  .表示任意字符，*表示次数
"""
import re
# re_pattern=r"abc"
# match表示：从开始位置进行匹配,如果开始位置没有就打印none
# res=re.match(re_pattern,"djfkdjfdabckdjdjdabc")
# print(res)

# search：表示全文匹配,当找到第一个符合的后面的就不会再搜索了，打印<re.Match object; span=(8, 11), match='abc'>
# res=re.search(re_pattern,"djfkdjfdabckdjdjdabc")
# print(res)

# findall ，全部匹配,把所有匹配到的结果通过列表存起来
# res=re.findall(re_pattern,"djfkdjfdabckdjdjdabc")
# print(res)

# [abc] ,匹配中括号中的任意一个字符，不需要abc连着，只要碰到abc当中任意字符就打印
# re_pattern=r"[abc]"
# res=re.findall(re_pattern,"adjfkdjfdabckdjdjdabc")
# print(res)

# . 点是匹配任意的一个字符串，除了\n 是换行符,如果里面有\n会自动跳过
# re_pattern=r"."
# res=re.findall(re_pattern,"adjfkdjfdabckdjdjdabc")
# print(res)

# \d 匹配数字字符，等价于[0-9] 如果是\D就的匹配非数字
# re_pattern=r"[0-9]"
# re_pattern=r"\d"
# res=re.findall(re_pattern,"adjfk11djfdabckdjdjdabc23")
# print(res)

# \w 匹配字母，数字，下划线。等价于[A-Za-z0-9_]  如果是\W就是匹配非。。
# re_pattern=r"[A-Za-z0-9_]"
# res=re.findall(re_pattern,"a_djf$k11djfdabckdjdjdabc23")
# print(res)

#匹配花括号当中的数字次数，匹配2个符合规则的w，要组合才可以，如果中间断开了就会丢掉
# re_pattern=r"\w{2}"
# res=re.findall(re_pattern,"a_djf$k11djfdabckdjdjdabc23")
# print(res)

#{2，}匹配至少2次  ['113666', '23']  加入逗号属于贪婪匹配
# re_pattern=r"\d{2,}"
# res=re.findall(re_pattern,"a_djf$k113666djfdabckdjdjdabc23")
# print(res)
# {，2}匹配最多2次，包括0次 1次和2次，如果遇到非数字就会打印空格
# re_pattern=r"\d{,2}"
# res=re.findall(re_pattern,"a_djf$k113666djfdabckdjdjdabc23")
# print(res)

# {2,4}匹配2到4 最少2次，最多4次，其他都不会匹配会丢掉  ['1136', '66', '23']
# re_pattern=r"\d{2,4}"
# res=re.findall(re_pattern,"a1_djf$k113666djfdabckdjdjdabc23")
# print(res)

# 如何匹配手机号码
# re_pattern=r"1[3589]\d{9}"
# res=re.findall(re_pattern,"a1_djf$k113466667777djfdabckdjdjdabc23")
# print(res)

# *匹配0次和任意次  贪婪匹配 通配符 如果没有数字就是0次 会打印空字符串
# re_pattern=r"\d*"
# res=re.findall(re_pattern,"a1_djf$k113466667777djfdabckdjdjdabc23")
# print(res)

# +匹配1次或者任意次  ['1', '113466667777', '23']  先要有数字才行，最好要有1个
# re_pattern=r"\d+"
# res=re.findall(re_pattern,"a1_djf$k113466667777djfdabckdjdjdabc23")
# print(res)

# 匹配任意字符，但必须是2个，第一个必须是数字后面的一个随意  ['1_', '2j', '11', '34', '66', '66', '77', '77', '23']
# re_pattern=r"\d."
# res=re.findall(re_pattern,"a1_d2jf$k113466667777djfdabckdjdjdabc23")
# print(res)

#匹配0次或者1次，非贪婪模式,遇到非数字就打印空字符串，数字是单个打印
# re_pattern=r"\d?"
# res=re.findall(re_pattern,"a1_d2jf$k113466667777djfdabckdjdjdabc23")
# print(res)

# ^ 开头的边界,匹配以数字开头，  r"\d$" 匹配以数字结尾
# re_pattern=r"^\d"
# res=re.findall(re_pattern,"a1_d2jf$k113466667777djfdabckdjdjdabc23")
# print(res)


# re_pattern=r"#.*?#"
# mystr='{"member_id":"#member_id#","load_id":"#load_id#","token":"#token#"}'
# res=re.findall(re_pattern,mystr)
# print(res)

# 组 () #号就会被去掉
# re_pattern=r"#(.*?)#"
# mystr='{"member_id":"#member_id#","load_id":"#load_id#","token":"#token#"}'
# res=re.findall(re_pattern,mystr)
# print(res)

# re.sub(正则表达式，替换的新内容，原字符，替换的次数) 字符串不支持修改，需要用一个新的变量去接收
# new_str=re.sub(re_pattern,"me23",mystr,1)
# print(new_str)
#
# new_str=re.sub(re_pattern,"ld123",new_str,1)
# print(new_str)
#
# new_str=re.sub(re_pattern,"token123",new_str,1)
# print(new_str)

# re.search(正则表达式，原字符).group(1) 需要用search，因为是一次搜索一个符合的
re_pattern = r"#(.*?)#"
mystr='{"member_id":"#member_id#","load_id":"#load_id#","token":"#token#"}'
res=re.search(re_pattern,mystr).group(1)
print(res)

class Context:
    member_id=999
    loan_id=888
    token="ddddd"


def replace_label(target):
    """while循环"""
    re_pattern = r"#(.*?)#"
    while re.findall(re_pattern,target):
    # 如果能够匹配就完成替换
        key=re.search(re_pattern,target).group(1)
        target=re.sub(re_pattern,str(getattr(Context,key)),target,1)
    return target

if __name__ == '__main__':
    mystr = '{"member_id":"#member_id#","loan_id":"#loan_id#","token":"#token#"}'
    print(replace_label(mystr))

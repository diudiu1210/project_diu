
# 随机生成手机号码
import random


def get_mobile():
    # 随机生成一个手机号码，1[3,5,6,7,8]+9
    mobie="1"+random.choice(["3","5","6","7","8"])
    for i in range(9):
        sum=random.randint(0,9)
        mobie+=str(sum)
    return mobie

if __name__ == '__main__':
    print(get_mobile())

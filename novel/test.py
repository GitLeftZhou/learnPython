def num2ch(b_num: int):
    if b_num == 0:
        return ""
    elif b_num == 1:
        return "一"
    elif b_num == 2:
        return "二"
    elif b_num == 3:
        return "三"
    elif b_num == 4:
        return "四"
    elif b_num == 5:
        return "五"
    elif b_num == 6:
        return "六"
    elif b_num == 7:
        return "七"
    elif b_num == 8:
        return "八"
    elif b_num == 9:
        return "九"


def num_weight(b_num: int):
    if b_num == 0:
        return ""
    elif b_num == 1:
        return "十"
    elif b_num == 2:
        return "百"
    elif b_num == 3:
        return "千"
    elif b_num == 4:
        return "万"
    elif b_num == 8:
        return "亿"
    return num_weight(b_num % 4)


num = "10000000"
idx = 0
return_str = ""
for i in range(len(num) - 1, -1, -1):
    ni = num[i]
    # print(ni)
    return_str = num2ch(int(ni)) + num_weight(idx) + return_str

# print(return_str)
    idx += 1
print(return_str)

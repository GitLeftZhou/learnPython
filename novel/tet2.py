import re
a = "第二-五章张三李四王五说"

print(re.sub(r"第.*章", "", a))
import re

with open(r"E:\myfile\pythonfile\rsl_che.sql", 'w', encoding='utf-8') as fw:
    for line_str_all in open(r"E:\myfile\pythonfile\src.txt", encoding="utf-8"):
        txt = "insert into a value ('"
        line_strs = line_str_all.replace("\t", "").split("aa")
        txt += (line_strs[0].strip() + "',")
        line_str = line_strs[1]
        if "省" in line_str:
            sheng = line_str.split("省")
            txt += ("'" + sheng[0] + "',")
            if "市" in sheng[1]:
                shi = sheng[1].split("市")
                txt += ("'" + shi[0] + "',")
            elif "州" in sheng[1]:
                shi = sheng[1].split("州")
                txt += ("'" + shi[0] + "',")
            else:
                txt += ("'" + "" + "',")
        else:
            if "市" in line_str:
                shi = line_str.split("市")
                txt += ("'" + "'," + "'" + shi[0] + "',")

        phoneNumRegex = re.compile(r'\d{11}')
        phones = phoneNumRegex.findall(line_str)
        for phone in phones:
            txt2 = txt + "'" + phone + "')"
            if len(txt) > 0:
                print(txt2)
                fw.write(txt2)  # 追加内容
                fw.write('\n')  # 换行

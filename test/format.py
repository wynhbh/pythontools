
dic = []
with open('coca') as fr:
    for l in fr:
        s = l.strip().split(' ')
        dic.append(s[1])

with open('words7042', 'w') as fw:
    for i in dic:
        st = "<item>    <word> " + i + "</word><progress>-1</progress></item>"
        fw.write(st + '\n')

dic = []
c = {}
with open('coca20000.txt') as fr:
    for l in fr:
        s = l.strip().split(' ')
        if len(s) > 0 and s[0].isdigit():
            if s[1] not in dic:
                dic.append(s[1])

            if s[0] in c:
                c[s[1]] += 1
            else:
                c[s[1]] = 1

ls = sorted(c.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

#print ls[:10]
#ds = set(dic)
#print len(ds)
#print list(ds)[:10]

with open('words20000', 'w') as fw:
    for i in dic:
        st = "<item>    <word> " + i + "</word><progress>-1</progress></item>"
        fw.write(st + '\n')

'''
with open('words7042', 'w') as fw:
    for i in dic:
        st = "<item>    <word> " + i + "</word><progress>-1</progress></item>"
        fw.write(st + '\n')
'''
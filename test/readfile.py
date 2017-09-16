
list = []
with open('COCA7000.txt') as fr:
    i = 1
    for line in fr:
        l = line.strip().split(' ')
        if l[0].isdigit() and int(l[0]) == i:
            list.append(l)
            i += 1
        else:
            continue

with open('coca', 'w') as fw:
    for i in list:
        fw.write(i[0]+' '+i[1]+'\n')

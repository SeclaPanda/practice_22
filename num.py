import re

fil = '/Users/alex_secla/Documents/GitHub/practice_22/groups/uis_311.txt'
num = []
with open (fil, 'r') as f:
    for inp_str in f:
        buf = re.findall(r'\d+', inp_str) 
        num += buf
for i in num:
    for i in num:
        if (len(i) > 5):
            continue
        else:
            num.remove(i)
print(num)


#307354251 - None
str = '95,251|206,217|254,127'
print(str)

for index in str.split('|'):
    # print(index)
    x = index.split(',')[0]
    y = index.split(',')[1]
    print(x, y)
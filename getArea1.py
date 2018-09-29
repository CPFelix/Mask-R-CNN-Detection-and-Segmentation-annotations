# -*-coding=utf8-*-

def checkio(data):
    '''输入多点的个坐标，返回这些点构成的凸多边形的面积'''
    sort_x = sorted(list(data))  # 按横坐标排序
    copy_sort_x = sort_x[0:]
    length = len(copy_sort_x)
    top = bottom = sort_x[0]
    for coor in sort_x:
        if top[1] < coor[1]:
            top = coor
        if bottom[1] > coor[1]:
            bottom = coor
    middle = (top[1] + bottom[1]) / 2.0  # 图形最高点与最低点中点的y值

    anticlock_sort = []  # 逆时针存放各点坐标
    mysum = 0
    for i in range(0, length):
        if copy_sort_x[i][1] <= middle:
            # 移除下半部分的点
            sort_x.remove(copy_sort_x[i])
            # 将下半部分的点添加进去
            anticlock_sort.append(copy_sort_x[i])

    # 生成最终的逆时针坐标点
    anticlock_sort.extend(reversed(sort_x))

    '''根据公式 S = 1/2×((X1*Y2-X2*Y1)+...+(Xi*Yi+1-Xi+1*Yi)+... +(Xn*Y1-X1*Yn)) q求面积'''
    for i in range(length - 1):
        mysum += (anticlock_sort[i][0] * anticlock_sort[i + 1][1]
                  - anticlock_sort[i][1] * anticlock_sort[i + 1][0])

    mysum = mysum + anticlock_sort[-1][0] * anticlock_sort[0][1]
    -anticlock_sort[-1][1] * anticlock_sort[0][0]


    mysum = mysum / 2.0  # 精确输出

    return mysum

if __name__ == '__main__':
    data = input('Input coordinate>>')
    data = list(data)
    print checkio(data)
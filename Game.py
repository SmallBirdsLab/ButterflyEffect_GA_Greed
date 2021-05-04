'''这里主要是游戏功能的实现'''
def star(map, index, operands): # 输入地图map，表的位置index，玩家操作operands，返回分数
    thisMap = [l[:] for l in map]  # 不能修改 Map 里的原地图，所以先复制
    score = 0
    for operand in operands:  # 依次读取玩家点击的指针标号

        # r,c表示下一个转动的指针在第r行c列
        r = index[int(operand)][0]
        c = index[int(operand)][1]
        
        while( thisMap[r][c] != -1 ): # 当下一个转动的指针不在界外时，产生蝴蝶效应
            # 改变指针方向，分数增加90
            thisMap[r][c] = (thisMap[r][c] + 1) % 4
            score += 90

            # 顺着该指针所指方向改变r，c，得到下一个转动的指针位置
            if(thisMap[r][c] == 0):   # 指向上
                r -= 1
            elif(thisMap[r][c] == 1): # 指向右
                c += 1
            elif(thisMap[r][c] == 2): # 指向下
                r += 1
            else:                     # 指向左
                c -= 1

    return score
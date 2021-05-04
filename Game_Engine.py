import Game
import Map
import numpy as np
from sko.GA import GA

level = 10000                                # 关卡过关分数
clickNum = 10                                # 玩家点击次数
size_pop = 24 * clickNum                     # 种群数量
max_iter = 2000                              # 最大迭代次数
tryNum = 100                                 # 遗传算法运行次数
fPath = "运行结果/关卡" + str(level) + ".txt" # 得到解存入的文件路径
index = eval("Map.index" + str(level))
map = eval("Map.map" + str(level))
pNum = len(index)                            # 指针的数量，即指针标号的上界

def demo_func(p):  # 计算p的适应度，这个遗传算法库适应度越小越易存活，而十步万度要求最高分，所以可以取倒数或作差
    return 1 / (Game.star(map, index, p) - 1350)     # 取游戏得分的倒数
    # return abs(11090 - (Game.star(map, index, p))) # 作差
    # return Game.star(fly, p)                       # 求得分最小值

def gaRun():  # 调用遗传算法库得到解
    ga = GA(func=demo_func, n_dim=clickNum, size_pop=size_pop, max_iter=max_iter,
            lb=[0]*clickNum, ub=[pNum-1]*clickNum, precision=[1]*clickNum)
    return ga.run()

'''贪心'''
def greedNext(now):          # 当前是now，返回当前下一步的最优选择
    gScore = 0
    for next in range(pNum): # 遍历下一步的所有情况，t: try or temp
        tOperat = now + [next]
        tScore = Game.star(map, index, tOperat)
        # print("if click ", next, " then score: ", tScore)
        if(tScore > gScore): # 选出得分最高的组合
            gScore = tScore
            best_next = next
    # print("so click: ", best_next)
    return [best_next]

def greedNext4(now):          # 当前是now，返回当前后四步的最优选择
    gScore = 0
    for next1 in range(pNum): # 遍历后面第四步所有情况
        for next2 in range(pNum):         
            for next3 in range(pNum):     
                for next4 in range(pNum): 
                    tOperat = now + [next1, next2, next3, next4]
                    tScore = Game.star(map, index, tOperat)
                    # print("if click ", next1, ",", next2, ",", next3, ",", next4, " then score: ", tScore)
                    if(tScore > gScore): # 选出得分最高的组合
                        gScore = tScore
                        best_next = [next1, next2, next3, next4]
    # print("so click: ", best_next)
    return best_next

gOperat = []                      # 存贪心所得的解
for i in range(clickNum):         # 添加clickNum个元素
    gOperat += greedNext(gOperat) # 每次添加局部最优解
print('贪心一步得到最优解: ', gOperat, ' score:  ', Game.star(map, index, gOperat), '\n')

'''运行遗传算法tryNum次得到的解按格式写入文件并去重'''
def writeWith(operat, score):        # 将得分为score的操作数组（列表存储）operat写入fPath
    with open(fPath, 'a') as fa:     # 打开存储文件（从末尾开始写），文件不存在就创建
        with open(fPath, 'r') as fr: # 打开存储文件（只读）

            line = fr.readline()                 # 读到的第一行是分数
            if((not line) or int(line) < score): # 如果第一行为空或分数太小，则更新最高分，重新写
                with open(fPath, 'w') as fw:     # 打开存储文件（重新开始写）
                    print('更优，更新最高分: ', score)
                    fw.write(str(score)+'\n'+str(operat)+'\n')

            elif(int(line) == score): # 分数相同，可以写入，但要判断是否与已得的解重复

                repeat = False        # 判断是否重复，默认为否
                line = fr.readline() 

                while line:           # 默认文件都按规定的格式存储
                    # 读到的字符串转换为整型列表（去除其他成分），才能与整型列表operat比较是否重复
                    line = [int(e) for e in line.replace('[', '').replace(']', '').replace(',', '').replace(' ', '').replace('\n', '')]
                    if(operat == line):
                        print('已存在，不写入')
                        repeat = True
                        break
                    line = fr.readline()

                if(not repeat):
                    print('与已有解没重复，写入 ' + fPath)
                    fa.write(str(operat)+'\n')

            else:
                print('分数低，不写入')

for i in range(tryNum):
    best_operat, best_func = gaRun()
    gaOperat = [int(ii) for ii in best_operat] # 解转换为整型列表

    # 删掉最后四步，再遍历最后四步所有情况选择最优解
    gaScore = Game.star(map, index, gaOperat)
    print("\n遗传算法第", i+1, "次得到解: ", gaOperat, ' score: ', gaScore)
    
    greedOperat = gaOperat[:-4]
    greedOperat += greedNext4(greedOperat)
    greedScore = Game.star(map, index, greedOperat)
    print("最后四步重新贪心选择后:", greedOperat, ' score: ', greedScore)

    # 将解写入文件
    print("遗传贪心的解 ", end='')
    writeWith(greedOperat, greedScore)
    if(gaScore == greedScore): # gaScore不可能比greedScore大，但相等时，可以尝试把gaOperat加进去
        print("遗传算法的解 ", end='')
        writeWith(gaOperat, gaScore)

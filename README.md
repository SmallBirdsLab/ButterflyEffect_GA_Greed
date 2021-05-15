成功运行遗传算法得**先安装python的GA算法开发包scikit-opt**。 ！！！  
[详细过程见我的博客](https://blog.csdn.net/ScienceLimit/article/details/116108469)
# 各关卡的解
各个关卡运算出的最高解存储在 “运行结果” 的文件的txt文档里。
# 增加/删除/修改关卡地图
`Map.py用于存储地图信息`，可以自己diy关卡，只用修改Map.py文件。  
因为20000关之后指针初始状态就随机了，所以没有存入地图，但自己可以根据指针状态diy地图，只要原地图指针方向改一下。

# 开始运行遗传算法 
运行Game_Engine.py即可，引入了Map.py和Game.py，主要是调用遗传算法玩游戏，并对运行结果重新贪心，再写入存储文件。  
`Game.py主要是游戏功能的实现`，输入地图信息和操作数组即可返回相应分数。  
如图红框是对遗传算法的解后四步重新贪心选择，再将运行结果存入文件并去重。
![image](https://gitee.com/worldlab/ButterflyEffect_GA_Greed/raw/main/%E5%9B%BE/%E9%81%97%E4%BC%A0%E8%B4%AA%E5%BF%83%E8%BF%90%E7%AE%97%E7%BB%93%E6%9E%9C.png)

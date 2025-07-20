import random
import pandas
import copy
import matplotlib.pyplot as plt

#基因染色體
class Gene:  
    def __init__(self):
        self.take=[]    #是否裝該編號的物品
        self.gene_weight=0  #背包內總重量
        self.gene_price=0 #背包內總價值
        for i in range(0, 30):
            if(random.randint(0,9)<=6): #隨機產生初始染色體是否拿取某物品(拿取機率30%)(註記:討論可以寫若五五分拿到爆的機率太高了)
                self.take.append(0) #不拿該物品
            else:
                self.take.append(1) #拿該物品
        self.calculate()   
            
    #突變
    def mutation(self): 
        location=random.randint(0,29)   #突變位置  
        self.take[location]=(self.take[location]+1)%2   #改變拿或不拿 
    
    #計算總重量與總價值   
    def calculate(self):    
        self.gene_price=0
        self.gene_weight=0  #歸零
        for i in range(0, 30):
            if self.take[i]==1: #判斷是否拿取該物品
                self.gene_weight+=all_items[i].weight      #總重量加上物品重量
                self.gene_price+=all_items[i].price   #總價值加上物品價值
                
#物品數值
class Item: 
    def __init__(self, index):
        self.name=data.iat[index, 1]    #讀入物品名稱
        self.weight=data.iat[index, 2] #讀入物品重量
        self.price=data.iat[index, 3]  #讀入物品價值

        
#主程式開始--------------------------------------------------------------------------
data=pandas.read_excel("0-1背包問題參數.xlsx")    #讀入excel檔
max_weight=data.iat[0,4]     #背包重量上限
all_items=[]    #所有物品數值
gene_pool=[]    #基因池
next_pool=[]   #下一代的基因池
total_price=0   #基因池內總價值
ans=0   #最終答案(作圖用得到)
running_times=0 #跑第幾次(作圖用得到)
generation=50000    #目標迭代次數
price=[]#圖的list
price2=[]
time=[]#圖的list
time2=[]
for i in range(0, 30):  
    all_items.append(Item(i))   #建立物品數值陣列
for i in range(0, 20):
    gene_pool.append(Gene())   #建立初始染色體
    while gene_pool[i].gene_weight>max_weight:   #判斷初始染色體是否超重
        gene_pool.pop(i)    #刪除超重染色體
        gene_pool.append(Gene())   #重新產生新染色體
    total_price+=gene_pool[i].gene_price   #計算初始基因池內總價值 
        
#開始迭代(當迭代次數達到設定時停止)
while running_times<generation:
    running_times+=1
    #每個世代交配10次
    for i in range(0, 10):  
        #根據染色體價值比例抽取兩個相異的染色體
        random_num=random.randint(1, total_price)   #產生一個介於1到總價值的隨機數
        for j in gene_pool:
            random_num-=j.gene_price   #將隨機數逐一減去總價值(分母) 直到<=0
            if random_num<=0:
                gene_a=j    #選出該染色體a
                break
        gene_b=gene_a   #先把染色體b設成跟染色體a同一條
        #確保兩條染色體相異
        while(gene_b==gene_a):
            random_num=random.randint(1, total_price)   
            for j in gene_pool:
                random_num-=j.gene_price  
                if random_num<=0:
                    gene_b=j    #選出該染色體b
                    break
        gene_a=copy.deepcopy(gene_a)    #複製一個一樣的染色體                                (原本的等於是指到同一個染色體 複製後原本跟現在的就獨立了)
        gene_b=copy.deepcopy(gene_b)    #複製
        #染色體交配
        swap_point=random.randint(0, 29)    #隨機選出兩染色體單點交配的起始點
        gene_a.take[swap_point:30], gene_b.take[swap_point:30]=gene_b.take[swap_point:30], gene_a.take[swap_point:30]   #單點交配
        #突變
        if random.randint(0, 9)==0:    #10%機率a發生突變
            gene_a.mutation()   #呼叫突變函式 
        if random.randint(0, 9)==0:    #10%機率b發生突變
            gene_b.mutation()   #呼叫突變函式
        #放進下一代基因庫
        gene_a.calculate()  #計算重量跟價值
        if gene_a.gene_weight>max_weight:
            gene_a.gene_price=0 #如果超重就把價值歸零
        next_pool.append(gene_a)    #把新的染色體放進下一代的基因庫
        gene_b.calculate()  #計算重量跟價值
        if gene_b.gene_weight>max_weight:
            gene_b.gene_price=0 #如果超重就把價值歸零
        next_pool.append(gene_b)    #把新的染色體放進下一代的基因庫
    #世代交替
    gene_pool=next_pool;    #把下一代的基因庫丟回來 原本的染色體們就用不到了
    gene_pool.sort(key=lambda x: x.gene_price, reverse=True)    #排序(方便找出最大值)
    next_pool=[]    #清空下一代基因庫
    total_price=0   #歸零總價值重新計算
    for i in gene_pool:
        total_price+=i.gene_price   #計算基因池內總價值
    #如果新的總價值比原有的好就更新並輸出(或作圖)
    price2.append(gene_pool[0].gene_price)#畫圖用
    time2.append(running_times)#畫圖用
    if ans<gene_pool[0].gene_price:
        ans=gene_pool[0].gene_price
        print("price:", ans, "gen:", running_times)
    if running_times%10000==0:
        print("generation:" , running_times)
    price.append(ans)#畫圖用
    time.append(running_times)#畫圖用
#畫圖
plt.figure(figsize=(20, 4))  # 設置畫布大小
plt.plot(time,price, color='blue')
plt.title('best generation')
plt.xlabel('times')
plt.ylabel('price')
plt.grid(True)  # 添加網格線
plt.show()

plt.figure(figsize=(20, 4))  # 設置畫布大小
plt.plot(time2, price2, color='green')
plt.title('every generation')
plt.xlabel('times')
plt.ylabel('price')
plt.grid(True)  # 添加網格線
plt.show()





    


        
            
            


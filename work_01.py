import random

answer = random.randint(1,100)
#random_n = 7
for i in range(5):
    cnt = cnt + 1
    input_line = int(input("1~100までの数"))
    print("入力された値",input_line)
    if answer == int(input_line):
        print("正解")
        result = True
        break
    else:
        print("不正解")
        if input_line < answer:
            if answer - input_line > 10:
                print("もっと大きい")
            else:
                print("もっと小さい数字ですが、だいぶ近い")   

while True:
    result = ()              
    
    if result:
        print("ゲームに勝ちました！あなたは{cnt}回目で正解しました") 
    else:
        print("ゲームに負けました。正解は{answer}")   

    ans = input("もう一度やりますか？(yes/no):")

    if ans == "yes":
        print("お疲れ")
        break


    print("正解の値",answer)

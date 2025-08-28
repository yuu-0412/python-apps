import time
import random
def reaction_test():
    t = random.uniform(5,15)
    time.sleep(t)
    print("押す")
    start_time = time.time()
    input()
    end_time = time.time()
    
    s = end_time - start_time
    if s < 0.01:
        print("早すぎ")
    else:
        print(f"{s:.4}秒") 

 

  
    
def ask_yes_no(prompt="もう一度やりますか？(yes/no):"):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ('yes','y'):
            return True
        if answer in ('no','n'):
            return False
        print("yesかnoで答えてください。")

def main():
    print("==== 反応速度テスト====")
    while True:
        reaction_test()
        if not ask_yes_no():
            print("お疲れ様でした！")
            break
if __name__ =="__main__":
    main()



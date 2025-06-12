import time
import random

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
    



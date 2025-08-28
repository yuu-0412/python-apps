import random
import mysql.connector

# MySQLに接続
conn = mysql.connector.connect(
    host="localhost",
    user="root",         # あなたのユーザー名
    password="yuka0227", # rootのパスワード
    database="work1db"   # データベース名
)
cur = conn.cursor()

while True:
    answer = random.randint(1, 100)
    result = False
    cnt = 0
    guesses = []

    for i in range(5):
        cnt += 1
        input_line = int(input("1から100の数字を入力してください: "))
        guesses.append(input_line)

        if input_line == answer:
            print("正解です！")
            result = True
            break
        else:
            print("不正解です。")
            if input_line < answer:
                if answer - input_line > 10:
                    print("10以上大きいです")
                else:
                    print("もっと大きい数字ですが、だいぶ近いです")
            else:
                if input_line - answer > 10:
                    print("10以上小さいです")
                else:
                    print("もっと小さい数字ですが、だいぶ近いです")

    if result:
        print(f"ゲームに勝ちました！ あなたは{cnt}回目で正解しました。")
        game_result = "win"
    else:
        print(f"ゲームに負けました。正解は{answer}でした。")
        game_result = "lose"

    # データベースに保存
    cur.execute('''
        INSERT INTO work1_results (answer, attempts, result, guesses)
        VALUES (%s, %s, %s, %s)
    ''', (answer, cnt, game_result, ",".join(map(str, guesses))))
    conn.commit()

    ans = input("もう一度やりますか？(yes/no): ")
    if ans != "yes":
        print("おつかれさまでした！")
        break

cur.close()
conn.close()

#!/usr/bin/env python3
import time
import random
import datetime
import mysql.connector
from mysql.connector import Error

# --- MySQL 接続情報（実際の値に書き換えてください） ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yuka0227",
    "database": "work4_db"
}

# --- ゲーム本体（反応速度テスト） ---
def reaction_test():
    t = random.uniform(5, 15)  # ランダム待機（秒）
    time.sleep(t)

    print("押す！　Enterキーを押してください")
    start_time = time.time()
    input()  # ユーザーの Enter を待つ
    end_time = time.time()

    re_time = end_time - start_time

    if re_time < 0.01:
        print("早すぎます（無効）")
        return None, None
    else:
        print(f"速度は {re_time:.4f} 秒")
        # started_at を DATETIME 型で保存するために datetime オブジェクトを作る
        started_at = datetime.datetime.fromtimestamp(start_time)
        return re_time, started_at

def ask_yes_no(prompt="もう一回やりますか？ (y/n): "):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes", "はい"):
            return True
        if ans in ("n", "no", "いいえ"):
            return False
        print("y/yes/はい または n/no/いいえ で答えてください。")

# --- DB：テーブル作成・保存・読み出し ---
def ensure_table_exists(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reaction_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            record_time DOUBLE NOT NULL,
            started_at DATETIME NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')

def insert_result(cur, conn, record_time, started_at):
    sql = 'INSERT INTO reaction_results (record_time, started_at) VALUES (%s, %s)'
    cur.execute(sql, (record_time, started_at))
    conn.commit()

def get_last_record(cur):
    cur.execute('SELECT record_time, started_at FROM reaction_results ORDER BY started_at DESC LIMIT 1')
    return cur.fetchone()  # None または (record_time, started_at)

def main():
    # DB接続
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
    except Error as e:
        print("DB接続エラー:", e)
        return

    # テーブルがなければ作る
    ensure_table_exists(cur)

    # 起動時に前回の記録を表示
    last = get_last_record(cur)
    if last:
        last_time, last_started = last
        print(f"前回の記録: {last_time:.4f} 秒（{last_started}）")
    else:
        print("前回の記録はありません。")

    # メインループ
    best_time = None
    while True:
        record_time, started_at = reaction_test()
        if record_time is not None:
            # 保存
            try:
                insert_result(cur, conn, record_time, started_at)
                print("結果をデータベースに保存しました。")
            except Error as e:
                print("結果の保存に失敗しました:", e)

            # 今回がベストかチェック（任意）
            if best_time is None or record_time < best_time:
                best_time = record_time
                print(f"更新！ 今のベストは {best_time:.4f} 秒です。")

        # 続けるか確認
        if not ask_yes_no():
            if best_time is not None:
                print(f"セッションのベスト: {best_time:.4f} 秒")
            print("終了します。おつかれさまでした！")
            break

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
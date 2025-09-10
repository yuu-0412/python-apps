import random
import unicodedata
import os
from datetime import datetime

# スコア保存用ファイル名
score_file = "tiikawa_score.txt"
max_score = 3  # 最大スコア

# ===== キャラと手 =====
characters2 = ["でかい鳥", "悪夢のゾウ", "じゃんけんまん", "醤油ダコ"]
hands = ["グー", "チョキ", "パー"]

# ===== クイズとヒント =====
quiz = [
    {"q": "ちいかわは何回目で草むしり検定に合格した？", "a": ["３回目", "3"], "hint": "○度目の正直！"},
    {"q": "ハチワレの趣味は？", "a": ["カメラ", "かめら"], "hint": "写真を撮るのが好き！"},
    {"q": "うさぎの口癖は？", "a": ["ウラ", "ヤハ", "ハァ？", "うら", "やは", "はぁ？"], "hint": "叫び声っぽい言葉！"},
    {"q": "くりまんじゅうが好きな飲み物は？", "a": ["酒", "お酒", "ビール"], "hint": "大人が飲むあれ！"},
    {"q": "モモンガの性格は？", "a": ["かまちょ", "かまちょな性格", "かまってちゃん"], "hint": "いつも構ってほしい！"},
    {"q": "ラッコが好きなコーヒーの種類は？", "a": ["ウインナーコーヒー"], "hint": "クリームが乗った甘いコーヒー！"},
    {"q": "シーサーが働いているラーメン屋さんの名前は？", "a": ["郎"], "hint": "「二○系ラーメン」○に入るのは？"}
]

# ===== ユーザー入力を正規化（全角→半角、ひらがな→カタカナ）=====
def hira_to_kata(text):
    # ひらがな → カタカナに変換
    return ''.join([chr(ord(ch) + 0x60) if 'ぁ' <= ch <= 'ゖ' else ch for ch in text])

def normalize(text):
    # NFKCで全角→半角に、stripで前後空白除去、ひらがな→カタカナ
    text = unicodedata.normalize("NFKC", text).strip()
    text = hira_to_kata(text)
    return text

# ===== じゃんけんフェーズ（ヒントチャレンジ）=====
def janken_phase():
    enemy_character2 = random.choice(characters2)  # 敵キャラをランダム選出
    print(f"\n{enemy_character2} がじゃんけんを仕掛けてきた！")

    player_hand = input("じゃんけんぽん！（グー / チョキ / パー）: ")
    if player_hand not in hands:# 無効な手は即負け
        print("その手は出せないよ…（負け）")
        return False

    # プレイヤーの手に応じて敵の手を確率で決定
    lose_to_player = {"グー": "チョキ", "チョキ": "パー", "パー": "グー"}
    win_against_player = {"グー": "パー", "チョキ": "グー", "パー": "チョキ"}
    draw_with_player = player_hand# あいこはそのまま

    # 敵が出す手を重み付きでランダムに決定（勝ち45%、負け30%、あいこ25%）
    enemy_choices = (
        [lose_to_player[player_hand]] * 45 +
        [win_against_player[player_hand]] * 30 +
        [draw_with_player] * 25
    )
    enemy_hand = random.choice(enemy_choices)

    print(f"{enemy_character2} は「{enemy_hand}」を出した！")

    # 勝敗判定
    if player_hand == enemy_hand:
        print("あいこ！残念…")
        return False
    elif (player_hand == "グー" and enemy_hand == "チョキ") or \
         (player_hand == "チョキ" and enemy_hand == "パー") or \
         (player_hand == "パー" and enemy_hand == "グー"):
        print("討伐成功！ヒントGET！")
        return True
    else:
        print("負けちゃった…ヒントはもらえないよ")
        return False

# ===== クイズフェーズ =====
def quiz_phase():
    print("\n=== ちいかわクイズスタート！ ===")
    score = 0
    hint_tries = 3  # ヒントチャレンジ可能回数
    questions = quiz.copy() # クイズをコピーしてランダムに並べ替える
    random.shuffle(questions)

    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['q']}")
        while True:
            answer = input("答えは？（ヒントがほしいときは「ヒント」と入力してね)→ ").strip()
            if normalize(answer) == normalize("ヒント"):
                if hint_tries == 0:
                    print("❗ ヒントはもう使い切っちゃったよ！")
                else:
                    print(f"（ヒントチャレンジ残り {hint_tries} 回）")
                    won = janken_phase()
                    if won:
                        print(f"📝 ヒント: {q['hint']}")
                    else:
                        hint_tries -= 1 #負けたらヒント回数を減らす
                        print(f"😢 残念…ヒントは手に入らなかった（残り {hint_tries} 回）")
                continue  # 再入力へ
            break  # ヒント以外の答え入力があれば次へ

        normalized_input = normalize(answer)
        normalized_corrects = [normalize(ans) for ans in q["a"]]

        if normalized_input in normalized_corrects:
            print("⭕ 正解！")
            score += 1
        else:
            print(f"❌ 不正解… 正解は「{q['a']}」だよ")
    return score

def save_score(score):
    # 過去スコア読み込み
    if os.path.exists(score_file):
        with open(score_file, "r", encoding="utf-8") as f:
            scores = [line.strip() for line in f if line.strip()]
    else:
        scores = []

    # 今回のスコアを追加
    scores.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {score}/{len(quiz)}")

    # スコアの数値部分を抽出して降順にソート
    scores.sort(key=lambda x: int(x.split(" - ")[1].split("/")[0]), reverse=True)

    # 最新 max_score 件だけ残す
    scores = scores[:max_score]

    # ファイルに保存
    with open(score_file, "w", encoding="utf-8") as f:
        f.write("\n".join(scores))

    # 保存後に履歴表示
    print("\n📜 スコアランキング！！")
    for s in scores:
        print(s)

# ===== メイン関数 =====
def main():
    print("🌟 ちいかわクイズ with じゃんけんヒント 🌟")
    score = total = quiz_phase()
    print(f"\n🎉 スコア: {score} / {len(quiz)}")
     # 結果に応じたコメント表示
    if score == len(quiz):
        print("ちいかわマスター！すごい！！")
    elif score == len(quiz) - 1:
        print("いい感じ！あと1問だった！")
    else:
        print("また挑戦してね〜")

    # スコアを保存
    save_score(score)    

# ===== 実行部 =====
if __name__ == "__main__":
    main()
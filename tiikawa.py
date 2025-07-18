import random
import unicodedata

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
    if player_hand not in hands:
        print("その手は出せないよ…（負け）")
        return False

    # プレイヤーの手に応じて敵の手を確率で決定
    lose_to_player = {"グー": "チョキ", "チョキ": "パー", "パー": "グー"}
    win_against_player = {"グー": "パー", "チョキ": "グー", "パー": "チョキ"}
    draw_with_player = player_hand

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
    questions = quiz.copy()
    random.shuffle(questions)

    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['q']}")
        while True:
            answer = input("答えは？（ヒントがほしいときは「ヒント」と入力）→ ").strip()
            if normalize(answer) == normalize("ヒント"):
                if hint_tries == 0:
                    print("❗ ヒントはもう使い切っちゃったよ！")
                else:
                    print(f"（ヒントチャレンジ残り {hint_tries} 回）")
                    won = janken_phase()
                    if won:
                        print(f"📝 ヒント: {q['hint']}")
                    else:
                        hint_tries -= 1
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

# ===== メイン関数 =====
def main():
    print("🌟 ちいかわクイズ with じゃんけんヒント 🌟")
    score = quiz_phase()
    print(f"\n🎉 スコア: {score} / 3")
    if score == 3:
        print("ちいかわマスター！すごい！！")
    elif score == 2:
        print("いい感じ！あと1問だった！")
    else:
        print("また挑戦してね〜")

# ===== 実行部 =====
if __name__ == "__main__":
    main()
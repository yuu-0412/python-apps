import random

food = {
    "鳥刺し":"鹿児島",
    "もつ鍋":"福岡",
    "生牡蠣":"広島",
    "カレー":"石川",
    "もんじゃ":"東京",
    "たこ焼き":"大阪",
    "カニ":"北海道",
    "手羽先":"愛知",
    "海ぶどう":"沖縄",
    "かまぼこ":"静岡",
    "ほうとう":"山梨",
    "きび団子":"岡山",
    "みかん":"愛媛",
    "うどん":"香川",
    "フグ":"山口",
    "たまごパン":"長野",
    "リンゴ":"青森",
    "わんこそば":"岩手",
    "唐揚げ":"大分"
}

print("名産品の名前が表示され、それがどの都道府県の名産か当てるクイズ！\n")

while True:
    meisan, prefecture = random.choice(list(food.items()))  
    print(f"『{meisan}』はどこの都道府県の名産品？")
    
    answer = input("答え: ").strip()
    
    if answer == 'exit':
            print("終了")
            break
    
    if answer == prefecture:
                print("🎉 正解！！")


    else:
           print(f"❌ 不正解！正解は『{prefecture}』でした。")            
        
        






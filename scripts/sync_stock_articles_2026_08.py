from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parent.parent
STOCK = ROOT / "config" / "articles_stock.yaml"
FORBIDDEN = ["中古", "訳あり", "ジャンク", "ふるさと納税", "返礼品", "レンタル", "部品", "パーツ", "ケース", "カバー", "交換用", "フィルターのみ", "スタンドのみ", "ケーブルのみ"]
SUPERSEDED_IDS = ["robot-pool-cleaner-ranking"]

# date, id, category, slug, topic, benefit, regret, min_price,
# required_words, discovery_keywords, criteria(id/name), curated product keywords
THEMES = [
("2026-08-01","electric-hot-water-dispenser-ranking","home","electric-hot-water-dispenser","高機能電気ポット","省エネ・給湯量・手入れで選ぶ","再沸騰の待ち時間、蒸気、電気代、内部洗浄の頻度が生活に合わないこと",10000,["電気ポット","電動ポット","まほうびん"],["電気ポット 省エネ","電気ポット 5L"],[("energy","保温時の省エネ性"),("serve","給湯操作と容量"),("care","蒸気対策と洗浄")],["象印 優湯生","タイガー とく子さん"]),
("2026-08-02","air-fryer-ranking","home","air-fryer","ノンフライヤー","容量・焼きムラ・洗いやすさで選ぶ","食材を重ねて焼きムラが出たり、バスケット洗浄が面倒で使わなくなること",10000,["ノンフライヤー","エアフライヤー"],["ノンフライヤー 大容量","エアフライヤー 家庭用"],[("batch","一度に焼ける量"),("finish","加熱の均一性"),("cleanup","油汚れの落としやすさ")],["COSORI TurboBlaze","Ninja Crispi","Philips ノンフライヤー 3000"]),
("2026-08-03","garment-steamer-ranking","home","garment-steamer","衣類スチーマー","立ち上がり・連続噴射・重さで選ぶ","満水時の重さや給水回数が負担になり、朝の身支度で使わなくなること",10000,["衣類スチーマー","スチーマー"],["衣類スチーマー 連続","衣類スチーマー 大容量"],[("startup","立ち上がりと連続性"),("handling","満水時の取り回し"),("finish","プレス兼用のしやすさ")],["パナソニック 衣類スチーマー","ティファール 衣類スチーマー","SteamOne 衣類スチーマー"]),
("2026-08-04","carpet-cleaner-ranking","home","carpet-cleaner","リンサークリーナー","吸水力・タンク分離・乾きやすさで選ぶ","回収水が残って乾燥に時間がかかり、タンク洗浄の負担で出番が減ること",10000,["リンサー","カーペットクリーナー"],["リンサークリーナー 強力","カーペットクリーナー 洗浄機"],[("extract","汚水回収のしやすさ"),("reach","ノズルとホースの扱い"),("cleanup","タンク洗浄と乾燥")],["アイリスオーヤマ RNS-P10-W","BISSELL SpotClean Pro","ケルヒャー SE 3"]),
("2026-08-05","photo-printer-ranking","work","photo-printer","A3ノビ写真プリンター","色管理・インク構成・用紙対応で選ぶ","インク代、ノズル詰まり、用紙プロファイルの不足で作品印刷を続けられないこと",20000,["プリンター","インクジェット"],["A3ノビ 写真プリンター","作品印刷 プリンター"],[("color","色再現と階調"),("media","用紙対応と給紙"),("running","インク運用と保守")],["Canon imagePROGRAF PRO-G1","Epson SC-PX1V","Canon PIXUS PRO-S1"]),
("2026-08-06","portable-solar-panel-ranking","trend","portable-solar-panel","ポータブルソーラーパネル","実発電・収納性・電源互換で選ぶ","手持ち電源と端子が合わず、設置角度や重量のため持ち出さなくなること",20000,["ソーラーパネル","太陽光パネル"],["ポータブル ソーラーパネル 200W","折りたたみ ソーラーパネル"],[("yield","実運用の発電余力"),("carry","重量と収納"),("compat","端子と電源互換")],["EcoFlow 220W ソーラーパネル","Jackery SolarSaga 200","Anker Solix PS200"]),
("2026-08-07","fish-finder-ranking","trend","fish-finder","GPS魚群探知機","画面・振動子・地図機能で選ぶ","釣り方に合う振動子や地図が付かず、船体への取付けと配線で追加費用が出ること",30000,["魚群探知機","魚探"],["魚群探知機 GPS","魚探 振動子 セット"],[("sonar","探知方式と振動子"),("nav","GPS・地図機能"),("install","電源と取付け")],["HONDEX PS-611CNII","Garmin STRIKER Vivid 7sv","LOWRANCE HOOK Reveal 7"]),
("2026-08-08","ems-lift-brush-ranking","beauty","ems-lift-brush","EMSリフトブラシ","刺激調整・使用部位・手入れで選ぶ","肌や頭皮に合わせたレベル調整ができず、準備と清掃が面倒で継続できないこと",20000,["ブラシ","美顔器","EMS"],["EMS ブラシ 美顔器","電気ブラシ 頭皮"],[("control","刺激レベルの調整"),("coverage","顔・頭皮への使い分け"),("routine","日常への組み込みやすさ")],["Brighte ELEKI BRUSH+","YA-MAN ミーゼ スカルプリフト アクティブ プラス","MYTREX PROVE"]),
("2026-08-09","pet-dryer-house-ranking","home","pet-dryer-house","ペットドライハウス","温度管理・静音性・清掃で選ぶ","温風の当たり方、運転音、抜け毛清掃が合わず、ペットが入らないこと",30000,["ペット","ドライ","ドライヤー"],["ペット ドライハウス","ペット ドライルーム"],[("comfort","温度と風の穏やかさ"),("noise","運転音と慣れやすさ"),("clean","抜け毛と庫内清掃")],["Homerunpet Drybo Plus","PETKIT AIRSALON MAX","nello ペットドライルーム"]),
("2026-08-10","dog-stroller-ranking","home","dog-stroller","高級ペットカート","走行安定・折りたたみ・耐荷重で選ぶ","段差での振動、車載時の大きさ、コット着脱が生活導線に合わないこと",25000,["ペットカート","ペットバギー","ドッグカート"],["ペットカート 高級","犬 バギー 折りたたみ"],[("ride","段差と旋回の安定性"),("load","耐荷重と室内寸法"),("store","折りたたみと車載")],["AIRBUGGY DOME3","Piccolo Cane TANTO3","Combi Compet milimili EG"]),
("2026-08-11","premium-stroller-ranking","home","premium-stroller","高級ベビーカー","押し心地・折りたたみ・新生児対応で選ぶ","玄関や改札での幅、片手折りたたみ、シート角度が生活導線に合わないこと",30000,["ベビーカー","ストローラー"],["ベビーカー 高級","ベビーカー 新生児 軽量"],[("ride","押し心地と段差対応"),("fold","折りたたみと車載"),("seat","月齢対応と姿勢")],["CYBEX MELIO CARBON","AIRBUGGY COCO PREMIER FROM BIRTH","Bugaboo Butterfly 2"]),
("2026-08-12","aquarium-chiller-ranking","home","aquarium-chiller","水槽用クーラー","冷却能力・運転音・配管で選ぶ","室温上昇時に能力不足となり、ポンプ流量や配管径が合わず追加購入が出ること",20000,["水槽","クーラー","冷却"],["水槽用 クーラー","アクアリウム クーラー"],[("cooling","真夏の冷却余力"),("noise","運転音と排熱"),("plumbing","流量と配管互換")],["ゼンスイ ZC-100α","GEX クールウェイ BK-C220","テトラ クールタワー CR-3 NEW"]),
("2026-08-13","golf-laser-rangefinder-ranking","trend","golf-laser-rangefinder","ゴルフ用レーザー距離計","測定速度・手ぶれ補正・携帯性で選ぶ","ピンへ合わせにくく、競技モード切替やケース出し入れに時間がかかること",20000,["距離計","レーザー","ゴルフ"],["ゴルフ レーザー距離計","距離計 手ぶれ補正"],[("lock","ピン捕捉と測定速度"),("stability","手ぶれへの強さ"),("carry","サイズとケース運用")],["Bushnell Tour V6 Shift","Nikon COOLSHOT PROII STABILIZED","Voice Caddie TL1"]),
("2026-08-14","indoor-bike-trainer-ranking","beauty","indoor-bike-trainer","スマートトレーナー","勾配再現・静音性・アプリ互換で選ぶ","住環境の振動、車体規格、利用アプリが合わず設置後に使えないこと",50000,["スマートトレーナー","ダイレクトドライブ","KICKR","Tacx","DIRETO"],["スマートトレーナー ダイレクトドライブ","自転車 トレーナー 静音"],[("ride","負荷変化と勾配再現"),("noise","振動と駆動音"),("compat","車体・アプリ互換")],["Wahoo KICKR CORE","Garmin Tacx NEO 2T","ELITE DIRETO XR"]),
("2026-08-15","premium-tent-ranking","trend","premium-tent","高級2ルームテント","居住性・耐候性・設営人数で選ぶ","区画へ収まらず、重量とポール本数で設営が破綻すること",70000,["テント","2ルーム","ツールーム"],["2ルームテント 高級","大型テント ファミリー"],[("space","有効居住空間"),("weather","雨風への備え"),("setup","重量と設営負担")],["Snow Peak Land Lock TP-671R","Coleman 4S Wide 2 Room Cocoon III","Ogawa Apollon T/C"]),
("2026-08-16","sauna-tent-ranking","trend","sauna-tent","テントサウナ","耐熱性・設営・換気で選ぶ","ストーブ適合、換気、煙突位置、乾燥保管が不十分になり安全に続けられないこと",40000,["サウナテント","テントサウナ"],["テントサウナ セット","サウナテント 断熱"],[("heat","断熱と温度維持"),("safety","換気と煙突まわり"),("setup","設営・乾燥・収納")],["MORZH テントサウナ","Iam Sauna テントサウナ","サウナテント 4人用"]),
("2026-08-17","power-rack-ranking","beauty","power-rack","家庭用パワーラック","耐荷重・安全機構・占有面積で選ぶ","天井高、セーフティ位置、プレート収納が合わず安全な一人トレーニングができないこと",30000,["パワーラック","ハーフラック"],["パワーラック 家庭用","ホームジム ラック"],[("safety","セーフティと剛性"),("fit","寸法と可動域"),("expand","アタッチメント拡張")],["IROTEC","BARWING","WILD FIT"]),
("2026-08-18","adjustable-dumbbell-ranking","beauty","adjustable-dumbbell","可変式ダンベル","重量変更・台座安定・省スペースで選ぶ","重量変更のテンポ、台座への戻しやすさ、グリップ長が種目に合わないこと",20000,["可変式ダンベル","アジャスタブルダンベル"],["可変式ダンベル 32kg","ダンベル 重量調整"],[("change","重量変更の速さ"),("balance","長さと重心"),("storage","台座と収納")],["FLEXBELL 32kg 2kg刻み","Bowflex SelectTech 552i","NUOBELL 32kg"]),
("2026-08-19","elliptical-trainer-ranking","beauty","elliptical-trainer","家庭用クロストレーナー","歩幅・静音性・設置剛性で選ぶ","歩幅が身体に合わず、床振動と本体寸法で継続できないこと",30000,["クロストレーナー","エリプティカル"],["クロストレーナー 家庭用","エリプティカル 静音"],[("stride","歩幅と姿勢"),("noise","駆動音と床振動"),("stability","剛性と設置面積")],["Horizon クロストレーナー","アルインコ クロストレーナー","Reebok クロストレーナー"]),
("2026-08-20","premium-camping-cot-ranking","trend","premium-camping-cot","高級キャンプコット","寝面張力・高さ切替・収納で選ぶ","寝面の沈み、組立て力、収納長が車載と睡眠姿勢に合わないこと",15000,["コット","キャンプベッド"],["キャンプ コット 高級","コット ワイド"],[("sleep","寝面の張りと幅"),("setup","組立て負担"),("pack","収納寸法と重量")],["Helinox Tactical Cot Convertible","Snow Peak High Tension Cot BD-030","DOD Hanpen in the Sky CB1-633"]),
("2026-08-21","golf-launch-monitor-ranking","trend","golf-launch-monitor","ゴルフ弾道測定器","計測項目・設置距離・アプリ料金で選ぶ","必要な弾道データを取れず、屋内の設置距離や継続課金が練習環境に合わないこと",30000,["弾道測定器","ゴルフ","ローンチモニター"],["ゴルフ 弾道測定器","ローンチモニター ゴルフ"],[("metrics","計測できる弾道データ"),("space","屋内外の設置条件"),("service","アプリと継続費用")],["Garmin Approach R10","Rapsodo MLM2PRO","Voice Caddie SC4"]),
("2026-08-22","cordless-chainsaw-ranking","work","cordless-chainsaw","充電式チェーンソー","切断力・重量・安全機構で選ぶ","ガイドバー長と本体重量が作業に合わず、チェーン調整や給油を怠って危険になること",25000,["チェンソー","チェーンソー"],["充電式 チェーンソー","コードレス チェンソー"],[("cut","切断径と粘り"),("handling","重量とバランス"),("safety","ブレーキと保守")],["マキタ MUC353","HiKOKI CS3630","ハスクバーナ 540i"]),
("2026-08-23","laser-level-ranking","work","laser-level","高精度レーザー墨出し器","精度・見やすさ・受光器互換で選ぶ","屋外で見えず、三脚や受光器が合わず、校正費用まで見落とすこと",25000,["レーザー","墨出し"],["レーザー 墨出し器 グリーン","墨出し器 フルライン"],[("accuracy","精度と校正"),("visibility","屋内外の視認性"),("system","電源・受光器・三脚互換")],["タジマ ZERO BLUE","マキタ SK507GD","Bosch GLL 3-80"]),
("2026-08-24","welding-machine-ranking","work","welding-machine","100V半自動溶接機","板厚対応・電源・消耗品で選ぶ","家庭回路で安定せず、使用率とワイヤー入手性が作業量に合わないこと",20000,["溶接機","半自動"],["100V 半自動溶接機","ノンガス 溶接機"],[("arc","アーク安定と板厚"),("power","100V回路との相性"),("supply","ワイヤーと保守部品")],["SUZUKID Buddy SBD-80","SUZUKID Arcury 80 Luna III","YOTUKA YS-MIG100"]),
("2026-08-25","air-compressor-ranking","work","air-compressor","高圧エアコンプレッサー","吐出量・静音性・電源で選ぶ","連続吐出量が足りず、再起動音と電圧降下で現場運用が止まること",50000,["コンプレッサ","コンプレッサー","高圧"],["高圧 エアコンプレッサー","コンプレッサー 静音 建築"],[("flow","連続吐出量"),("noise","再起動音と振動"),("site","電源と持ち運び")],["Makita AC500XL","HiKOKI EC1245H3","MAX AK-HL1310E"]),
("2026-08-26","gaming-chair-ranking","work","gaming-chair","高級ゲーミングチェア","姿勢調整・座面・保証で選ぶ","座面高と奥行きが体格に合わず、長時間作業で腰と肩の負担が増えること",30000,["ゲーミングチェア","チェア"],["ゲーミングチェア 高級","ゲーミングチェア ファブリック"],[("fit","体格への調整幅"),("seat","座面と背面の支持"),("durability","張地・機構・保証")],["AKRacing Premium","noblechairs EPIC","Contieaks Rosa"]),
("2026-08-27","electric-adjustable-bed-ranking","home","electric-adjustable-bed","電動リクライニングベッド","起き上がり・マットレス・搬入で選ぶ","身体に合う屈曲位置、マットレス硬さ、搬入経路が合わず日常動作を改善できないこと",80000,["電動ベッド","リクライニングベッド"],["電動ベッド 介護","電動リクライニングベッド"],[("motion","背・脚の動かしやすさ"),("sleep","マットレスと姿勢"),("delivery","搬入・設置・保証")],["パラマウントベッド INTIME","フランスベッド 電動ベッド","グランツ 電動ベッド"]),
("2026-08-28","baby-monitor-ranking","home","baby-monitor","高機能ベビーモニター","検知方式・通信・夜間画質で選ぶ","Wi-Fi障害、通知過多、設置角度で必要な場面を見逃すこと",15000,["ベビーモニター","見守りカメラ"],["ベビーモニター 高機能","ベビーモニター WiFi不要"],[("alert","通知と検知の分かりやすさ"),("link","Wi-Fi・専用モニター方式"),("night","暗所画質と設置")],["CuboAi Plus スマートベビーモニター","Panasonic KX-HC705","Babysense HD S2"]),
("2026-08-29","laser-engraver-ranking","work","laser-engraver","密閉型レーザー加工機","出力・安全対策・排気で選ぶ","素材に合わず、煙と火災対策、作業範囲、ソフト互換で追加費用が出ること",50000,["レーザー","彫刻","加工機"],["レーザー加工機 密閉型","レーザー彫刻機 20W"],[("process","切断・彫刻の対応幅"),("safety","カバー・停止・排気"),("workflow","ソフトと位置合わせ")],["xTool S1 20W","LaserPecker 4","Creality Falcon2 22W"]),
("2026-08-30","3d-scanner-ranking","work","3d-scanner","ハンディ3Dスキャナー","追従性・精度・PC要件で選ぶ","黒色・光沢物で追従を失い、PC性能と後処理時間が足りなくなること",50000,["3Dスキャナー","3Dスキャン"],["ハンディ 3Dスキャナー","3Dスキャナー 高精度"],[("tracking","対象追従と再取得"),("detail","細部と寸法精度"),("compute","PC・後処理・出力")],["Creality CR-Scan Otter","Revopoint MIRACO","SHINING 3D Einstar"]),
("2026-08-31","thermal-camera-ranking","work","thermal-camera","高性能サーモグラフィーカメラ","熱解像度・測温範囲・記録で選ぶ","必要温度帯を測れず、放射率設定とレポート出力が現場用途に合わないこと",30000,["サーモグラフィ","熱画像","赤外線"],["サーモグラフィーカメラ 高解像度","赤外線カメラ 測温"],[("image","熱解像度と視認性"),("range","測温範囲と精度"),("record","保存・注釈・レポート")],["FLIR ONE Edge Pro","HIKMICRO Pocket2","Bosch GTC 600 C"]),
]

def build(spec):
    date, aid, category, slug, topic, benefit, regret, min_price, required, discovery, criteria, products = spec
    names = "、".join(products)
    axes = "・".join(name for _, name in criteria)
    ids = [cid for cid, _ in criteria]
    extras = []
    score_sets = ([4.8,4.6,4.3],[4.6,4.8,4.4],[4.4,4.5,4.8])
    for keyword, scores in zip(products, score_sets):
        extras.append({
            "keyword": keyword,
            "best_for": f"{keyword}を指名候補にし、{criteria[0][1]}と{criteria[1][1]}を優先して購入条件を詰めたい人",
            "scores": dict(zip(ids, scores)),
            "analysis_why": f"{keyword}は{topic}の指名買い候補です。商品説明の仕様表記、公開レビュー評価・件数、販売元、保証を同じ軸で確認できる場合だけ掲載します。",
            "pros": [f"{keyword}の新品本体を指名検索できる", f"{criteria[0][1]}を商品説明で比較できる", f"{criteria[1][1]}と保証条件を購入前に照合できる"],
            "critical_cons": f"{keyword}でも販売店ごとに型番、付属品、保証、納期が異なり、名称だけで同一条件とは判断できません。",
            "maintenance_reality": f"購入後は{criteria[2][1]}に関わる消耗、清掃、設置状態を定期確認する必要があります。",
            "cost_performance": f"{benefit}という目的を高頻度で使い、買い直しや作業の手戻りを減らせる人には価格を回収しやすい候補です。",
        })
    return {
        "id": aid, "category_id": category, "type": "daily", "slug": slug, "release_date": date,
        "h1": f"{topic}比較｜{benefit}", "title": f"【2026年】{topic}比較｜{benefit}",
        "intro": f"{topic}は価格や知名度だけで決めると、{regret}があります。本記事では{names}を、{axes}で比較し、購入前に確認すべき条件を明確にします。",
        "meta_description": f"{topic}を{names}で比較。{axes}を軸に、新品本体の価格・在庫・保証を楽天市場で確認する前の判断ポイントを整理します。",
        "analysis_insight": f"{topic}で最も避けたい後悔は、{regret}です。公開レビュー評価・件数と商品説明の仕様表記を根拠に、数合わせをせず、用途に合う候補だけを比較します。",
        "qa_config": {"min_price": min_price, "required_words": required, "forbidden_words": FORBIDDEN},
        "rakuten_params": {"keyword": ", ".join(products), "discovery_keywords": discovery, "hits": 20, "sort": "-reviewCount"},
        "test_criteria": [{"id": cid, "name": name} for cid, name in criteria], "products_extra": extras,
    }

def block(article):
    dumped = yaml.safe_dump([article], allow_unicode=True, sort_keys=False, width=1000).rstrip()
    return "\n".join("  " + line for line in dumped.splitlines()) + "\n"

def main():
    text = STOCK.read_text(encoding="utf-8")
    for article_id in SUPERSEDED_IDS:
        retired = re.compile(rf"(?ms)^  - id: {re.escape(article_id)}\r?\n.*?(?=^  - id: |\Z)")
        text = retired.sub("", text)
    if [x[0] for x in THEMES] != [f"2026-08-{d:02d}" for d in range(1,32)]:
        raise ValueError("August plan must cover 2026-08-01 through 2026-08-31 exactly")
    if len({x[1] for x in THEMES}) != len(THEMES):
        raise ValueError("duplicate article id")
    replaced = appended = 0
    for spec in THEMES:
        article = build(spec)
        pattern = re.compile(rf"(?ms)^  - id: {re.escape(article['id'])}\r?\n.*?(?=^  - id: |\Z)")
        if pattern.search(text):
            text = pattern.sub(block(article), text, count=1); replaced += 1
        else:
            text = text.rstrip() + "\n" + block(article); appended += 1
    STOCK.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"August stock synchronized: replaced={replaced}, appended={appended}, total={len(THEMES)}")

if __name__ == "__main__":
    main()

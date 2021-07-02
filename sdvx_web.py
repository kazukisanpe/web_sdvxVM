from bs4 import BeautifulSoup
import sys
from bs4.element import PageElement
import requests
import re
import time
import sqlite3

#実行処理時間計測開始
start = time.time()

# データベースに接続する
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

#テーブル「store」が存在する場合は削除
c.execute("DROP TABLE IF EXISTS app_item")

# テーブルの作成
c.execute('''
    CREATE TABLE app_item(
        id integer,
        store_name text,
        store_address text,
        store_prefecture text,
        store_holiday text,
        store_operationtime text,
        store_telno text,
        store_latitude text,
        store_longitude text
        )
        ''')

#各都道府県を定義（search_prefに引数を渡して全国を網羅的に検索）
search_pref_all = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
#店舗数カウンタ
cnt = 0
#店名のSQLインジェクション防止
code_regex = re.compile('["\'\\\\()*+,-./:;?[\\]]')
for search_pref_ in range(len(search_pref_all)):
    search_pref = search_pref_all[search_pref_]

    # Webページを取得して解析する
    load_url = "https://p.eagate.573.jp/game/facility/search/p/list.html?gkey=SDVX&paselif=false&finder=keyword&keyword=" + search_pref
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    store_cnt_ = soup.find(class_="cl_search_result")
    elems = soup.find_all(class_ = "cl_shop_bloc")

    #表示
    print(search_pref + "のSOUND VOLTEX設置店情報をINSERT")
    #何件取得できたか出力
    print(store_cnt_.contents[0])
    #該当店舗数が一桁か二桁か判別
    store_cnt = store_cnt_.contents[0][0:1] if "件" in store_cnt_.contents[0][0:2] else store_cnt_.contents[0][0:2]

    #1ページ目の情報（店舗件数が一桁）
    for num in range(len(elems)):
        store_info = list()
        cnt = cnt + 1
        store_info.append(str(cnt))
        store_info.append(code_regex.sub('', elems[num].attrs['data-name'])) #店舗名
        store_info.append(elems[num].attrs['data-address'] if elems[num].attrs['data-address'] != "" else "データなし") #所在地
        store_info.append(search_pref) #所在県
        store_info.append(elems[num].attrs['data-holiday'] if elems[num].attrs['data-holiday'] != "" else "データなし") #定休日
        store_info.append(elems[num].attrs['data-operationtime'] if elems[num].attrs['data-operationtime'] != "" else "データなし") #営業時間
        store_info.append(elems[num].attrs['data-telno'] if elems[num].attrs['data-telno'] != "" else "データなし") #電話番号
        store_info.append(elems[num].attrs['data-latitude'] if elems[num].attrs['data-latitude'] != "" else "データなし") #緯度
        store_info.append(elems[num].attrs['data-longitude'] if elems[num].attrs['data-longitude'] != "" else "データなし") #経度
        #print(store_info)
        # データの挿入
        c.execute("INSERT INTO app_item VALUES (" + str(cnt) + ",'" + store_info[1] + "', '" + store_info[2] + "', '" + store_info[3] + "', '" + store_info[4] + "', '" + store_info[5] + "', '" + store_info[6] + "', '" + store_info[7] + "', '" + store_info[8] + "')")


    # 挿入した結果を保存（コミット）する
    conn.commit()

    #該当店舗数が二桁
    if int(store_cnt) > 10:
        #1ページに10件表示されるため店舗数が10店より多ければページ数分URL表示
        page_num = int(store_cnt)//10
        for page_num_ in range(page_num):
            load_url_2 = load_url + "&page=" + str(page_num_+2) #ページ番号をURLに付与
            html_2 = requests.get(load_url_2)
            soup_2 = BeautifulSoup(html_2.content, "html.parser")
            elems_2 = soup_2.find_all(class_ = "cl_shop_bloc")

            for num in range(len(elems_2)):
                store_info = list()
                cnt = cnt + 1
                store_info.append(str(cnt))
                store_info.append(code_regex.sub('', elems_2[num].attrs['data-name'])) #店舗名
                store_info.append(elems_2[num].attrs['data-address'] if elems_2[num].attrs['data-address'] != "" else "データなし") #所在地
                store_info.append(search_pref) #所在県
                store_info.append(elems_2[num].attrs['data-holiday'] if elems_2[num].attrs['data-holiday'] != "" else "データなし") #定休日
                store_info.append(elems_2[num].attrs['data-operationtime'] if elems_2[num].attrs['data-operationtime'] != "" else "データなし") #営業時間
                store_info.append(elems_2[num].attrs['data-telno'] if elems_2[num].attrs['data-telno'] != "" else "データなし") #電話番号
                store_info.append(elems_2[num].attrs['data-latitude'] if elems_2[num].attrs['data-latitude'] != "" else "データなし") #緯度
                store_info.append(elems_2[num].attrs['data-longitude'] if elems_2[num].attrs['data-longitude'] != "" else "データなし") #経度
                #print(store_info)   
                # データの挿入
                c.execute("INSERT INTO app_item VALUES (" + str(cnt) + ",'" + store_info[1] + "', '" + store_info[2] + "', '" + store_info[3] + "', '" + store_info[4] + "', '" + store_info[5] + "', '" + store_info[6] + "', '" + store_info[7] + "', '" + store_info[8] + "')") 

        # 挿入した結果を保存（コミット）する
        conn.commit()

# データベースへのアクセスが終わったら close する
conn.close()

print(str(cnt) + "件の情報をdb.app_itemにINSERTしました。")

#計測処理時間を出力
elapsed_time = time.time() - start
print ("実行結果:{:.2f}".format(elapsed_time) + "[sec]")




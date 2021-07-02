# 必要モジュールをインポートする
from bs4 import BeautifulSoup
import sqlite3
import time
import sys
import re

#実行処理時間計測開始
start = time.time()

#引数を取得
search_pref = ""
if len(sys.argv) == 1:
    search_pref = ""
else:
    args = sys.argv
    search_pref = args[1]

#記号排除
code_regex = re.compile('["\'\\\\()*+,-./:;?[\\]]')

# データベースに接続する
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# テーブル"store"の情報を取得する
sql_1 = "SELECT * FROM app_item"
sql_2 = ""
#引数に県の値があれば元sqlに県指定のsqlを追加
if search_pref != "":
    sql_2 = " WHERE store_prefecture = '" + search_pref + "'"
sql = sql_1 + sql_2

print("SQL:" + sql)
for row in c.execute(sql):
    print(row)

#何件取得したかの表示用SQL
count_sql = "SELECT count(*) count_num FROM app_item" + sql_2
c.execute(count_sql)

print(code_regex.sub('', str(c.fetchone())) + "件のデータを取得")

# データベースへのアクセスが終わったら close する
conn.close()

#計測処理時間を出力
elapsed_time = time.time() - start
#print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
print ("実行結果:{:.2f}".format(elapsed_time) + "[sec]")
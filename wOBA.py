import requests
from bs4 import BeautifulSoup

# 分別五個網址
url1 = "http://www.cpbl.com.tw/stats/all.html?year=2020&game_type=01&stat=pbat&online=0&sort=G&order=desc&per_page="
url2 = "http://www.cpbl.com.tw/stats/all.html?year=2020&game_type=01&stat=pbat&online=0&sort=G&order=desc&per_page=2"
url3 = "http://www.cpbl.com.tw/stats/all.html?year=2020&game_type=01&stat=pbat&online=0&sort=G&order=desc&per_page=3"
url4 = "http://www.cpbl.com.tw/stats/all.html?year=2020&game_type=01&stat=pbat&online=0&sort=G&order=desc&per_page=4"
url5 = "http://www.cpbl.com.tw/stats/all.html?year=2020&game_type=01&stat=pbat&online=0&sort=G&order=desc&per_page=5"

# 五頁網址合併一個list
url = [url1, url2, url3, url4, url5]

# 球員清單
players = []

# for 迴圈跑五個網址
for i in range(5):
    webpage = requests.get(url[i])
    # webpage.content[:500].decode('utf-8'))

    soup = BeautifulSoup(webpage.text, 'html5lib')

    # 利用 class 從該 HTML 裡取得特定表格
    table = soup.find('table', {'class': 'std_tb mix_x'})

    # 產生數據名稱
    columns = [th.text for th in table.find('tr').find_all('th')]
    columns.append('OPS')
    columns.append('wOBA')
    new_columns = [columns[1], columns[17], columns[15], columns[16], columns[31], columns[32]]

    # 產生對應球員資料
    trs = table.find_all('tr')[1:]
    for tr in trs:
        players.append([td.text.replace(' ', '') for td in tr.find_all('td')])

    # 計算 OPS 跟 wOBA
    for i in range(len(players)):
        # OPS
        OPS = float(players[i][15])+float(players[i][16])
        # wOBA
        wOBA = ((0.69*float(players[i][21])-float(players[i][22]))+(0.719*float(players[i][23]))+(0.87*float(players[i][8]))+(1.217*float(players[i][9]))+(1.529*float(players[i][10]))+(1.94*float(players[i][11])))/(float(players[i][4])+float(players[i][21])-float(players[i][22])+float(players[i][23])+float(players[i][20]))
        players[i].append(OPS)
        players[i].append(wOBA)
        # print(players[i][1], players[i][31], players[i][32], sep='\t')
print("")

# 印出達到打席數
print("PA >= G*3.1")

# 印出第一行數據名稱
for i in range(6):
    print(new_columns[i], end='\t')
print('')

# 比較各球員 wOBA
comp = []
for i in range(len(players)):
    comp.append(players[i][32])
c = sorted(comp)
c.reverse()

# 排序 and 篩選掉打席不足的球員，再將結果印出
for i in range(len(c)):
    for j in range(len(c)):
        if players[j][32] == c[i] and float(players[j][3]) >= 91*3.1:
            print(players[j][1], players[j][17], players[j][15], players[j][16], '%.3f'%players[j][31], '%.3f'%players[j][32], sep='\t')
print("")

# 印出不到打席數的
print("PA <= G*3.1")

# 印出數據名稱
for i in range(6):
    print(new_columns[i], end='\t')
print('')

# 排序剩餘球員，再將結果印出
for i in range(len(c)):
    for j in range(len(c)):
        if players[j][32] == c[i] and float(players[j][3]) <= 91*3.1:
            print(players[j][1], players[j][17], players[j][15], players[j][16], '%.3f'%players[j][31], '%.3f'%players[j][32], sep='\t')
print("")
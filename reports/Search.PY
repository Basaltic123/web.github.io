import http.client
import urllib.parse
import json
import random

# 連接到 KKBOX API
conn = http.client.HTTPSConnection("api.kkbox.com")

# 搜尋特定歌曲或歌手
search_keyword = "lemon"  # 可以是歌曲名稱或歌手名稱
encoded_keyword = urllib.parse.quote(search_keyword)

headers = {
    'accept': "application/json",
    'authorization': "Bearer ECEC8Mx9wZWcM9PIVx14kQ=="  # 你的 KKBOX API 金鑰
}

conn.request("GET", f"/v1.1/search?q={encoded_keyword}&type=track&territory=TW&offset=0&limit=1", headers=headers)
res = conn.getresponse()
data = res.read()
kkbox_data = json.loads(data.decode("utf-8"))

# 檢查是否找到相關歌曲
if 'tracks' in kkbox_data and 'data' in kkbox_data['tracks'] and len(kkbox_data['tracks']['data']) > 0:
    artist_name = kkbox_data['tracks']['data'][0]['album']['artist']['name']
    song_name = kkbox_data['tracks']['data'][0]['name']
    print(f"找到歌曲：{song_name} - {artist_name}")

    # 使用相關資訊再次調用 KKBOX API，進行類似歌曲的搜尋
    encoded_artist_name = urllib.parse.quote(artist_name)
    conn.request("GET", f"/v1.1/search?q={encoded_artist_name}&type=track&territory=TW&offset=0&limit=30", headers=headers)
    res = conn.getresponse()
    data = res.read()
    kkbox_data = json.loads(data.decode("utf-8"))

    # 處理類似歌曲的搜尋結果
    if 'tracks' in kkbox_data and 'data' in kkbox_data['tracks'] and len(kkbox_data['tracks']['data']) > 0:
        print("類似歌曲：")
        # 取得相似歌曲清單
        similar_tracks = kkbox_data['tracks']['data']
        # 隨機排序相似歌曲清單
        random.shuffle(similar_tracks)
        for i, track in enumerate(similar_tracks[:5]):  # 只顯示前五首
            similar_artist_name = track['album']['artist']['name']
            similar_song_name = track['name']
            print(f"{i + 1}. {similar_song_name} - {similar_artist_name}")
    else:
        print("找不到相似歌曲。")
else:
    print("找不到相關的歌曲。")

conn.close()

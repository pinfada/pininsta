from TikTokApi import TikTokApi as tiktok
import pandas as pd

#verifyFp = "verify_kx2ee558_BH6fvQVi_cXHF_4lfK_Bimg_hH0lYMCV6Vm6"
proxy_address = "http://122.116.20.91:8080"
api = tiktok.get_instance(proxy=proxy_address)

#api = tiktok.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
#api = TikTokApi()

def simple_dict(tiktok_dict):
  to_return = {}
  to_return['user_name'] = tiktok_dict['author']['uniqueId']
  to_return['user_id'] = tiktok_dict['author']['id']
  to_return['video_id'] = tiktok_dict['id']
  to_return['video_desc'] = tiktok_dict['desc']
  to_return['video_time'] = tiktok_dict['createTime']
  to_return['video_length'] = tiktok_dict['video']['duration']
  to_return['video_link'] = 'https://www.tiktok.com/@{}/video/{}?lang=en'.format(to_return['user_name'], to_return['video_id'])
  to_return['n_likes'] = tiktok_dict['stats']['diggCount']
  to_return['n_shares'] = tiktok_dict['stats']['shareCount']
  to_return['n_comments'] = tiktok_dict['stats']['commentCount']
  to_return['n_plays'] = tiktok_dict['stats']['playCount']
  return to_return

# recommended, individual
seed_users = ['tiktok', 'washingtonpost', 'charlidamelio', 'chunkysdead']
seed_ids = [api.get_user(user_name, proxy=proxy_address)['userInfo']['user']['id'] for user_name in seed_users]
suggested = [api.get_suggested_users_by_id_crawler(count=5, startingId=s_id, proxy=proxy_address) for s_id in seed_ids]

for i in range(len(suggested)):
    print("\nSeed: {}".format(seed_users[i]))
    for u in suggested[i]:
        print('{} ({}, {} fans)'.format(u['subTitle'], u['title'], u['extraInfo']['fans']))

# recommended, crawler
#tiktok_id = api.get_user('tiktok')['userInfo']['user']['id']
#suggested_10 = api.getSuggestedUsersbyIDCrawler(count=10, startingId=tiktok_id)


# trending videos
n_trending = 5
trending_videos = api.by_trending(count=n_trending, proxy=proxy_address)
trending_videos = [simple_dict(v) for v in trending_videos]
trending_videos_df = pd.DataFrame(trending_videos)
trending_videos_df.to_csv('trending.csv', encoding='utf-8', index=False)
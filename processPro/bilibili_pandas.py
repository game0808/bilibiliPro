import pandas as pd
import numpy as np

# 读取路径
# ./user_info.csv
user_info_df = pd.read_csv('')

user_info_df_1 = user_info_df.loc[user_info_df['following'].isnull() & user_info_df['archive_view'].isnull(), 'mid':'level'].sort_values(
    by='mid', ascending=True)
user_info_df_2 = user_info_df.loc[user_info_df['following'].notnull(), [
    'mid', 'following', 'follower']]
user_info_df_3 = user_info_df.loc[user_info_df['archive_view'].notnull(
), ['mid', 'archive_view', 'article_view', 'likes']]

user_info_df = pd.merge(
    user_info_df_1, user_info_df_2, left_on='mid', right_on='mid', how='outer')
user_info_df = pd.merge(
    user_info_df, user_info_df_3, left_on='mid', right_on='mid', how='outer')

# 缺失mid
invalid_mid = []
for i in range(1,int(user_info_df['mid'].max())):
    if i not in user_info_df['mid']:
        invalid_mid.append(i)
# 用户数
user_number = user_info_df.shape[0]
# 性别分布
sex_m = user_info_df[user_info_df['sex'] == '男'].shape[0]
sex_f = user_info_df[user_info_df['sex'] == '女'].shape[0]
sex_s = user_info_df[user_info_df['sex'] == '保密'].shape[0]
# 签名分布
sign_notnull = user_info_df[user_info_df['sign'].isnull()].shape[0]
sign_isnull = user_number - sign_notnull
# 等级分布
avg_level = int(user_info_df['level'].mean())
# 关注数分布
max_following = int(user_info_df['following'].max())
avg_following = int(user_info_df['following'].mean())
# 粉丝数分布
max_follower = int(user_info_df['follower'].max())
avg_follower = int(user_info_df['follower'].mean())
# 播放量分布
max_archive_view = int(user_info_df['archive_view'].max())
avg_archive_view = int(user_info_df['archive_view'].mean())
# 阅读量分布
max_article_view = int(user_info_df['article_view'].max())
avg_article_view = int(user_info_df['article_view'].mean())
# 获赞数分布
max_likes = int(user_info_df['likes'].max())
avg_likes = int(user_info_df['likes'].mean())

d_mid = {
    '缺失mid': len(invalid_mid),
    '用户数': user_number,
}

d_sex = {
    '性别_男_人数': sex_m,
    '性别_女_人数': sex_f,
    '性别_保密_人数': sex_s,
}

d_sign = {
    '签名_空_人数': sign_isnull,
    '签名_人数': sign_notnull,
}

d_level = {
    '平均等级': avg_level,
}

d_following = {
    '最高关注数': max_following,
    '平均关注数': avg_following,
}

d_follower = {
    '最高粉丝数': max_follower,
    '平均粉丝数': avg_follower,
}

d_archive_view = {
    '最高播放量': max_archive_view,
    '平均播放量': avg_archive_view,
}

d_article_view = {
    '最高阅读量': max_article_view,
    '平均阅读量': avg_article_view,
}

d_likes = {
    '最高获赞数': max_likes,
    '平均获赞数': avg_likes,
}


def helper1():
    pre_sum = 0
    for i in range(7):
        new_key_name = 'level_' + str(i)
        d_level[new_key_name] = user_info_df[user_info_df['level']
                                             <= i].shape[0] - pre_sum
        pre_sum += d_level[new_key_name]


def helper2(key_max, key_name, d):
    pre_sum = user_info_df[user_info_df[key_name] < 10].shape[0]
    d[key_name + '_10'] = pre_sum
    n = 0
    while key_max > 0:
        key_max //= 10
        n += 1
    for i in range(2, n + 1):
        end = 10 ** i
        new_key_name = key_name + '_' + str(end)
        d[new_key_name] = user_info_df[user_info_df[key_name] < end].shape[0] - pre_sum
        pre_sum += d[new_key_name]


helper1()
helper2(max_following, 'following', d_following)
helper2(max_follower, 'follower', d_follower)
helper2(max_archive_view, 'archive_view', d_archive_view)
helper2(max_article_view, 'article_view', d_article_view)
helper2(max_likes, 'likes', d_likes)


def my_print(d):
    for k, v in d.items():
        print(f'{k}:{v}')


my_print(d_mid)
my_print(d_sex)
my_print(d_sign)
my_print(d_level)
my_print(d_following)
my_print(d_follower)
my_print(d_archive_view)
my_print(d_article_view)
my_print(d_likes)
print(invalid_mid)

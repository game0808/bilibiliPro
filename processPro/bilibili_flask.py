from flask import Flask, render_template
from bilibili_pandas import d_mid, d_sex, d_sign, d_level, d_following, d_follower, d_archive_view, d_article_view, d_likes

app = Flask(__name__)


@app.route('/')
def index():
    name = 'bilibili'
    return render_template('index.html', name=name)


@app.route('/bilibili')
def bilibili():
    return render_template('bilibili.html', d_mid=d_mid, d_sex=d_sex, d_sign=d_sign, d_level=d_level, d_following=d_following, d_follower=d_follower, d_archive_view=d_archive_view, d_article_view=d_article_view, d_likes=d_likes)


@app.route('/echarts')
def echarts():
    return render_template('echarts.html')


if __name__ == "__main__":
    app.run()

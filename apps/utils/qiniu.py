import random
from apps.article.views import Article_type
from flask import session

from apps.user.models import User

from qiniu import Auth, put_file, etag, put_data, BucketManager
from settings import Config


def upload_qiniu(filestorage):
    """上传相片"""
    # 需要填写你的 Access Key 和 Secret Key
    # access_key = 'bZlGPCXm3Bt6SPqQeY3G9-Te4PiCHOUlOVuEQWM1'
    # secret_key = '9ttO0AXliBgiUQvMHPsGHPaOXpiqazp6uvDv11nW'
    # 构建鉴权对象
    q = Auth(Config.access_key, Config.secret_key)
    # 要上传的空间
    bucket_name = 'lisa530'
    # 上传后保存的文件名
    filename = filestorage.filename
    ran = random.randint(1, 1000)
    suffix = filename.rsplit('.')[-1]
    key = filename.rsplit('.')[0] + '_' + str(ran) + '.' + suffix
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, filestorage.read())
    return ret, info


# 使用七牛云提供的删除的方法
def delete_qiniu(filename):
    """删除相片"""
    # 构建鉴权对象,接收两个参数,Access Key 和 Secret Key
    q = Auth(Config.access_key,Config.secret_key)
    # 要上传的空间
    bucket_name = 'lisa530'
    # 初始化BucketManager
    bucket = BucketManager(q)
    # key就是要删除的文件的名字
    key = filename
    ret, info = bucket.delete(bucket_name, key)
    return info


def user_type():
    """封装文章分类工具类"""
    # 1.查询所有文章分类
    types = Article_type.query.all()
    # 2. 判断用户是否登录
    user = None
    # 从session中获取用户信息
    user_id = session.get('uid',None)
    if user_id: # 用户存在则查询数据库
        user = User.query.get(user_id)
    # 返回用户和对应文章分类内容
    return user,types
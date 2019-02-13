import memcache

# 开启
mc = memcache.Client(["127.0.0.1:11211"])


# 设置
def set_key(key=None, val=None, time=60 * 5):
    if key and val:
        mc.set(key=key, val=val, time=time)
        return True
    return False


# 查询
def get_key(key=None):
    if key:
        return mc.get(key)
    return key


# 删除
def delete_key(key=None):
    if key:
        mc.delete(key)
        return True
    return False

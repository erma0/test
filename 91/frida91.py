# -*- encoding: utf-8 -*-
'''
@File    :   frida91.py
@Time    :   2022年11月04日 16:08:26 星期五
@Author  :   erma0
@Version :   1.0
@Link    :   https://erma0.cn
@Desc    :   91短视频刷邀请 frida rpc调用自身加密
'''

import requests
import time
import json
from hashlib import sha256, md5
from Crypto.Random import get_random_bytes
# from Crypto.Hash import SHA256, MD5  # 和hashlib库一样
import frida


class Aff(object):
    """
    91短视频刷邀请
    """

    def __init__(self, aff: str = "gcKyA"):
        self.aff = aff
        self.oauth_id = ''
        self.timestamp = ''
        self.url = 'http://api.91apiapi.com/api.php'
        # self.url = 'http://v2.my10api.com:8080/api.php'
        self.headers = {  # 加不加header都可以
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; M973Q Build/LMY49I) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.key = 'OTkZOVoPAAkIWAgICl1bDFgOXAkBSFwOAF8KDgBDX0oPDVhfAiQVNCE2AAkLKw=='
        self.script = self.frida_rpc()

    @staticmethod
    def frida_rpc():
        """
        frida_rpc 主动调用加密方法
        需运行app后用adb转发端口才可以找到进程
        """
        with open('./91.js',encoding='utf-8',) as f:
            jscode = f.read()
        process = frida.get_remote_device().attach('91短視頻')
        script = process.create_script(jscode)
        script.load()
        return script

    @staticmethod
    def get_timestamp(long: int = 10):
        """
        取时间戳，默认10位
        """
        return str(time.time_ns())[:long]

    def decrypt(self, data: str):
        return self.script.exports.decrypt(data, self.key)

    def encrypt(self, data: str):
        return self.script.exports.encrypt(data, self.key)

    def get_sign(self):
        """
        生成sign
        """
        template = 'crypt=V2&data={}&timestamp={}dsaf76cfbb39cjdusihcuekd3b066a6e'.format(
            self.encrypt_data, self.timestamp)
        # sha256
        sha = sha256()
        sha.update(template.encode())
        res = sha.hexdigest()
        # md5
        m = md5()
        m.update(res.encode())
        res = m.hexdigest()
        return res

    def request(self, d: dict):
        """
        请求封包
        """
        plaintext = {
            "app_type": "local",
            "app_status": "78465239911592ACE0E24E5A382B91C769FCBF65:1",
            "build_id": "a1000",
            "oauth_type": "android",
            "version": "5.3.1",
            "apiV2": "v2",
            "token": ""
        }
        d.update(plaintext)
        self.timestamp = self.get_timestamp(10)
        self.encrypt_data = self.encrypt(json.dumps(d, separators=(',', ':')))
        sign = self.get_sign()
        data = {
            "timestamp": self.timestamp,
            "data": self.encrypt_data,
            "sign": sign,
            'crypt': 'V2'
        }
        res = requests.post(url=self.url, data=data, headers=self.headers)
        resj = res.json()
        res = self.decrypt(resj.get('data'))
        print(res)
        return res

    def get_user(self):
        """
        生成新用户
        """
        # 取随机md5
        m = md5()
        m.update(get_random_bytes(16))
        oauth_id = m.hexdigest()
        data = {"mod": "system", "oauth_id": oauth_id, "code": "index"}
        self.request(data)
        self.oauth_id = oauth_id
        print(oauth_id)

    def invite(self):
        """
        刷邀请，邀请码：self.aff
        """
        self.get_user()
        data = {"mod": "user", "oauth_id": self.oauth_id,
                "aff": self.aff, "code": "invitation"}
        self.request(data)


if __name__ == "__main__":
    aff = Aff('gcKyA')
    aff.invite()
    # data = ''
    # print(aff.decrypt(data))

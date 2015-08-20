# -*- coding:utf-8 –*-
__author__ = 'wuyonglin'

import web
import json
import base64
from M2Crypto import RSA

SECKEY_LENGTH = 128

urls = (
    '/Echo/', 'Echo'
)
app = web.application(urls, globals())

class Echo(object):

    def rsa_password(self, *args):
        #在此返回产生密钥时输入的密码
        return '123456'

    def decrypt(self, msg):
        rsa = RSA.load_key('private_key.pem', callback=self.rsa_password)

        encryptString = base64.b64decode(msg)
        originString = ''
        count = len(encryptString) / SECKEY_LENGTH;

        #分段解密
        for i in range(count):
            subEncryptString = encryptString[SECKEY_LENGTH * i : SECKEY_LENGTH *(i+1)]
            subOriginString = rsa.private_decrypt(subEncryptString, 1)
            originString += subOriginString

        return originString

    def GET(self):
        msg = 'Hello!'
        inputDict = web.input()
        if 'msg' in inputDict:
            msg = inputDict['msg']
        web.header('content-type','text/json')
        response = {}
        response['msg'] = self.decrypt(msg)
        return json.dumps(response)

if __name__ == "__main__":
    app.run()
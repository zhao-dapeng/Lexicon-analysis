#encoding:utf-8
import struct
import binascii

class Baidu(object):

    def __init__(self, originfile):
        self.originfile = originfile
        self.lefile = originfile + '.le'
        self.txtfile = originfile[0:(originfile.__len__()-5)] + 'txt'
        self.buf = [b'0' for x in range(0,2)]
        self.listwords = []

    #字节流大端转小端
    def be2le(self):
        of = open(self.originfile,'rb')
        lef = open(self.lefile, 'wb')
        contents = of.read()
        contents_size = contents.__len__()
        mo_size = (contents_size % 2)
        #保证是偶数
        if mo_size > 0:
            contents_size += (2-mo_size)
            contents += contents + b'0000'
        #大小端交换
        for i in range(0, contents_size, 2):
            self.buf[1] = contents[i]
            self.buf[0] = contents[i+1]
            le_bytes = struct.pack('2B', self.buf[0], self.buf[1])
            lef.write(le_bytes)
        print('写入成功转为小端的字节流')
        of.close()
        lef.close()

    def le2txt(self):
        lef = open(self.lefile, 'rb')
        txtf = open(self.txtfile, 'w')
        #以字符串形式读取转成小端后的字节流，百度词典的起始位置为0x350
        le_bytes = lef.read().hex()[0x350:]
        i = 0
        while i<len(le_bytes):
            result = le_bytes[i:i+4]
            i+=4
            #将所有字符解码成汉字，拼音或字符
            content = binascii.a2b_hex(result).decode('utf-16-be')
            #判断汉字
            if '\u4e00' <= content <= '\u9fff':
                self.listwords.append(content)
            else:
                if self.listwords:
                    word = ''.join(self.listwords)
                    txtf.write(word + '\n')
                self.listwords = []
        print('写入txt成功')
        lef.close()
        txtf.close()

if __name__ == '__main__':
    path = r'F:\作业\词库\城市区划\安徽\安徽安康公交站.bdict'
    bd = Baidu(path)
    bd.be2le()
    bd.le2txt()


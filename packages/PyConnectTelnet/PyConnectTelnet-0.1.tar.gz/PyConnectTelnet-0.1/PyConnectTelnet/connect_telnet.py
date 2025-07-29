# -*-coding:UTF-8-*-
import telnetlib
import time


class ConnectTelnet:
    def __init__(self, ip, port=23, debug=False, encode='utf-8', timeout=8):
        # 获取login_make 字段进行排序之后按照顺序进行登陆
        self.tn = telnetlib.Telnet()
        self.encode = encode
        self.tn.open(ip, port, timeout=timeout)

        if debug:
            self.tn.set_debuglevel(10)

    def login(self, login_info, timeout=8):
        result = {}

        for key, value in login_info:
            index, re_compile, con = self.tn.expect([key.encode(self.encode)], timeout=timeout)
            self.tn.write(value.encode(self.encode) + b'\r\n')
            result[value] = con
        time.sleep(1)
        return result

    def send_command(self, commands, make_more=' ', make_enter=' ', timeout=8, ignore_decode=None, encode='utf-8'):
        result = {}
        if not isinstance(commands, list):
            return 'commands must list'
        i = 1
        for command in commands:
            i += 1
            content = b''
            self.tn.write(command.encode(encode) + b'\r\n')
            exit_make = 0
            while exit_make < 5000:
                index, re_compile, con = self.tn.expect([make_more.encode(encode)],
                                                        timeout=timeout, )
                content += con
                if index == 1:
                    self.tn.write(make_enter.encode(encode))
                else:
                    break
                exit_make += 1
            result[command] = content.decode(encode, errors=ignore_decode or 'ignore')
        return result

    def finish(self, exit_flag=None):
        result = ''
        if exit_flag:
            for exit_make, exit_write in exit_flag:
                index, re_compile, con = self.tn.expect([exit_make.encode(self.encode)], timeout=4)
                self.tn.write(exit_write.encode(self.encode) + b'\r\n')
                result += con.decode(self.encode)
            self.tn.close()
            return result
        self.tn.close()

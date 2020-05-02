"""
    作者：梁树辉
    功能：远程开机
    日期：
    版本号：
    更新：
"""
import json
import os
import struct
import socket
import time


class PowerOn(object):
    def __init__(self):
        # 定义功能列表
        self.funcs = [('添加主机', self.add_host),
                 ('选择开启主机', self.select_hosts)]
        # 判断文件是否存在
        if os.path.isfile('hosts'):
            f = open('hosts', 'r')
            self.hosts = json.load(f)
            f.close()
        else:
            self.hosts = []

    def wake_up(self):
        MAC = self.selected_host[2]
        BROADCAST = self.selected_host[1]
        if len(MAC) != 17:
            raise ValueError("MAC address should be set as form 'XX-XX-XX-XX-XX-XX'")
        mac_address = MAC.replace("-", '')
        data = ''.join(['FFFFFFFFFFFF', mac_address * 16])  # 构造原始数据格式
        send_data = b''

        # 把原始数据转换为16进制字节数组，
        for i in range(0, len(data), 2):
            send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])

        # 通过socket广播出去，为避免失败，间隔广播三次
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(send_data, (BROADCAST, 7))
            time.sleep(0.1)
            sock.sendto(send_data, (BROADCAST, 7))
            time.sleep(0.1)
            sock.sendto(send_data, (BROADCAST, 7))
            print("%s已经开机" % self.selected_host[0])
            print('')
        except Exception as e:
            print(e)

    def add_host(self):
        """添加主机函数"""
        while True:
            hostname = input('主机名：').strip()
            if hostname == 'q':
                break
            ip = input('IP：').strip()
            if ip == 'q':
                break
            mac = input('MAC（以-分隔）：')
            print('')
            if mac == 'q':
                break
            added_host = [hostname, ip, mac]
            self.hosts.append(added_host)
            f = open('hosts', 'w')
            json.dump(self.hosts, f)
            f.close()

    def interactive(self):
        """交互函数"""
        while True:
            self.show_func_menu()
            # 提供选择
            choice = input('请输入序号：').strip()
            if choice == 'q':
                break
            print('')
            if self.check_choice(choice):
                func = self.funcs[int(choice) - 1][1]
                func()

    def select_hosts(self):
        """选择开启主机"""
        while True:
            if self.hosts:
                self.show_hosts()
                print('')
                choice = input('\033[1;31m请选择主机序号（主机间可用逗号分隔）\033[0m：').strip()
                print('\n')
                if choice == 'q':
                    break
                choice_list = choice.split(',')
                for choice in choice_list:
                    if choice.isdigit():
                        choice = int(choice)
                        if (choice > 0) and (choice <= len(self.hosts)):
                            self.selected_host = self.hosts[choice - 1]
                            self.wake_up()
                        else:
                            print('没有序号为\033[1;31m%s\033[0m的主机' % choice)
                    else:
                        print('没有序号为\033[1;31m%s\033[0m的主机' % choice)
            else:
                print('没有主机在列表中！')
                break

    def show_hosts(self):
        """显示主机列表"""
        for i, host in enumerate(self.hosts):
            print('%s、%s' % (i + 1, host[0]))

    def show_func_menu(self):

        """显示功能列表"""
        # 显示列表
        for i, menu in enumerate(self.funcs):
            print('%s、%s' % (i + 1, menu[0]))

    def check_choice(self, choice):
        """检查输入"""
        # 输入的是数字
        if choice.isdigit():
            # 转换成整型
            choice = int(choice)
            if (choice > 0) and (choice <= len(self.funcs)):
                return True
            else:
                print('输入错误，请重新输入')
                return False
        # 输入了非数字
        else:
            print('输入错误，请重新输入')
            return False


poweron = PowerOn()
poweron.interactive()

"""
    作者：梁树辉
    功能：
    日期：
    版本号：
    更新：
"""
import winrm
win2012 = winrm.Session('http://10.62.34.20:5985/wsman', auth=('Administrator', 'dczx_5501'))

r = win2012.run_cmd('shutdown /s /t 1')

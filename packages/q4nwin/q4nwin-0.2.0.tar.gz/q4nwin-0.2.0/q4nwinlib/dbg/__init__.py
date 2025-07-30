# -*- coding=Latin1 -*-
import tempfile
import os
import sys
import subprocess

from q4nwinlib.context import context
from q4nwinlib.misc import showbanner,Latin1_encode,sleep,pause,color

debugger = {
    'i386': {
        'windbg': r'C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\windbg.exe',
        "windbgx": os.path.abspath(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\Microsoft.WinDbg_8wekyb3d8bbwe\WinDbgX.exe"))
    },
    'amd64': {
        'windbg': r'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\windbg.exe',
        "windbgx": os.path.abspath(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\Microsoft.WinDbg_8wekyb3d8bbwe\WinDbgX.exe"))
    }
}

debugger_init = {
    'i386': {
        'windbg': '',
        "windbgx": ""
    },
    'amd64': {
        'windbg': '',
        "windbgx": ""
    }
}


class windbg():
    @classmethod
    def attach(clx, target, script="", sysroot=None):

        showbanner('attaching', 'purple', '[=]')
        if context.windbg is None:
            windbgPath = debugger[context.arch]['windbg']
        else:
            windbgPath = context.windbg
        load_windbg = [windbgPath, '-p']

        if isinstance(target, int):
            load_windbg.append(target)
        else:
            load_windbg.append(str(target.pid))

        script = context.dbginit+'\n' + \
            debugger_init[context.arch]['windbg']+'\n'+script+'\n'
        tmp = tempfile.NamedTemporaryFile(
            prefix='winpwn_', suffix='.dbg', delete=False)
        tmp.write(Latin1_encode(script))
        tmp.flush()
        tmp.close()
        load_windbg += ['-c']             # exec command
        load_windbg += ['$$><{}'.format(tmp.name) +
                        ';.shell -x del {}'.format(tmp.name)]
        # print('script:',script)
        # print('load:',load_windbg)
        ter = subprocess.Popen(load_windbg)
        while(os.path.exists(tmp.name)):    # wait_for_debugger
            pass
        target.debugger = ter
        return ter.pid

    @classmethod
    def com(clx, com, script="", baudrate=115200):
        showbanner('attaching', 'purple', '[=]')
        if context.windbg is None:
            windbgPath = debugger[context.arch]['windbg']
        else:
            windbgPath = context.windbg
        load_windbg = [windbgPath]
        load_windbg += [
            "-k com:pipe,port={},baud={},reconnect".format(com, baudrate)]

        script = context.dbginit+'\n' + \
            debugger_init[context.arch]['windbg']+'\n'+script+'\n'
        tmp = tempfile.NamedTemporaryFile(
            prefix='winpwn_', suffix='.dbg', delete=False)
        tmp.write(Latin1_encode(script))
        tmp.flush()
        tmp.close()
        load_windbg += ['-c']             # exec command
        load_windbg += ['"$$><{}'.format(tmp.name) +
                        ';.shell -x del {}"'.format(tmp.name)]
        # ter=subprocess.Popen(Latin1_encode(' '.join(load_windbg)))
        ter = subprocess.Popen(' '.join(load_windbg))
        while(os.path.exists(tmp.name)):    # wait_for_debugger
            sleep(0.05)
            # pass
        # target.debugger=ter
        # mark('attached')
        return ter.pid

    @classmethod
    def net(clx):
        pass


class windbgx():
    @classmethod
    def attach(clx, target, script="", sysroot=None):
        showbanner('attaching', 'purple', '[=]')
        if context.windbgx is None:
            windbgxPath = debugger[context.arch]['windbgx']
        else:
            windbgxPath = context.windbgx

        load_windbg = [windbgxPath, '-p']

        if isinstance(target, int):
            load_windbg.append(str(target))
        else:
            load_windbg.append(str(target.pid))

        script = context.dbginit+'\n' + \
            debugger_init[context.arch]['windbgx']+'\n'+script+'\n'

        tmp = tempfile.NamedTemporaryFile(
            prefix='winpwn_', suffix='.dbg', delete=False)
        tmp.write(Latin1_encode(script))
        tmp.flush()
        tmp.close()
        load_windbg += ['-c']             # exec command
        load_windbg += ['"$$><{}'.format(tmp.name) +
                        ';.shell -x del {}"'.format(tmp.name)]
        
        # print('script:',script)
        # print('load:',load_windbg)
        ter = subprocess.Popen(' '.join(load_windbg))
        while(os.path.exists(tmp.name)):    # wait_for_debugger
            pass

        if not isinstance(target, int):
            target.debugger = ter

        # mark('attached')
        return ter.pid

    @classmethod
    def remote(clx, target, script=""):
        showbanner('attaching', 'purple', '[=]')
        if context.windbgx is None:
            windbgxPath = debugger[context.arch]['windbgx']
        else:
            windbgxPath = context.windbgx

        IP = ''
        port = 1025
        if ',' in target:
            idx = target.find(',')
            IP = target[0:target.find(',')]
            port = int(target[target.find(',')+1:])
        else:
            IP = target

        load_windbg = [windbgxPath]
        load_windbg += [
            "-premote tcp:server={},port={}".format(IP, port)]

        script = context.dbginit+'\n' + \
            debugger_init[context.arch]['windbgx']+'\n'+script+'\n'
        tmp = tempfile.NamedTemporaryFile(
            prefix='winpwn_', suffix='.dbg', delete=False)
        tmp.write(Latin1_encode(script))
        tmp.flush()
        tmp.close()
        load_windbg += ['-c']             # exec command
        load_windbg += ['"$$><{}'.format(tmp.name) +
                        ';.shell -x del {}"'.format(tmp.name)]

        
        ter = subprocess.Popen(' '.join(load_windbg))
        while(os.path.exists(tmp.name)):    # wait_for_debugger
            sleep(0.05)
        return ter.pid

    @classmethod
    def com(clx, com, script="", baudrate=115200):
        showbanner('attaching', 'purple', '[=]')
        if context.windbgx is None:
            windbgxPath = debugger[context.arch]['windbgx']
        else:
            windbgxPath = context.windbgx
        load_windbg = [windbgxPath]
        load_windbg += [
            "-k com:pipe,port={},baud={},reconnect".format(com, baudrate)]

        script = context.dbginit+'\n' + \
            debugger_init[context.arch]['windbgx']+'\n'+script+'\n'
        tmp = tempfile.NamedTemporaryFile(
            prefix='winpwn_', suffix='.dbg', delete=False)
        tmp.write(Latin1_encode(script))
        tmp.flush()
        tmp.close()
        load_windbg += ['-c']             # exec command
        load_windbg += ['"$$><{}'.format(tmp.name) +
                        ';.shell -x del {}"'.format(tmp.name)]
        # ter=subprocess.Popen(Latin1_encode(' '.join(load_windbg)))
        ter = subprocess.Popen(' '.join(load_windbg))
        while(os.path.exists(tmp.name)):    # wait_for_debugger
            sleep(0.05)
        return ter.pid

    @classmethod
    def net(clx, key, script = ""):
        showbanner('attaching', 'purple', '[=]')
        if context.windbgx is None:
            windbgxPath = debugger[context.arch]['windbgx']
        else:
            windbgxPath = context.windbgx

        IP = ''
        port = 50000
        if ',' in key:
            idx = key.find(',')
            IP = key[0:key.find(',')]
            port = int(key[key.find(',')+1:])
        else:
            IP = key

        load_windbg = [windbgxPath]
        load_windbg += [
            "-k net:port={},key={}".format(port, key)]

        script = context.dbginit+'\n' + \
            debugger_init[context.arch]['windbgx']+'\n'+script+'\n'
        tmp = tempfile.NamedTemporaryFile(
            prefix='winpwn_', suffix='.dbg', delete=False)
        tmp.write(Latin1_encode(script))
        tmp.flush()
        tmp.close()
        load_windbg += ['-c']             # exec command
        load_windbg += ['"$$><{}'.format(tmp.name) +
                        ';.shell -x del {}"'.format(tmp.name)]
        
        # print('[debug] load_windbg:', load_windbg)
        ter = subprocess.Popen(' '.join(load_windbg))
        while(os.path.exists(tmp.name)):    # wait_for_debugger
            sleep(0.05)
        return ter.pid



def init_debugger():
    sc_base = os.path.dirname(os.path.abspath(__file__))


    ext_path = os.path.join(sc_base, "..", "..", "q4nwinext", "windbg_init.py")
    ext_path = os.path.abspath(ext_path)

    # pykd_x64_dll_path = os.path.join(sc_base, "..", "..", "q4nwinext", "pykd", "pykd_ext", "pykd_ext_2.0.0.25_x64", "pykd.dll")
    # pykd_x86_dll_path = os.path.join(sc_base, "..", "..", "q4nwinext", "pykd", "pykd_ext", "pykd_ext_2.0.0.25_x86", "pykd.dll")

    # patch
    pykd_x64_dll_path = os.path.join(sc_base, "..", "..", "q4nwinext", "pykd", "pykd.pyd")
    pykd_x86_dll_path = os.path.join(sc_base, "..", "..", "q4nwinext", "pykd", "pykd.pyd")

    pykd_x64_dll_path = os.path.abspath(pykd_x64_dll_path)
    pykd_x86_dll_path = os.path.abspath(pykd_x86_dll_path)

    # print("[debug]", pykd_x64_dll_path)

    cmdline_x64 = f".load {pykd_x64_dll_path};!py -g {ext_path};"
    cmdline_x86 = f".load {pykd_x86_dll_path};!py -g {ext_path};"


    debugger_init['i386']['windbg'] = cmdline_x86
    debugger_init['i386']['windbgx'] = cmdline_x86

    debugger_init['amd64']['windbg'] = cmdline_x64
    debugger_init['amd64']['windbgx'] = cmdline_x64


init_debugger()
import base64
import os
import time

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *

debug = False

'''
Suma Vote Server

Open Source To Github ： 2023-02-05
祝元宵节快乐

Version: 1.1 / 2023-1-14
Description: Bad Bug Fix & Path Issue
Detail: 修复了在恶意多开的情况下可以实现多次报名的漏洞
        修复了在Linux下的路径报错问题
        完善了定时开关服务器的功能

Version: 1.0 / 2023-1-9
Description: Created Release from Test Branch
'''


def sc_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def file_path(name):
    if name == 'logger':
        a = str(w_path) + "\\dynamic\\log.txt"
    elif name == 'db':
        a = str(w_path) + "\\dynamic\\database.txt"
    elif name == 'used_qq_list':
        a = str(w_path) + "\\dynamic\\qq.txt",
    elif name == 'used_song_list':
        a = str(w_path) + "\\dynamic\\songs.txt"
    elif name == 'used_qq':
        a = str(w_path) + "\\dynamic\\qq.txt"
    elif name == 'used_song':
        a = str(w_path) + "\\dynamic\\songs.txt",
    elif name == 'bands':
        a = str(w_path) + "\\static\\bands.txt",
    elif name == 'songs_ppp':
        a = str(w_path) + "\\static\\ppp.txt",
    elif name == 'songs_ag':
        a = str(w_path) + "\\static\\ag.txt",
    elif name == 'songs_pp':
        a = str(w_path) + "\\static\\pp.txt",
    elif name == 'songs_r':
        a = str(w_path) + "\\static\\r.txt",
    elif name == 'songs_hhw':
        a = str(w_path) + "\\static\\hhw.txt",
    elif name == 'songs_m':
        a = str(w_path) + "\\static\\m.txt",
    elif name == 'songs_ras':
        a = str(w_path) + "\\static\\ras.txt",
    elif name == 'songs_agn':
        a = str(w_path) + "\\static\\agn.txt",
    elif name == 'songs_other':
        a = str(w_path) + "\\static\\other.txt",
    else:
        a = ''

    if sys_env == 1:
        b = str(a.__str__())
        b = b.replace('\\\\', '\\')
        b = b.replace("('", '')
        b = b.replace("',)", '')
        b = b.replace('\\\\', '\\')
        # print(str(b))
        return str(b)
    elif sys_env == 2:
        b = a.replace('\\', '/')
        # print(str(b))
        return str(b)


def check_qq(qq):
    if qq < 0:
        qq = -qq
    qq = int(qq)
    qq = str(qq)
    if len(qq) < 5 or len(qq) > 11:
        return 'QQ号格式错误'
    else:
        return None


def file2list(path, logger, filter):
    try:
        fp = open(path, mode='r', encoding='utf-8')
        lns = fp.readlines()
        fp.close()
        lo = []
        li = []
        for k in lns:
            a = k.replace('\n', '')
            lo.append(a)
        for d in lo:
            if d not in filter:
                li.append(d)
        return li
    except:
        logger.write(sc_time() + " | File open error" + '\n')
        return []
        pass


def handle_main():
    lg_s = sc_time() + ' | New User' + ' | ' + info.user_ip + ' | ' + info.user_language + ' | ' + info.user_agent.__str__()
    print(lg_s)

    logger.write(lg_s+'\n')
    logger.flush()

    set_env(title='报名表', output_animation=True, auto_scroll_bottom=True)

    if time.time() < server_open_stamp:
        put_info("服务器开始时间:%r，请勿重复刷新" % server_open_str)
        return

    elif time.time() > server_close_stamp:
        put_info("服务器已关闭:%r " % server_open_str)
        return

    put_info("报名系统BETA  访问时间：%r\n" % sc_time())
    put_text("QQ号为报名的唯一凭证，请确保进群哦\n"
             "每个QQ号码仅能提交一次，若需要变更请联系管理\n"
             "想回到上一步的话，请刷新页面\n"
             "----\n")

    put_text("公告：暂无公告\n"
             "----\n")

    put_text("目前已被选择的歌曲有：\n")
    for i in used_song_list:
        put_text(i)
    put_text("----\n")

    put_info("步骤1：基础信息")
    qq_num = input("QQ号码", type=NUMBER, validate=check_qq)
    qq_num = abs(qq_num)
    qq_num = int(qq_num)
    qq_num = str(qq_num)

    if qq_num in used_qq_list:
        put_text("该号码已被使用！请刷新页面重试")
        lr = sc_time() + ' | Rejected User:' + qq_num
        logger.write(lr)
        print(lr)
        return
    else:
        # put_text("成功")
        pass

    put_text("已输入：%r" % qq_num)

    put_info("步骤2-1：选择乐队")
    band = select('歌曲所在的乐队，如不确定则可查询文档或者群内咨询', bands)
    put_text("已选：%r" % band)

    # band = band.replace('\n', '')

    # print(band)

    put_info("步骤2-2：选择歌曲")
    if band == "Poppin'Party":
        song = select('请选择想要报名的歌曲', songs_ppp)
        songs_ppp.remove(song)

    elif band == "Afterglow":
        song = select("请选择想要报名的歌曲", songs_ag)
        songs_ag.remove(song)

    elif band == "ハロー、ハッピーワールド！":
        song = select("请选择想要报名的歌曲", songs_hhw)
        songs_hhw.remove(song)

    elif band == "Pastel＊Palettes":
        song = select("请选择想要报名的歌曲", songs_pp)
        songs_pp.remove(song)

    elif band == "Roselia":
        song = select("请选择想要报名的歌曲", songs_r)
        songs_r.remove(song)

    elif band == "RAISE A SUILEN":
        song = select("请选择想要报名的歌曲", songs_ras)
        songs_ras.remove(song)

    elif band == "Morfonica":
        song = select("请选择想要报名的歌曲", songs_m)
        songs_m.remove(song)

    elif band == "ARGONAVIS":
        song = select("请选择想要报名的歌曲", songs_agn)
        songs_agn.remove(song)

    else:
        song = select("请选择想要报名的歌曲", songs_other)
        songs_other.remove(song)

    put_text("已选：%r" % song)

    lt = sc_time() + ' | ' + qq_num + ' | ' + band + ' | ' + song
    print(lt)
    blt = lt.encode('utf-8')
    blt64 = base64.encodebytes(blt)
    lt64 = blt64.decode('utf-8')
    lt64d = lt64.replace('\n', '')

    if qq_num in used_qq_list:
        put_text("该号码已被使用！请刷新页面重试")
        lr = sc_time() + ' | Rejected User:' + qq_num + '2_PASS_ALERT'
        logger.write(lr)
        print(lr)
        return
    else:
        # put_text("成功")
        pass

    put_text("您的报名号为：%r" % lt64d)
    put_info("您的报名信息已经提交，可以关闭页面了")
    dwl = sc_time() + '|' + qq_num + '|' + band + '|' + song + '|' + lt64
    dwl = dwl.replace('\n','')
    # print(dwl)
    db.write(dwl+'\n')

    used_song_list.append(song)
    used_qq_list.append(qq_num)
    used_qq.write(qq_num + '\n')
    used_song.write(song + "\n")

    logger.flush()
    db.flush()
    used_qq.flush()
    used_song.flush()


if __name__ == '__main__':
    print("Suma Vote Release 1.1 Initing...")

    # Path Config
    sys_env = 0
    w_path = os.getcwd()
    if '\\' in w_path:
        sys_env = 1
        print('Cwd Mode : Windows')
    elif '/' in w_path:
        sys_env = 2
        print('Cwd Mode : Linux')
    else:
        print('Cwd Detect Failed')

    # open Log and Data
    logger = open(file_path('logger'), mode='a', encoding='utf-8', buffering=8192)
    db = open(file_path('db'), mode='a', encoding='utf-8', buffering=8192)
    # load Config
    used_qq_list = file2list(file_path('used_qq_list'), logger=logger, filter=[])
    used_song_list = file2list(file_path('used_song_list'), logger=logger, filter=[])
    # open Config
    used_qq = open(file_path('used_qq'), mode='a+', encoding='utf-8')
    used_song = open(file_path('used_song'), mode='a+', encoding='utf-8')
    # load Resources
    bands = file2list(file_path('bands'), logger=logger, filter=used_song_list)
    songs_ppp = file2list(file_path('songs_ppp'), logger=logger, filter=used_song_list)
    songs_ag = file2list(file_path('songs_ag'), logger=logger, filter=used_song_list)
    songs_pp = file2list(file_path('songs_pp'), logger=logger, filter=used_song_list)
    songs_r = file2list(file_path('songs_r'), logger=logger, filter=used_song_list)
    songs_hhw = file2list(file_path('songs_hhw'), logger=logger, filter=used_song_list)
    songs_m = file2list(file_path('songs_m'), logger=logger, filter=used_song_list)
    songs_ras = file2list(file_path('songs_ras'), logger=logger, filter=used_song_list)
    songs_agn = file2list(file_path('songs_agn'), logger=logger, filter=used_song_list)
    songs_other = file2list(file_path('songs_other'), logger=logger, filter=used_song_list)

    print('已报名的qq：' + str(len(used_qq_list)))
    if debug:
        for i in used_qq_list:
            print(i)

    # 配置开关服务器时间
    server_open_str = '2023-01-09 12:00:00'
    server_close_str = '2023-01-29 23:00:00'

    server_open_stamp = int(time.mktime(time.strptime(server_open_str, '%Y-%m-%d %H:%M:%S')))
    server_close_stamp = int(time.mktime(time.strptime(server_close_str, '%Y-%m-%d %H:%M:%S')))

    print('正在启动服务器...')
    # start_server(handle_main, port=8080, debug=True)
    start_server(handle_main, port=7000, debug=False)

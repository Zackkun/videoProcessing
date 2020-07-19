import subprocess
import os
import shutil
from Tensorflow import detect_voc2012 as dv
from Fragment_mothed import videoMethod_1, videoMethod_2
Zhen_path = ".\\data\\Zhen\\"
cut_path = ".\\data\\cutVideo\\"
guochang_path = ".\\data\\guoChang\\"
ts_path = ".\\data\\ts\\"
cutVideotxt = ".\\data\\ts\\cut_video.txt"
#获取用户上传的视频文件
def setData(source_path, target_path, mothed=2, intervals = False):
    videoDatadict = {}
    intervalsPath = None
    with open('videoData.txt', 'r') as f1:
        t = f1.read()
        if len(t):
            Data = eval(t)
            if Data['Soure'] == source_path:
                videoDatadict = Data
            else:
                size, fps, vcodec, acodec = getVideodata(source_path)
                videoDatadict = {'Soure': source_path, 'Size': size, 'Fps': fps, 'Vcodec': vcodec, 'Acodec': acodec}
                with open('videoData.txt', 'w+') as f2:
                    f2.write(str(videoDatadict))
        else:
            size, fps, vcodec, acodec = getVideodata(source_path)
            videoDatadict = {'Soure': source_path, 'Size': size, 'Fps': fps, 'Vcodec': vcodec, 'Acodec': acodec}
            with open('videoData.txt', 'w+') as f3:
                f3.write(str(videoDatadict))

    if intervals:
        intervalsPath = video_intervals(videoDatadict)

    filtrateData(source_path)
    cklist, delist = dv(Zhen_path)
    if mothed == 1:
        temp = videoMethod_1(cklist)
        cut_video_1(source_path, temp, intervalsPath)
    elif mothed == 2:
        cktemp, detemp = videoMethod_2(cklist, delist)
        cut_video_2(source_path, cktemp, detemp, intervalsPath)
    else:
        print('error')
        return -1

    generate_video(cutVideotxt, target_path)
    return target_path

#供用户下载处理好的视频
def getData():
    return

#对视频文件进行一秒一帧的图片截取，返回截取后的数据集和时间戳
def filtrateData(video_path):
    path = Zhen_path.rstrip('\\')
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)
    subprocess.run("ffmpeg -i %s -r 1 -f image2 %s.jpeg -y" % (video_path, Zhen_path + '%05d'))
    fileList = os.listdir(Zhen_path)
    n = 0
    for i in fileList:
        oldname = Zhen_path + fileList[n]
        m = int(fileList[n].split('.')[0])
        newname = Zhen_path + "%02d-%02d-%02d.jpeg" % ((m // 3600), (m % 3600 // 60), (m % 60))
        os.rename(oldname, newname)
        fileList[n] = newname
        print(oldname, '======>', newname)
        n += 1
    #删除最后一帧
    print('delete' + fileList[n-1])
    os.remove(fileList[n-1])
    return 0
#生成过程动画
def video_intervals(videoDatadict):
    size = videoDatadict['Size']
    fps = videoDatadict['Fps']
    vcodec = videoDatadict['Vcodec']
    acodec = videoDatadict['Acodec']

    subprocess.run("ffmpeg -f lavfi -t 2 -i anullsrc %smute.mp4 -y" % guochang_path)

    w, h = size.split('x')
    subprocess.run(
        "ffmpeg -i %sguochang.PNG -vf scale=%s:%s %sguochang2.jpg -y" % (guochang_path, w, h, guochang_path))

    subprocess.run(
        "ffmpeg -loop 1 -f image2 -i %sguochang2.jpg -i %smute.mp4 -t 2 -vcodec %s -acodec %s -r %d %sguochang3.mp4 -y"
        % (guochang_path, guochang_path, vcodec, acodec, fps, guochang_path))

    temp = '%sguochang3.mp4' % guochang_path
    subprocess.run(
        "ffmpeg -i %s -f mpegts -vcodec copy -acodec copy -vbsf h264_mp4toannexb -y %s.ts" % (
            temp, guochang_path + 'guochang3'))
    intervalsPath = '%sguochang3.ts' % guochang_path
    return intervalsPath

def getVideodata(source_path):
    size = None
    fps = None
    vcodec = None
    acodec = None

    cmd = "ffprobe -print_format json -select_streams v %s" % source_path
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

    list = str(p.stdout.read()).split(r"\n")

    list2 = []
    for _ in list:
        if 'Stream' in _:
            list2.append(_)

    for data in list2:
        if "#0:0" in data:
            list3 = data.split(",")
            vcodec = list3[0].split(':')[3].split('(')[0].replace(' ', '')
            list3.pop(0)
            for _ in list3:
                if "x" in _:
                    size = _.split('[')[0].replace(' ', '')
                    break
            for _ in list3:
                if "fps" in _:
                    fps = _.replace('fps', '')
                    fps = round(float(fps))
                    break

        elif "#0:1" in data:
            list4 = data.split(',')
            acodec = list4[0].split(':')[3].split('(')[0].replace(' ', '')

    return size, fps, vcodec, acodec

#根据筛选好的时间戳对视频文件进行截取拼接
def cut_video_1(source_path, list, interval = None):
    cutVideo_path = cut_path.rstrip('\\')
    if not os.path.exists(cutVideo_path):
        os.mkdir(cutVideo_path)
    else:
        shutil.rmtree(cutVideo_path)
        os.mkdir(cutVideo_path)
    with open(cutVideotxt, 'w+') as f0:
        print('清空文本')
    with open(cutVideotxt, 'a+') as f:

        for time_Fragment in list:
            strs = "%02d%02d%02d-%02d%02d%02d" % (time_Fragment[0], time_Fragment[1], time_Fragment[2],
                                                  time_Fragment[3], time_Fragment[4], time_Fragment[5])
            subprocess.run("ffmpeg -ss %02d:%02d:%02d -i %s -to %02d:%02d:%02d -c copy -copyts %s%s.mp4 -y" %
                           (time_Fragment[0], time_Fragment[1], time_Fragment[2], source_path,
                            time_Fragment[3], time_Fragment[4], time_Fragment[5], cut_path, strs))

            f.write('file'+' '+'\''+cut_path + strs + '.mp4' + '\'' + '\n')
            if interval:
                f.write('file'+' '+'\''+interval + '\'' + '\n')

    return


def cut_video_2(source_path, cklist, delist, interval=None):
    cutVideo_path = cut_path.rstrip('\\')
    if not os.path.exists(cutVideo_path):
        os.mkdir(cutVideo_path)
    else:
        shutil.rmtree(cutVideo_path)
        os.mkdir(cutVideo_path)
    tsVideo_path = ts_path.rstrip('\\')
    if not os.path.exists(tsVideo_path):
        os.mkdir(tsVideo_path)
    else:
        shutil.rmtree(tsVideo_path)
        os.mkdir(tsVideo_path)
    #size, fps, vcodec, acodec = getVideodata(source_path)
    for time_Fragment1 in delist:
        strs1 = "d%02d%02d%02d-%02d%02d%02d" % (time_Fragment1[0], time_Fragment1[1], time_Fragment1[2],
                                                    time_Fragment1[3], time_Fragment1[4], time_Fragment1[5])
        strs2 = "%02d%02d%02d-%02d%02d%02d" % (time_Fragment1[0], time_Fragment1[1], time_Fragment1[2],
                                                   time_Fragment1[3], time_Fragment1[4], time_Fragment1[5])

        subprocess.run("ffmpeg -ss %02d:%02d:%02d -i %s -to %02d:%02d:%02d -c copy -copyts %s%s.mp4 -y" %
                       (time_Fragment1[0], time_Fragment1[1], time_Fragment1[2], source_path,
                        time_Fragment1[3], time_Fragment1[4], time_Fragment1[5], cut_path, strs1))
        subprocess.run("ffmpeg -i %s.mp4 -vf scale=160:-1 %s.mp4 -y" % (cut_path+strs1, cut_path+strs2))
        os.remove(cut_path+strs1+'.mp4')
        subprocess.run(
            "ffmpeg -i %s.mp4 -f mpegts -vcodec copy -acodec copy -vbsf h264_mp4toannexb %s.ts -y" % (
                cut_path+strs2, ts_path+strs2))

    for time_Fragment2 in cklist:
        strs3 = "%02d%02d%02d-%02d%02d%02d" % (time_Fragment2[0], time_Fragment2[1], time_Fragment2[2],
                                                   time_Fragment2[3], time_Fragment2[4], time_Fragment2[5])
        subprocess.run("ffmpeg -ss %02d:%02d:%02d -i %s -to %02d:%02d:%02d -c copy -copyts %s%s.mp4 -y" %
                       (time_Fragment2[0], time_Fragment2[1], time_Fragment2[2], source_path,
                        time_Fragment2[3], time_Fragment2[4], time_Fragment2[5], cut_path, strs3))
        subprocess.run(
            "ffmpeg -i %s.mp4 -f mpegts -vcodec copy -acodec copy -vbsf h264_mp4toannexb %s.ts -y" % (
                cut_path + strs3, ts_path + strs3))


    alllist = cklist + delist
    alllist.sort()
    with open(cutVideotxt, 'w+') as f0:
        print('清空文本')
    with open(cutVideotxt, 'a+') as f:
        for time_Fragment in alllist:
            strs = "%02d%02d%02d-%02d%02d%02d.ts" % (time_Fragment[0], time_Fragment[1], time_Fragment[2],
                                                       time_Fragment[3], time_Fragment[4], time_Fragment[5])

            f.write('file' + ' ' + '\'' + ts_path + strs + '\'' + '\n')
            if interval:
                f.write('file' + ' ' + '\'' + interval + '\'' + '\n')

    return

def generate_video(videotxt, target_path):
    subprocess.run("ffmpeg -f concat -safe 0 -i %s -c copy %s -y" % (videotxt, target_path))






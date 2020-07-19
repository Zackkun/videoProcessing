from operator import eq
import numpy as np

"""
剪切拼接方法1，将连续的时间戳组合成一个时间段，视频会更加连贯，减少丢帧、重复帧的情况
"""
def videoMethod_1(timeFragment):
    ckTime, moveTime = timeFragmentMethod_1(timeFragment)
    ckTime = timeFragmentMethod_3(ckTime)

    return ckTime

def videoMethod_2(cktimeFragment, detimeFragment):
    ckTime, ckmoveTime = timeFragmentMethod_1(cktimeFragment, False)
    deTime, demoveTime = timeFragmentMethod_1(detimeFragment)
    #暂时弥补单秒问题
    ckNew = timeFragmentMethod_2(ckTime, demoveTime)
    move = []
    for point in ckNew:
        if eq(point[:3], point[3:]):
            move.append(point)
    if len(move):
        for x in move:
            ckNew.remove(x)
        move_np = np.array(move)
        move_temp = move_np[:, 0:3].tolist()
        for point2 in ckNew:
            temp = point2[3:]
            temp[2] += 1
            if temp[2] == 60:
                temp[1] += 1
                temp[2] = 0
                if temp[2] == 60:
                    temp[0] += 1
                    temp[1] = 0
            if temp in move_temp:
                point2[3:] = temp
                move_temp.remove(temp)
            if len(move_temp):
                pass
            else:
                break

    ckNew = timeFragmentMethod_3(ckNew)
    deTime = timeFragmentMethod_3(deTime)
    return ckNew, deTime

def timeFragmentMethod_3(Time):
    lens = len(Time)
    if lens < 2:
        pass
    else:
        for i in range(lens-1):
            temp = Time[i][3:]
            temp2 = Time[i+1][0:3]
            temp[2] += 1
            if temp[2] == 60:
                temp[1] += 1
                temp[2] = 0
                if temp[2] == 60:
                    temp[0] += 1
                    temp[1] = 0
            move = []
            if eq(temp, temp2):
                move.append(Time[i])
                Time[i+1][0:3] = Time[i][0:3]

        if len(move):
            for x in move:
                Time.remove(x)
    return Time

def timeFragmentMethod_2(Time, move):
    move_np = np.array(move)
    move_temp = move_np[:, 0:3].tolist()
    for point in Time:
        temp = point[3:]
        temp[2] += 1
        if temp[2] == 60:
            temp[1] += 1
            temp[2] = 0
            if temp[2] == 60:
                temp[0] += 1
                temp[1] = 0
        if temp in move_temp:
            point[3:] = temp
            move_temp.remove(temp)
        if len(move_temp):
            pass
        else:
            break
    return Time

def timeFragmentMethod_1(list, removeCheck = True):
    Time = []
    for name in list:
        time = name.split('.')[0].split('-')
        time = [int(x) for x in time]
        if Time:
            Temp = Time[-1][3:]
            Temp[2] += 1
            if Temp[2] == 60:
                Temp[1] += 1
                Temp[2] = 0
                if Temp[2] == 60:
                    Temp[0] += 1
                    Temp[1] = 0

            if eq(Temp, time):
                Time[-1][3:] = time[:]
            else:
                Time.append(time + time)
        else:
            temp = time + time
            Time.append(temp)
    move = []
    for point in Time:
        if eq(point[:3], point[3:]):
            move.append(point)
    if len(move) and removeCheck:
        for x in move:
            Time.remove(x)


    return Time, move

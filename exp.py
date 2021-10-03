#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors, gui
from psychopy.sound import Sound
import helpers as hp
import numpy as np
import pandas as pd


# GUI
myDlg = gui.Dlg(title=u"实验")
myDlg.addText(u'被试信息')
myDlg.addField('姓名:')
myDlg.addField('性别:', choices=['male', 'female'])
myDlg.addField('年龄:', 21)
# A: expand, B: shrink, C: large, D: small
myDlg.addField('屏幕分辨率:', choices=['1920*1080', '3200*1800', '1280*720', '2048*1152', '2560*1440'])
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if not myDlg.OK:
    core.quit()
name = ok_data[0]
sex = ok_data[1]
age = ok_data[2]
resolution = ok_data[3]

w, h = resolution.split('*')
w = int(w)
h = int(h)
a = h/720
results = {
    'balloon':[], 'break_point':[], 'choice':[], 'money':[], 'total':[],
    'last': [], 'rt': [], 'status':[]
    }
df = hp.generate(n_trial=30, max_pump=128)
df['pix_w'] = w
df['pix_h'] = h

win = visual.Window(size=(w, h), fullscr=True, units='pix', color=[0, 0, 0])
color = np.array([34, 74, 132])*2/255 - 1
# Buttons
button_pump = hp.Button(
    text= visual.TextStim(win, text=u'充气', height=36*a, wrapWidth=10000),
    shape= visual.Rect(win, lineColor=[0.8, 0.8, 0.8], lineWidth=2)
)
button_gather = hp.Button(
    text= visual.TextStim(win, text=u'收钱', height=36*a, wrapWidth=10000),
    shape= visual.Rect(win, lineColor=[0.8, 0.8, 0.8], lineWidth=2)
)
button_pump.set_pos(pos=(0, -240*a), size=(240*a, 60*a))
button_gather.set_pos(pos=(-300*a, -240*a), size=(240*a, 60*a))

# Balloon
balloon = hp.Balloon(
    img=visual.ImageStim(win, image='img/balloon_blue0.png'),
    shape=visual.Rect(
        win, lineColor=color, fillColor=color, lineWidth=2,
        pos=(0, -240*a+30*a+30*a), size=(30*a, 60*a)),
    bottom_pos=(0, (-240+30+50)*a),
    size=720*a/6
)

# Text
text = visual.TextStim(win, height=64 * h / 720, pos=(0, 0), wrapWidth=10000)
info_total = visual.TextStim(win, height=36*a, pos=(400*a, -120*a), wrapWidth=10000)
info_last = visual.TextStim(win, height=36*a, pos=(400*a, -240*a), wrapWidth=10000)

# Sound
bang = Sound('sound/bang.wav')

# 指导语

# 实验
clk = core.Clock()
myMouse = event.Mouse()
text.text = '按【空格键】进入正式实验'
text.draw()
win.flip()
key = event.waitKeys(keyList=['space', 'escape'])
if 'escape' in key:
    win.close()
    core.quit()

money_total = 0
money_last = 0
for i in range(len(df)):
    break_point = df['break_point'][i]
    money = 0
    balloon.reset()
    button_gather.txt.text = u'收取%s分' % money
    info_total.text = u'已获得%s分' % money_total
    info_last.text = u'上次获得%s分' % money_last

    button_pump.draw()
    button_gather.draw()
    balloon.draw()
    info_total.draw()
    info_last.draw()
    win.flip()
    clk.reset()
    for j in range(break_point):
        key = event.waitKeys(keyList=['f', 'j', 'escape'])
        rt = clk.getTime()
        results['rt'].append(rt)
        results['balloon'].append(i)
        results['break_point'].append(break_point)
        results['total'].append(money_total)
        results['last'].append(money_last)
        results['money'].append(money)
        if 'escape' in key:
            win.close()
            core.quit()
        elif 'f' in key:   # gather money
            results['choice'].append(0)
            results['status'].append('gather')
            money_total += money
            money_last = money
            break
        elif 'j' in key:   # pump
            results['choice'].append(1)
            if j != break_point-1:
                balloon.pump(r_change=10 * a)
                money += 1
                button_gather.txt.text = u'收取%s元' % money
                results['status'].append('pump')
                button_pump.draw()
                button_gather.draw()
                balloon.draw()
                info_total.draw()
                info_last.draw()
                win.flip()
            else:
                bang.play()
                money_last = 0
                results['status'].append('bang')
                for k in range(6):
                    balloon.img.image = 'img/balloon_blue%s.png'%k
                    button_pump.draw()
                    balloon.draw()
                    win.flip()
                core.wait(0.2)
                bang.stop()
                balloon.img.image = 'img/balloon_blue0.png'
        clk.reset()

data = pd.DataFrame(results)
data['name'] = name
data['sex'] = sex
data['age'] = age
data['trial'] = np.arange(len(data))+1
data.to_csv('data/%s_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))
text.text = "本实验结束，请呼叫主试"
text.draw()
win.flip()
core.wait(3)
win.close()
core.quit()
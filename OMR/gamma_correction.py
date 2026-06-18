MONITOR_SIZE = 1920, 1080
MONITOR_ID   = 0
N_POINT      = 5

import numpy as np
import matplotlib.pyplot as pp
from psychopy import visual, monitors

def measure(npoint = N_POINT):
    win = visual.Window(size         = MONITOR_SIZE,
                        screen       = MONITOR_ID,
                        allowGUI     = False,
                        waitBlanking = False,
                        fullscr      = False,
                        allowStencil = True)
    
    rct    = visual.Rect(win, width = MONITOR_SIZE[0], height = MONITOR_SIZE[1], units = 'pix', colorSpace = 'rgb255')
    gscale = np.linspace(0, 255, npoint)
    v      = []
    for g in gscale:
        rct.color = g
        rct.draw()
        win.flip()
        v.append(float(input('value? >> ')))
    win.close()
    
    gamma = monitors.GammaCalculator(inputs = gscale, lums = v).gamma
    
    print('m = %f'%v[0])
    print('M = %f'%v[-1])
    print('gamma = %f'%gamma)
    print('npoint = %d'%npoint)
    
    return v[0], v[-1], gamma, npoint

def evaluate(m = 0, M = 70, gamma = 2.2, npoint = N_POINT):
    win = visual.Window(size         = MONITOR_SIZE,
                        screen       = MONITOR_ID,
                        gamma        = gamma,
                        allowGUI     = False,
                        waitBlanking = False,
                        fullscr      = False,
                        allowStencil = True)
    
    rct    = visual.Rect(win, width = MONITOR_SIZE[0], height = MONITOR_SIZE[1], units = 'pix', colorSpace = 'rgb255')
    gscale = np.linspace(0, 255, npoint)
    est    = m+(M-m)*np.linspace(0, 1, npoint)
    v      = []
    for g, e in zip(gscale, est):
        rct.color = g
        rct.draw()
        win.flip()
        v.append(float(input('estimated = %f: measured = '%e)))
    win.close()
    
    pp.plot(est, v, 'ko')
    pp.plot([0, M], [0, M], 'r')
    pp.xlabel('Estimated')
    pp.ylabel('Measured')
    pp.show()

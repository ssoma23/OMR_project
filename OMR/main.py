# Grating stimulation for OKR recording (multiple monitors)

"""
#Screen/stimulus tearing: only on Linux? -> Not observed on Win10.
#Screen refresh timing save
#Data save
#Trigger detector
"""

import os
import sys
import time   as tm
#import numpy  as np
#import pickle as pc
#from psychopy import monitors, visual, clock
from psychopy import visual, monitors
from config import *

import PyQt6.QtWidgets as qw
import PyQt6.QtCore    as qc
import PyQt6.QtGui     as qg

import multiprocessing as mp

def stimulation():
    mon = monitors.Monitor(MONITOR_NAME)
    mon.setDistance(MONITOR_DISTANCE)
    mon.setGamma(MONITOR_GAMMA)
    mon.setSizePix(MONITOR_RESOLUTION)
    mon.setWidth(MONITOR_SIZE[0])
    
    win = visual.Window(size         = MONITOR_RESOLUTION,
                        monitor      = mon,
                        units        = 'deg',
                        screen       = MONITOR_ID,
                        allowGUI     = False,
                        waitBlanking = False,
                        fullscr      = False,
                        allowStencil = True)
    
    #ct = ...
    #sf = ...
    #tf = ...
    
    stm = visual.GratingStim(win,
                             size = 100,
                             contrast = 1,
                             sf = 1)
    tf = 1
    
    # any break acceptance
    # interruption/update acceptance
    while True:
        stm.phase += tf/MONITOR_REFRESH_RATE
        stm.draw()
        win.flip()

class StimulationProcess():
    def __init__(self, vis = False, ct = 1, sf = 1, tf = 1):
        super().__init__()
        self.process  = mp.Process(target = self.run)
        
        self.vis      = mp.Value('B', vis)
        self.ct       = mp.Value('d', ct)
        self.sf       = mp.Value('d', sf)
        self.tf       = mp.Value('d', tf)
        self.flag_run = mp.Value('B', False)
    
    def start(self):
        self.process.start()
    
    def run(self):
        mon = monitors.Monitor(MONITOR_NAME)
        mon.setDistance(MONITOR_DISTANCE)
        mon.setGamma(MONITOR_GAMMA)
        mon.setSizePix(MONITOR_RESOLUTION)
        mon.setWidth(MONITOR_SIZE[0])
        win = visual.Window(size         = MONITOR_RESOLUTION,
                            pos          = MONITOR_POSITION,
                            monitor      = mon,
                            units        = 'deg',
                            screen       = MONITOR_ID,
                            allowGUI     = False,
                            waitBlanking = False,
                            fullscr      = False,
                            allowStencil = True)
        stm = visual.GratingStim(win, size = 120, texRes = 512, tex = 'sqr')
        self.flag_run.value = True
        while self.flag_run:
            stm.contrast = self.ct.value
            stm.sf       = self.sf.value
            stm.phase   += self.tf.value/MONITOR_REFRESH_RATE
            if self.vis.value:
                stm.draw()
            win.flip()
    
    def update(self, vis = None, ct = None, sf = None, tf = None):
        self.vis.value = vis if vis is not None else self.vis.value
        self.ct.value  = ct  if ct  is not None else self.ct.value
        self.sf.value  = sf  if sf  is not None else self.sf.value
        self.tf.value  = tf  if tf  is not None else self.tf.value
    
    def abort(self):
        self.flag_run = False
        self.process.terminate()
        self.process.join()
        
    
class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('OKR Visual Stimulation')
        self.setWindowIcon(qg.QIcon('icon.png'))
        #self.setWindowFlag(qc.Qt.WindowType.WindowStaysOnTopHint, True)
        
        text_ct = qw.QLabel('Contrast (%)')
        self.ct = qw.QSpinBox()
        self.ct.setMaximum(100)
        self.ct.setValue(STIMULATION_CONTRAST)
        
        text_sf = qw.QLabel('Spatial frequency (c/d)')
        self.sf = qw.QDoubleSpinBox()
        self.sf.setMaximum(10)
        self.sf.setValue(STIMULATION_SPATIAL_FREQUENCY)
        
        """
        text_tf = qw.QLabel('Temporal frequency (c/s)')
        self.tf = qw.QDoubleSpinBox()
        self.tf.setMaximum(10)
        self.tf.setMinimum(-10)
        self.tf.setValue(1)
        """
        
        text_spd = qw.QLabel('Speed (d/s)')
        self.spd = qw.QDoubleSpinBox()
        self.spd.setMaximum(20)
        self.spd.setMinimum(-20)
        self.spd.setValue(STIMULATION_SPEED)
        
        button_show_hide = qw.QPushButton('Show/Hide')
        button_apply = qw.QPushButton('Apply')
        
        self.state_ct_step = qw.QRadioButton('Contrast step (%)')
        self.ct_step       = qw.QSpinBox()
        self.ct_step.setMaximum(100)
        self.ct_step.setValue(10)
        
        self.state_sf_step = qw.QRadioButton('Spatial frequency step (c/d)')
        self.sf_step       = qw.QDoubleSpinBox()
        self.sf_step.setMaximum(1)
        self.sf_step.setValue(0.05)
        
        self.state_spd_step = qw.QRadioButton('Speed step (d/s)')
        self.spd_step       = qw.QDoubleSpinBox()
        self.spd_step.setMaximum(20)
        self.spd_step.setValue(1)
        
        group_step = qw.QButtonGroup()
        group_step.addButton(self.state_ct_step)
        group_step.addButton(self.state_sf_step)
        group_step.addButton(self.state_spd_step)
        self.state_sf_step.setChecked(True)
        self.ct_step.setEnabled(False)
        self.spd_step.setEnabled(False)
        
        text_timer = qw.QLabel('Timer (sec)')
        self.timer = qw.QSpinBox()
        self.timer.setValue(10)
        
        text_termination = qw.QLabel('Termination (#Miss)')
        self.termination = qw.QSpinBox()
        self.termination.setValue(20)
        text_nmiss       = qw.QLabel('Total #Miss')
        self.nmiss       = qw.QLabel('0')
        
        text_save   = qw.QLabel('Save directory')
        self.save   = qw.QLineEdit()
        self.save.setText(SAVE_DIRECTORY)
        button_save = qw.QPushButton('Select')
        text_id     = qw.QLabel('Animal ID')
        self.id     = qw.QLineEdit()
        
        self.button_start = qw.QPushButton('Start')
        self.button_stop  = qw.QPushButton('Stop')
        self.button_stop.setEnabled(False)
        
        #text_answer = qw.QLabel('Staircase method\nClick here\nHit --- left\nMiss --- right\nFlip --- middle')
        text_answer = qw.QLabel('Staircase method\nClick here\nHit --- left\nMiss --- right')
        
        layout_values = qw.QGridLayout()
        layout_values.addWidget(text_ct, 1, 1)
        layout_values.addWidget(self.ct, 1, 2)
        layout_values.addWidget(text_sf, 2, 1)
        layout_values.addWidget(self.sf, 2, 2)
        #layout_values.addWidget(text_tf, 3, 1)
        #layout_values.addWidget(self.tf, 3, 2)
        layout_values.addWidget(text_spd, 3, 1)
        layout_values.addWidget(self.spd, 3, 2)
        group_values = qw.QGroupBox()
        group_values.setLayout(layout_values)
        group_values.setStyleSheet('QGroupBox {border:0;}')
        
        layout_task = qw.QGridLayout()
        layout_task.addWidget(self.state_ct_step,  1, 1)
        layout_task.addWidget(self.ct_step,        1, 2)
        layout_task.addWidget(self.state_sf_step,  2, 1)
        layout_task.addWidget(self.sf_step,        2, 2)
        layout_task.addWidget(self.state_spd_step, 3, 1)
        layout_task.addWidget(self.spd_step,       3, 2)
        layout_task.addWidget(text_timer,          4, 1)
        layout_task.addWidget(self.timer,          4, 2)
        layout_task.addWidget(text_termination,    5, 1)
        layout_task.addWidget(self.termination,    5, 2)
        layout_task.addWidget(text_nmiss,          6, 1)
        layout_task.addWidget(self.nmiss,          6, 2)
        layout_task.addWidget(text_save,           7, 1)
        layout_task.addWidget(self.save,           7, 2)
        layout_task.addWidget(button_save,         7, 3)
        layout_task.addWidget(text_id,             8, 1)
        layout_task.addWidget(self.id,             8, 2)
        layout_task.addWidget(self.button_start,   9, 1, 1, 3)
        layout_task.addWidget(self.button_stop,   10, 1, 1, 3)
        group_task = qw.QGroupBox()
        group_task.setLayout(layout_task)
        group_task.setStyleSheet('QGroupBox {border:0;}')
        
        layout_buttons = qw.QGridLayout()
        layout_buttons.addWidget(button_show_hide, 4, 1)
        layout_buttons.addWidget(button_apply, 4, 2)
        group_buttons = qw.QGroupBox()
        group_buttons.setLayout(layout_buttons)
        group_buttons.setStyleSheet('QGroupBox {border:0;}')
        
        layout_answer = qw.QGridLayout()
        layout_answer.addWidget(text_answer)
        group_answer = qw.QGroupBox()
        group_answer.setLayout(layout_answer)
        
        layout_main = qw.QGridLayout()
        layout_main.addWidget(group_values,  1, 1)
        layout_main.addWidget(group_buttons, 2, 1)
        layout_main.addWidget(group_task,    3, 1)
        layout_main.addWidget(group_answer,  1, 2, 3, 1)
        widget = qw.QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)
        
        self.flag_visible = False
        self.flag_flip    = False
        
        self.stimulation_process = StimulationProcess(vis = self.flag_visible)
        self.clickApply()
        self.stimulation_process.start()
        
        button_show_hide.clicked.connect(self.clickShowHide)
        button_apply.clicked.connect(self.clickApply)
        group_answer.mousePressEvent = self.selectAnswer
        self.answer = group_answer
        self.answer.setEnabled(False)
        
        button_save.clicked.connect(self.clickSelect)
        
        self.button_start.clicked.connect(self.startTask)
        self.button_stop.clicked.connect(self.stopTask)
        
        self.state_ct_step.clicked.connect(lambda: self.ct_step.setEnabled(True))
        self.state_ct_step.clicked.connect(lambda: self.sf_step.setEnabled(False))
        self.state_ct_step.clicked.connect(lambda: self.spd_step.setEnabled(False))
        self.state_sf_step.clicked.connect(lambda: self.ct_step.setEnabled(False))
        self.state_sf_step.clicked.connect(lambda: self.sf_step.setEnabled(True))
        self.state_sf_step.clicked.connect(lambda: self.spd_step.setEnabled(False))
        self.state_spd_step.clicked.connect(lambda: self.ct_step.setEnabled(False))
        self.state_spd_step.clicked.connect(lambda: self.sf_step.setEnabled(False))
        self.state_spd_step.clicked.connect(lambda: self.spd_step.setEnabled(True))
    
    def clickShowHide(self):
        self.flag_visible = not self.flag_visible
        self.stimulation_process.update(vis = self.flag_visible)
    
    def clickApply(self):
        ct = self.ct.value()/100
        sf = self.sf.value()
        tf = self.sf.value()*self.spd.value()
        self.stimulation_process.update(ct = ct, sf = sf, tf = tf)
    
    def clickSelect(self):
        dialog = qw.QFileDialog()
        dialog.setFileMode(qw.QFileDialog.FileMode.Directory)
        if dialog.exec():
            name = dialog.selectedFiles()[0]
            if name:
                self.save.setText(name)
    
    def selectAnswer(self, event):
        if event.button() == qc.Qt.MouseButton.LeftButton:
            self.hit()
        elif event.button() == qc.Qt.MouseButton.RightButton:
            self.miss()
    
    def hit(self):
        self.file.write('%f,%f,%f,%s\n'%(self.ct.value(), self.sf.value(), self.spd.value(), 'h'))
        if self.flag_flip:
            self.flag_flip = False
            if self.state_ct_step.isChecked():
                self.ct.setValue(self.ct.value() - self.ct_step.value())
            elif self.state_sf_step.isChecked():
                self.sf.setValue(self.sf.value() + self.sf_step.value())
            elif self.state_spd_step.isChecked():
                self.spd.setValue(abs(self.spd.value()) + self.spd_step.value())
            #self.spd.setValue(-self.spd.value())
        else:
            self.flag_flip = True
            self.spd.setValue(-self.spd.value())
        #self.spd.setValue(-self.spd.value())
        self.stimulation_process.update(ct = self.ct.value()/100, sf = self.sf.value(), tf = self.sf.value()*self.spd.value())
        self.timer.setValue(self.timer_value)
        self.countdown.start()
    
    def miss(self):
        if self.state_ct_step.isChecked() and not self.ct.value() == 100:
            self.file.write('%f,%f,%f,%s\n'%(self.ct.value(), self.sf.value(), self.spd.value(), 'm'))
            self.flag_flip = False
            self.ct.setValue(self.ct.value() + self.ct_step.value())
            self.spd.setValue(abs(self.spd.value()))
            #self.stimulation_process.update(sf = self.sf.value(), tf = self.sf.value()*self.spd.value())
            #self.incrementMiss()
            #self.timer.setValue(self.timer_value)
            #self.countdown.start()
        elif self.state_sf_step.isChecked() and not self.sf.value() == 0:
            self.file.write('%f,%f,%f,%s\n'%(self.ct.value(), self.sf.value(), self.spd.value(), 'm'))
            self.flag_flip = False
            self.sf.setValue(self.sf.value() - self.sf_step.value())
            self.spd.setValue(abs(self.spd.value()))
        elif self.state_spd_step.isChecked() and not self.spd.value() == 0:
            self.file.write('%f,%f,%f,%s\n'%(self.ct.value(), self.sf.value(), self.spd.value(), 'm'))
            self.flag_flip = False
            self.spd.setValue(max(abs(self.spd.value())-self.spd_step.value(), 0))
        self.stimulation_process.update(ct = self.ct.value()/100, sf = self.sf.value(), tf = self.sf.value()*self.spd.value())
        self.incrementMiss()
        self.timer.setValue(self.timer_value)
        self.countdown.start()
    
    def incrementMiss(self):
        nmiss = int(self.nmiss.text()) + 1
        self.nmiss.setText(str(nmiss))
        if nmiss == self.termination.value():
            self.stopTask()
    
    def decrementTimer(self):
        time = self.timer.value() - 1
        self.timer.setValue(time)
        if time == 0:
            self.miss()
    
    def startTask(self):
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)
        self.file = open(os.path.join(self.save.text(), self.id.text() + tm.strftime('_%Y%m%dT%H%M%S.csv')), 'w')
        self.file.write('ct,sf,spd,hm\n')
        self.flag_visible = True
        #self.ct.setValue(STIMULATION_CONTRAST)
        #self.sf.setValue(STIMULATION_SPATIAL_FREQUENCY)
        #self.spd.setValue(STIMULATION_SPEED)
        self.ct_value  = self.ct.value()
        self.sf_value  = self.sf.value()
        self.spd_value = self.spd.value()
        ct = self.ct_value/100
        sf = self.sf_value
        tf = self.sf_value*self.spd_value
        self.stimulation_process.update(vis = self.flag_visible, ct = ct, sf = sf, tf = tf)
        self.answer.setEnabled(True)
        self.nmiss.setText('0')
        self.timer_value = self.timer.value()
        self.countdown = qc.QTimer()
        self.countdown.setInterval(1000) # 1000 ms
        self.countdown.timeout.connect(self.decrementTimer)
        self.countdown.start()
    
    def stopTask(self):
        self.file.close()
        self.flag_visible = False
        self.stimulation_process.update(vis = self.flag_visible)
        self.answer.setEnabled(False)
        self.countdown.timeout.disconnect(self.decrementTimer)
        self.countdown.stop()
        self.timer.setValue(self.timer_value)
        self.ct.setValue(self.ct_value)
        self.sf.setValue(self.sf_value)
        self.spd.setValue(self.spd_value)
        self.button_start.setEnabled(True)
        self.button_stop.setEnabled(False)
        
    def closeEvent(self, event):
        self.stimulation_process.abort()

if __name__ == '__main__':
    app = qw.QApplication([])
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

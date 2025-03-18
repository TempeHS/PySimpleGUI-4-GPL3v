#!/usr/bin/env python
import sys
sys.path.append("../lib")
import PySimpleGUI as sg
import time

"""
 Timer Desktop Widget Creates a floating timer that is always on top of other windows You move it by grabbing anywhere on the window Good example of how to do a non-blocking, polling program using PySimpleGUI 
 Something like this can be used to poll hardware when running on a Pi

 While the timer ticks are being generated by PySimpleGUI's "timeout" mechanism, the actual value
  of the timer that is displayed comes from the system timer, time.time().  This guarantees an
  accurate time value is displayed regardless of the accuracy of the PySimpleGUI timer tick. If
  this design were not used, then the time value displayed would slowly drift by the amount of time
  it takes to execute the PySimpleGUI read and update calls (not good!)

    Copyright 2021 PySimpleGUI
"""


def time_as_int():
    return int(round(time.time() * 100))


# ----------------  Create Form  ----------------
sg.theme('Black')

layout = [[sg.Text('')],
          [sg.Text('', size=(8, 2), font=('Helvetica', 20),
                justification='center', key='text')],
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-'),
           sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]]

window = sg.Window('Running Timer', layout,
                   no_titlebar=True,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   finalize=True,
                   element_justification='c',
                   right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_EXIT)

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

while True:
    # --------- Read and update window --------
    if not paused:
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time
    else:
        event, values = window.read()
    # --------- Do Button Operations --------
    if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
        break
    if event == '-RESET-':
        paused_time = start_time = time_as_int()
        current_time = 0
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_time = start_time + time_as_int() - paused_time
        # Change button's text
        window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
    elif event == 'Edit Me':
        sg.execute_editor(__file__)
    # --------- Display timer in window --------
    window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                        (current_time // 100) % 60,
                                                        current_time % 100))
window.close()

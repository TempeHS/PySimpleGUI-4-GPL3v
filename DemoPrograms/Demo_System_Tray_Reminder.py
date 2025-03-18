import sys
sys.path.append("../lib")
import PySimpleGUI as sg
from PIL import Image
import base64, io
from time import time

"""
    A periodic reminder that uses the System Tray.
    Will show a popup window every X minutes
    Should work with 3 of the PySimpleGUI ports - tkinter, WxPython, Qt
"""

ONE_HOUR_IN_SECONDS = 60*60
STARTING_FREQUENCY = ONE_HOUR_IN_SECONDS
POPUP_FONT = 'Helvetica 16'       # font to use in popup
POPUP_TEXT_COLOR, POPUP_BACKGROUND_COLOR = 'white', 'red'

def resize_base64_image(image64, size):
    """
    Resize a base64 image.  Good to use for Image elements, Button Images, etc.

    :param image64: The Base64 image
    :type image64: bytes
    :param size: Size to make the image in pixels (width, height)
    :type size: Tuple[int, int]
    :return: A new Base64 image
    :rtype: bytes
    """
    image_file = io.BytesIO(base64.b64decode(image64))
    img = Image.open(image_file)
    img.thumbnail(size,  Image.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    imgbytes = bio.getvalue()
    return imgbytes


def main():
    """
    Function with all the good stuff.  Creates the System Tray and processes all events
    """
    delay = frequency_in_seconds = STARTING_FREQUENCY

    tray_icon = resize_base64_image(icon, (64,64)) if sg.port == 'PySimpleGUI' else icon

    menu_def = ['UNUSED', ['Change Frequency', '---', 'Exit']]

    tray = sg.SystemTray(menu=menu_def, data_base64=tray_icon, tooltip=f'Reminder every {frequency_in_seconds/60} minutes')

    starting_seconds = time()

    while True:
        event = tray.read(timeout=delay*1000)
        if event == 'Exit':
            break

        delta_from_last = time() - starting_seconds
        if delta_from_last >= frequency_in_seconds:
            starting_seconds = time()
            delta_from_last = 0
            sg.popup_no_wait('Reminder!', f'It has been {frequency_in_seconds/60} minutes since your last reminder', background_color=POPUP_BACKGROUND_COLOR, text_color=POPUP_TEXT_COLOR, font=POPUP_FONT)

        if event == 'Change Frequency':       # Change how often a reminder should be shown
            freq = sg.popup_get_text(f'Currently you will be reminded every {frequency_in_seconds/60} minutes\n'+
                                     'Enter new frequency in minutes', 'Change Timer Frequency')
            try:
                frequency_in_seconds = int(float(freq)*60)
                starting_seconds = time()
                delta_from_last = 0
                tray.update(tooltip=f'Reminder every {frequency_in_seconds/60} minutes')
            except:
                sg.popup_error(f'Invalid value: {freq}', f'Keeping old frequency of {frequency_in_seconds/60} minutes')

        delay = frequency_in_seconds - delta_from_last
    tray.close()

if __name__ == '__main__':
    icon = \
        b'iVBORw0KGgoAAAANSUhEUgAAAyAAAAOdCAMAAABK+vbxAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAF4FBV4KCl4PEF0TE10XGFwaG14kJV4rK14zM147O2AUFGAXGGAaGXwEBHsHCHsLDHsPEHwSEn0WGGAsLGAvMWA9PXAjInsiI3s8PUxMTFJSUllZWW5dXH1AQmJiYm1tbXhubnNzc3h4eIAAAIATE4A6PNkAAO4bHfYOD/oGBv4AAPwGBvoHCPwGCPoIB/oICfkLDPgMC/kMDfwJCfkPEPcSFPYVFvMXGvYWGPcYF/IYG/EaHPEcHvYYGvYaHPYcHvgQEfkSFPgUFfwQEfgXGPgZGfgaHPgcHf0bHe8dIPIdIPkdIPUhH+8hJO4mKe8pLO4xL+E9PesxMu8wM+4yNe42Oe44Ou87PO48PvEgIvAhJPEkJfUhIvUiJPUlJvIlKPQrLPghIfoiJPknJ/8mJvwlKPkpKvIuMPExMvAyNfI1NfUxMvUyNPU1NvM2OPE4OvA5PfA8PvU4OvU6PfU8PfoyM/w4Nvo6PPQ+QPg7QPhAP+9KR+9KTO9SVO9YWvJAQvJBRPFERvVBQvVCRPRGQ/VFRvRFSPJIRfFJSvNJTPFNT/ZJSvVKTfdMSPVNT/pDRPhFSPlJR/lKTPZMUfpOU/pUT/FRUvFTVfBVV/ZQUfZSVfRVVfRWWPNaW/FaXPJdXvVYWfVZXPRcXvtTVPtVWftbW/RdYPtfYfthXfNiZPRmaPNqa/1jZPxmafxoZf1rbPJvcP1tcfxwbfRyc/Z2ePN5efR5evZ7fPZ8ffxzdP92e/15dv18e/d/gP2CfYCAgMSFhNOfndqdn+edne6RkeicnPOBgvaBgvaGhvOLi/iBgviChPiFhf6Fgf+EhfqHiP6JhPmLjPmRkvqTlfmUlf+RlPqZmfudnvyZmvyenuWiouihovaurvujo/yioviqqvWzs/K+vsfHx8bKy8zFxMrKx8jIyMnNyczIyM3NzdDQ0NbW1tfY19nZ2d3d3eDf3vHCwvDLy/DR0fDc3ODg4OXl5enp6ezs7PLg4PHx8f///wAAAAAAAAAAAAAAALul9qwAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAA7+UlEQVR4Xu3df5xld33X8bXF0qLGGBHb2a2zzlYXMyFOXDClhGwghU0zSFELWCLJLnRkUxK2NAGJvwoEE2PBogFRCg/5sVnpJsEtBBNSYqaKERYXYTHdsCmd1uhjdIl3JSGbbeaP6znnfmbm/jj3ez7fz/f39/t+/tEm4f4857zm+z3n3Hvulj4ATIVAABQQCIACAgFQQCAACggEQAGBACggEAAFBAKggEAAFBAIgAICGfLd1cdWV0+v1U6v1v9M/92v/0L/H2KAQBqnqIsWp1dP0Y28uPfl8yfoHyECCKS/eoZSUHjKUyS3nT8/P38p/QtEoPRAelQAw+N0F3d+daHKo7JC/w7hFR3I47Tpcz3zXbqjE596wSCP+fmfo/8C4RUcyDO02Wt5mu5s3cMvpjoqC/TfILxSA5m6T97NxVTrxG5qY+A2+s8QXJmBMHbLVU7Tw9jy7T0UxjoMIdEoMRDDPGo2E1m5jLIY8mn63yC08gKxkEetRw9nauWN1MSIXfS/QmilBaJxWLeLlX2Rt1IR4x6h/x0CKywQ0ZGrac7Sg8p9hE58TLqabgGBFRWIpdnVJrNdkWPj++bD6DYQWEmB0FZtFT20wLeGTny0+ATdDMIqJxDrw8eAcE+k7dDViFvohhBWMYGcpQ3aOtHhrBspg+neTLeEsEoJhLZmF/T31U+8gipQuZFuDEGVEYjupxI10bMwrYx+rGSq99PtIaQiArF48qOdzo7IdbT9d6M7QEglBGLwwUQu9o7IiUtp62fAycIIFBCIs93zYcxCXkXbPsvr6U4QUP6BWD15Ph3nnGH3sasRF9PdIKDsA6Ht173OMeQTF9GGz/ZFuieEk3sgtPX6cIaecgr+zvmG6+muEE7mgTxNG68X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'

    main()
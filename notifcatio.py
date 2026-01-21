from plyer import notification
from win10toast import ToastNotifier
import threading

def show_notification():
    notification.notify(
        title='KodeArrow in system tray',
        message='Click KodeArrow icon to open',
        app_name='KodeArrow',
        app_icon='icon.ico',  # Path to your icon file
        timeout=10  # Duration of the notification
    )

def show_notification2():
    toaster = ToastNotifier()
    # toaster.show_toast(
    #     'KodeArrow in system tray',
    #     'Click KodeArrow icon to open',
    #     # app_name='KodeArrow',
    #     timeout=10,  # Duration of the notification
    #     threaded=True  # Run in a separate thread
    # )
    toaster.show_toast(
    "KodeArrow in system tray",
    "Click KodeArrow icon to open",
    duration = 10,
    icon_path = "icon.ico",
    threaded = True,
)

# show_notification()
show_notification2()

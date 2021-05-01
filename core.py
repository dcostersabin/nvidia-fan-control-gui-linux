import tkinter as tk
from tkinter import messagebox as tkmsgbox
import os
import sys
import subprocess
import logging
import datetime
import time

# root frame
root = tk.Tk()
root.title("Nvidia Fan Control")
root.geometry("600x600")

# user info frame
user_cred = tk.Frame(root)
user_cred.pack(side=tk.TOP)

# nvidia info frame
nvid = tk.Frame(root)
nvid.pack(side=tk.BOTTOM)

# scale measure and set frame
scale = tk.Frame(root)
scale.pack(side=tk.BOTTOM)

# nvidia smi info frame
nvidia_smi = tk.Frame(root, pady=50)
nvidia_smi.pack(anchor=tk.CENTER)

smi_label = tk.Label(nvidia_smi, text="", bg='white', fg='green')

speed_label = tk.Label(nvid, text="")


def refresh_smi():
    try:
        smi_result = subprocess.check_output('nvidia-smi', shell=True, universal_newlines=True)
        smi_label['text'] = smi_result
        smi_label.pack(anchor=tk.CENTER)
    except subprocess.SubprocessError:
        smi_label['text'] = 'Cant Fetch nvidia-smi result'
        smi_label['fg'] = 'red'
        smi_label.pack(anchor=tk.CENTER)


def set_speed():
    logging.basicConfig(filename='nvidia-fan-control.log', level=logging.INFO)
    val = int(var.get())
    try:
        # set the gpu for over clocl
        command = "nvidia-settings -a '[gpu:0]/GPUFanControlState=1'"
        subprocess.check_output(command, shell=True, universal_newlines=True)
        # command to set the speed
        command = "nvidia-settings -a '[fan]/GPUTargetFanSpeed=" + str(val) + "'"
        # running a subprocess
        subprocess.check_output(command, shell=True,
                                universal_newlines=True)
        logging.info("Fan Speed Set To " + str(val) + " " + str(datetime.datetime.now()))
        speed_label['text'] = "Fan Speed Set To " + str(val)
        speed_label.pack(side=tk.BOTTOM)
        # sleep to coordinate with nvidia-smi
        time.sleep(8.0)
        refresh_smi()
    except subprocess.SubprocessError:
        # failed to set the value
        logging.warning("Failed To set Speed to " + str(val) + " " + str(datetime.datetime.now()))
        speed_label['text'] = "Failed To Set Fan Speed"
        speed_label['fg'] = 'red'
        speed_label.pack(side=tk.BOTTOM)


def reboot():
    result = tkmsgbox.askquestion(title='Reboot', message='Do you want to reboot?')
    if result == 'yes':
        logging.info("Rebooting the system" + str(datetime.datetime.now()))
        subprocess.check_output('sudo reboot', shell=True, universal_newlines=True)
    else:
        logging.info("Rebooting request rejected" + str(datetime.datetime.now()))
        tkmsgbox.showwarning(title='Reboot Required', message='Reboot is required to implement the changes')


reboot_button = tk.Button(user_cred, text="Reboot", command=reboot, fg="red", state=tk.DISABLED)
set_button = tk.Button(scale, text="Set", command=set_speed)


# setting the overall configurations
def set_config():
    try:
        # checking if nvidia-smi is installed
        subprocess.check_output('nvidia-smi', shell=True, universal_newlines=True)
        try:
            # allowing the gpu to overclock manually
            subprocess.check_output('sudo nvidia-xconfig -a --cool-bits=28 --allow-empty-initial-configuration',
                                    shell=True, universal_newlines=True)
            # success message
            msg = 'Success! New X configuration file written to /etc/X11/xorg.conf'
            # generates label after success
            tk.Label(nvid, text=msg, fg="green").pack(side=tk.BOTTOM)
            # creating logging
            logging.basicConfig(filename='nvidia-fan-control.log', level=logging.INFO)
            logging.info(msg=msg + str(datetime.datetime.now()))
            # enable reboot button
            reboot_button['state'] = tk.NORMAL
            # disable xconfig button
            button1['state'] = tk.DISABLED

        except subprocess.SubprocessError:
            # If xconfig failed to init
            tk.Label(nvid, text="Could Not Generate xorg.conf", fg="red").pack(side=tk.TOP)
    except subprocess.SubprocessError as e:
        # nvidia-smi not found
        tk.Label(nvid, text="Nvidia Driver Not Found Or Install nvidia-smi", fg="red").pack(side=tk.TOP)


button1 = tk.Button(user_cred, text="Initialize Nvidia Xconfig", command=set_config, state=tk.DISABLED)
# checking root privilege
if os.getuid() != 0:
    print("Script not started as root. Running sudo..")
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)
    root_label = tk.Label(user_cred, text="Root Privilege Required", fg="red").pack(side=tk.TOP)
    button1.pack(side=tk.LEFT)
else:
    root_label = tk.Label(user_cred, text="Root User", fg="green").pack(side=tk.TOP)
    button1['state'] = tk.NORMAL
    button1.pack(side=tk.LEFT)
    reboot_button.pack(side=tk.RIGHT)

    if os.path.isfile('nvidia-fan-control.log'):
        tk.Label(nvid, text="X Config File Already Set", fg='green').pack(side=tk.TOP)
        button1['state'] = tk.DISABLED
        tk.Label(scale, text="Select Fan Speed", fg='black').pack(side=tk.TOP)
        var = tk.DoubleVar()
        measure = tk.Scale(scale, variable=var, orient="horizontal")
        measure.pack(side=tk.BOTTOM)
        set_button.pack(side=tk.TOP)

    refresh_smi()

root.mainloop()

# nvidia-fan-control-gui-linux

GUI fan controller for nvidia
<br>
<i>Note: Tested on RTX 3060</i>

## Installation

Use the package manager [conda](https://www.anaconda.com/) to install the dependencies
<br>
<small>Note: All the requirements are in requirement.txt</small>
<br>
``conda create --name <env> --file <this file(requirement.txt)>``
<br>

## Usage

### Step 1

run core.py file  ``python3 core.py``
<br>
![step1](https://github.com/dcostersabin/nvidia-fan-control-gui-linux/blob/main/images/step1.png)
<br>

### Step 2
Click On Initialize Nvidia Xconfig
<br>
![Step2](https://github.com/dcostersabin/nvidia-fan-control-gui-linux/blob/main/images/step2.png)

### Step 3
If <strong>Success! New X configuration file written to /etc/X11/xorg.conf </strong> is shown below in green follow step 3 otherwise check your driver
<br>
<b>Click On Reboot</b> 
<br>
![step3](https://github.com/dcostersabin/nvidia-fan-control-gui-linux/blob/main/images/step3.png)
![step3](https://github.com/dcostersabin/nvidia-fan-control-gui-linux/blob/main/images/step4.png)
<br>
<strong>If No</strong>
<br>
![step3](https://github.com/dcostersabin/nvidia-fan-control-gui-linux/blob/main/images/step5.png)
<br>
### Step 4
After Reboot run <strong>Step 1 </strong> again
<br>
Interface should look like
<br>
![step4](https://github.com/dcostersabin/nvidia-fan-control-gui-linux/blob/main/images/step6.png)
<br>

### Step 5
Set desired speed
<br>
![step5](https://github.com/dcostersabin/nvidia-fan-control-gui-linux/blob/main/images/step7.png)
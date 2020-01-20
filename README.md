# Autonomous Driving Model Car with 2D Camera

This project was implemented as part of a Bachelor IT project. The goal was to build the Alamak kit (model vehicle) with the corresponding microcontrollers and to let it drive autonomously with the help of a 2D camera. Thereby an image recognition algorithm was to be implemented, which can process several pixel rows.


## Setup

### Arduino
The Arduino Uno is programmed in C++. To compile and flash the microcontroller, the Arduino IDE is used.

#### Required libraries

 * Adafuit PWM Servo Driver Library
 * NewPing
 * liquid crystal

These can be installed directly from the Arduino IDE. In the menu under
`Sketch > Include Library > Manage Libraries...`

### Raspberry Pi


#### 1) Install operating system on SD card

For the Raspberry Pi the official operating system Raspbian is available.

We recommend the Raspbian Lite variant (without desktop), as it requires the least resources.

*Optional:* To be able to connect to SSH on the Raspberry Pi from the beginning, the file ssh must be created in the boot directory of the SD card.  
SSH can also be activated later (see step 5).

#### 2) Download source code

Download and unzip the Raspberry Pi directory from source.

#### 3) Build CarTV frontend

Build the CarTV frontend (see [here](./docs/setup_cartv.md)).
This should not be done on the Raspberry Pi, because it takes a long time to load all needed packages and build the frontend.

#### 4) Transfer source code to the Raspberry Pi

Copy the files in the Raspberry Pi directory to the SD card of the Raspberry Pi under the /home/pi directory.

*With SSH/SCP:* If SSH is enabled on the Raspberry Pi (step 1), then the files can be transferred to the booted Raspberry Pi over the local network. The hostname of the Raspberry Pi is raspberrypi.  
Under Windows you can connect directly to the Raspberry Pi via WinSCP (login: `pi`, password: `raspberry`).

*Without SSH/SCP:* Write directly to the SD card via notebook or PC.

#### 5) Set up Raspberry Pi

Open a terminal on the Raspberry Pi either directly or, if configured in step 1, via SSH (under Windows using PuTTY).

Execute the following commands in sequence, using the login `pi`:

```bash
    sudo chmod +x setup.sh
    sudo ./setup.sh
    sudo raspi-config
        → interfaces → camera → enable
        → interfaces → ssh → enable
        → interfaces → i2c → enable
    sudo reboot now
```

#### 6) Building CPicLib

Build the CPicLib on the Raspberry Pi (see [here](./docs/setup_cpiclib.md)).

#### 7) Start program

To start the python3 program run `main.py`.

*Optional:* A crontab can be created for the automatic start of `main.py`.

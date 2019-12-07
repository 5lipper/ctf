Lock2018
Score: 500

You are given a COTS (commercial off-the-shelf) lock, running our home-brewed firmware, w/ web management (please login with whatever username, and your team token as password). You are also given some necessary tools including screw driver, debugger, RF transceiver and wires. See the attachment for document and demo code for RF transceiver.

Please demonstrate opening the door on the stage. (You are not allowed to access the key hole / micro USB port on the stage)

PS: The voice output of the lock is Chinese only. Here is an incomplete list of their Pin-Yin pronunciation with English translation. If you have any problem understanding Chinese, feel free to ask.

    Yǐ liánjiē: connected
    Mìmǎ zhèngquè: correct password
    Mìmǎ cuòwù: wrong password"

Attachment

update:

Additional Information for Lock Challenges

You can find an SPI module (yellow color, 18.1mm * 22.1mm) on the main PCB, labeled as "HJ-WL433-IP1". Since there's no English datasheet available for this module, we would like to provide necessary information here.

This is a radio module based on SI4438 transceiver, w/ 26 MHz oscillator.


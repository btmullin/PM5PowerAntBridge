# Concept 2 PM5 To Ant+ Power Meter Bridge

This project converts the USB output from a PM5 rowing erg to an Ant+ power meter and speed/cadence sensor stream.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python
USB something
PyRow
PyAnt
vpower
Ant+ Stick
PM5

What things you need to install the software and how to install them

### Installing

```
>git clone https://github.com/wemakewaves/PyRow
>git clone https://github.com/dhague/vpower
>cd vpower
>sudo pip install -r requirements.txt
>cd ..
>git clone https://github.com/mvillalba/python-ant
```

Fix driver error via this:
https://coderwall.com/p/canuka/alternatesetting-error-in-python-ant
Make change on line 197 or src/ant/core/driver.py before doing the install

```
>cd python-ant
>sudo python setup.py install
>cd ..
```

Create udev rule for Ant+ stick
/etc/udev/rules.d/garmin-ant2.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fcf", ATTRS{idProduct}=="1008", RUN+="/sbin/modprobe usbserial vendor=0x0fcf product=0x1008", MODE="0666", OWNER="pi", GROUP="root"

Create udev rule for C2 PM5
/etc/udev/rules.d/95-concept2.rules
KERNEL=="hidraw*" SUBSYSTEM=="hidraw" MODE="666"
KERNEL=="hiddev*" SUBSYSTEM=="usbmisc" MODE="666"

### Operation

Plug in Ant+ Stick
Plug in PM5

```
>sudo python row.py
```

Connect your device to the Ant+ Power device and Speed/Cadence device.

## Versioning

We may use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

Currently the software is not versioned.

## Authors

* **Ben Mullin** - *Initial work* - [btmullin](https://github.com/btmullin)

## License

This project is licensed under the BSD 2-Clause "Simplified" License - see the [LICENSE.md](LICENSE.md) file for details

This is carried forward from the PyRow project that is the basis for this implementation.

## Acknowledgments

This project is based on the POC work here [C2 to Zwift Connector](https://diana.bib.uniurb.it/pyRide/pyRide.html)


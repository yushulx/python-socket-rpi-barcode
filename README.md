# Server-side Python Barcode Detection for Raspberry Pi

The purpose of the sample is to send video frames from Raspberry Pi to a remote server for barcode detection with [Dynamsoft Barcode Reader](https://www.dynamsoft.com/Products/Dynamic-Barcode-Reader.aspx). Thanks to @sabjorn's [NumpySocket](https://github.com/sabjorn/NumpySocket).

## System Requirements

- Python 2.7
- [Dynamsoft Barcode Reader SDK Download](https://www.dynamsoft.com/Downloads/Dynamic-Barcode-Reader-Download.aspx)


## Prerequisites

### Raspberry Pi

Install `OpenCV`, `scipy` and `pillow`:

```
$ sudo apt-get install libopencv-dev python-opencv python-scipy
$ python -m pip install pillow
```

### Windows

Install `dbr` and `OpenCV`:

```
> pip install dbr opencv-python
```

You can also follow https://github.com/dynamsoft-dbr/python to build and install the Python barcode module.

## Usage
Open `rpi.py` to set the host IP address:

```py
host_ip = '192.168.8.84' 
```

Get a [FREE 30-day trial license](https://www.dynamsoft.com/CustomerPortal/Portal/Triallicense.aspx), and set it in `pc.py`:

```
dbr.initLicense('LICENSE KEY')
```

Run `pc.py` in Windows:

```
python pc.py
```

Run `rpi.py` in Raspberry Pi:

```
python rpi.py
```

<kbd><img src="https://www.codepool.biz/wp-content/uploads/2019/03/raspberry-pi-barcode-detection.PNG">

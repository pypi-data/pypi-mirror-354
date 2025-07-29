PyUSBTMC

PyUSBTMC:python module to handle USB-TMC(Test and Measurement
class)　devices. It requires pyusb module and libusb or openusb
libraries.

(C) 2012-2015, Noboru Yamamot, Accl. Lab, KEK, JAPAN contact:
noboru.yamamoto_at_kek.jp

rev.0.1d17:

    .read/.ask functions now use 0 as default values for requestSize
    arguments. And requestSize=0 means, read data until eom is returned.

rev.0.1d14:

    remove reset in __init__ of USBTMC_device. It breaks everything for
    the device from Tektronix. bring back mkDevDepMSGOUTHeader to older
    version.

Note on root priviledge

PyUSBTMCでPyUSBTMC_deviceあるいはUSB488_deviceオブジェクトの作成時に、
"usb.core.USBError: [Errno 13] Access denied (insufficient
permissions)"のエラーが出る場合があります。

この場合には、

1.  sudo コマンド経由でpython3を起動する。
2.  Linux では、この配布に含まれる 55-usb-tmc488.rules ファイルを
    /etc/udeb/rules.d ディレクトリにコピーします(root権限が必要です）。
    使用するデバイスのidVendorが 55-usb-tmc488.rules
    に含まれない場合は、そのidVendorをファイルに追加します。idVendorはlsusbコマンド（このパッケージ中のlsusb.pyモジュールも利用可能）を使って入手できます。
    以後は sudo コマンドなしでもデバイスオブジェクトが作成出来ます。

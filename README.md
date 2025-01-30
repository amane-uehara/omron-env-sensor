# オムロンの環境センサーを読むスクリプト

[環境センサ (USB型) 形2JCIE-BU01](https://www.omron.co.jp/ecb/product-detail?partNumber=2JCIE-BU)
にRaspberry PiでBlueTooth接続し、計測値を取得するためのスクリプトです。

![Omron sensor](https://github.com/amane-uehara/resource/blob/master/omron-env-sensor/omron.png)

### 実行環境のインストール

Raspberry Piに以下のソフトをインストールする。
一般ユーザーの権限で動かすのは難しいので、rootでログインして`pip3`を実行する。

```
$ sudo apt install python3-dev
$ sudo apt install python3-pip
$ sudo apt install libglib2.0-dev
$ sudo apt install libboost-python-dev
$ sudo apt install libboost-thread-dev
$ sudo apt install libbluetooth3-dev
$ sudo su root
# pip3 install pybluez
# pip3 install gattlib
```

### MACアドレスの確認

センサーをUSB給電コンセントに差し込んで点灯を確認し、以下を実行する。

```
$ sudo hcitool lescan
```

以下のように右カラムに`Rbt`の含まれる行が、環境センサーのMACアドレスである。

```
BA:32:39:A8:5E:8D Rbt
```

### スクリプトの修正

本リポジトリに含まれる

<https://raw.githubusercontent.com/amane-uehara/omron-env-sensor/master/fetch-by-raspi3-raspi4.py>

をダウンロードし、
[MACアドレスの設定部分](https://github.com/amane-uehara/omron-env-sensor/blob/master/fetch-by-raspi3-raspi4.py#L5)
を先ほど調べた値に書き換える。

### スクリプトの実行

rootでログインして `fetch-by-raspi3-raspi4.py` を実行すれば環境センサーからの値を取得できる。

```
# sudo su root
# python3 fetch-by-raspi3-raspi4.py
2765,6909,78,1007316,5319,29,594


～～蛇足～～
$ sudo python3 fetch-by-raspi3-raspi4.py
のように一般ユーザーで動かすのは難しい。
```

### 表示データの形式

BlueToothのパケットに含まれる整数値を、CSV形式でそのまま出力している。

|列番号|説明                            |データ出力例    |物理量        |
|:-----|:-------------------------------|:---------------|:-------------|
|1     |温度 `(temperature)`            |`2765`          |`27.65 ℃`    |
|2     |湿度 `(relative_humidity)`      |`6909`          |`69.09 %`     |
|3     |照度 `(ambient_light)`          |`78`            |`78 lx`       |
|4     |気圧 `(barometric_pressure)`    |`1007316`       |`1007.316 hPa`|
|5     |騒音 `(sound_noise)`            |`5319`          |`53.19 dB`    |
|6     |総揮発性有機化合物濃度 `(etvoc)`|`29`            |`29 ppb`      |
|7     |二酸化炭素濃度相当値 `(eco2)`   |`594`           |`594 ppm`     |

### 参考ページ

* オムロン社の公式仕様書 <https://omronfs.omron.com/ja_JP/ecb/products/pdf/CDSC-016A-web1.pdf>
* オムロン社のサンプルスクリプト <https://github.com/omron-devhub/2jciebl-bu-ble-raspberrypi>

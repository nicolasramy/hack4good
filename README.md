# Commute 4 Good [NAME PROPOSAL]

Hack4good session organized by #Geekli.st in partnership with #Gandi at #Deezer in Paris
from the 4th to the 7th of October 2013

## 0) tl;dr


While commuting (using public transports like suburban train or metro),
one might want to chat easily with people around.
The main idea of this mockup application is about enabling people to do so, the easiest way possible.

## 1) Application Deployment (Android device)

* Download [Apache Cordava Package] (http://cordova.apache.org/#download)

* Download [Android SDK] (http://developer.android.com/sdk/index.html)

* Activate the developer mode of your device

* Create symlinks to Apache Cordova and Android SDK binaries

* Change directory

    `cd cordova`

* Build application

    `cordova platform remove android`

    `cordova platform add android`

* Build application

    `cordova build`

* Run application on Android device (after having connected it to your computer)

    `cordova run android`

* OR Create an Android Virtual Device

    `android create avd --name 'img' --target android-18`

* AND run application in Android device emulator

    `cordova emulate android`

* Update basic plain HTML, JavaScript and CSS files which have been added to /cordova/www

## 2) Backoffice

### Requierements:

- postgresql 9.1+
- python 2.7
- pip
- virtualenv

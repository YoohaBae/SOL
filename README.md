# SOL

## Python Module

### In Python Module Folder, you can find two versions of qr_scanner

#### qrcode_user.py:
Passengers can scan their boarding pass to KIOSK machine to check their luggage status.

#### qrcode_belt.py:
QR scanner installled on the conveyor belt will scan the qr code of a luggage and measure its scannig time.
Then it will automatically calculate how many loops has the luggage went.

#### QR code scanner screen
![Untitled](https://user-images.githubusercontent.com/68123073/108533939-f0bb0900-731c-11eb-8119-fb4927367834.png)

## Website

### Website is consisted of 5 folders and one file; html, css, bootstrap, node_modules, public, views, index.js

#### html:
Includes pure html code

#### css
Includes the css style of website

#### node_modules
Includes Node.js package

#### bootstrap-5.0.0-beta1-dist
Includes bootstrap package

#### public
Includes images used in website

#### views
Includes ejs files

#### index.js
Uses express to connect the pages. Uses MySQL for the backend.

#### Used Packages
- mysql
- express-session
- fs
- body-parser
- path
- express
- sync-mysql
- url
- ejs

#### How to run website
1. Download all folders.
2. Download Xampp
3. Run mysql and apache
4. Open a terminal where the folder is located.
5. Enter npm install <package-name> for all packages in Used Packages
6. Enter node index.js
7. Open browser and enter localhost:3000
8. Login using the below data
  - Off-flight status: amcculloch@gmail.com 0001
  - On-flight status: scrosby@gmail.com 0002
  - Pick-up status: ybae@gmail.com 0011

## Artifical Intelligence

### The AI of SOL is developed using data science.

#### Steps
1. Get the mySQL data
2. connect luggage database with passenger database and find the owner of luggage
3. Go through luggages and calculate the suggestion time and suggestion location of the luggage.
4. Distribute the suggestion location so that people do not gather too much at one location and adjust the suggestion time accordingly.
5. Edit the database if the luggage QR Code is not scanned after a certain time.

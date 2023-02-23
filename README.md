# Canvasdl

![Console image](https://raw.githubusercontent.com/quintenroets/canvasdl/main/examples/console.png?raw=true)
![Screen image](https://raw.githubusercontent.com/quintenroets/canvasdl/main/examples/screen.png?raw=true)

Tired of managing your course content on 5-10 different platforms? 
Canvasdl comes to the rescue and saves you hours of work when studying and completing assignments.
This convenient package:
- Synchronizes all your course content to local files
- Synchronizes your assignment dates to google calendar
- Shows you what items are new
- Remembers your progress through course materials
- Keeps you up to date without overwhelming you with useless notifications
- Synchronizes content available on:
   - Canvas:
     - Announcements
     - Assignments
     - Course files
     - Video recordings
   - Course websites
   - Ed Discussion
   - Google Drive
   - Piazza
   - Gradescope
- Developed for:
   - Students at Columbia University 
   - Linux OS. 
- Useful for any school using any of the listed platforms
- Contact developer for other OS/platforms support.

## Installation

Make sure you are using python3.9+

1) Install the package
    ```shell
    pip install canvasdl
    
    ```
2) Obtain Canvas API key
    - Columbia University students
      - Go to Courseworks > Account > Settings
      - Click on "New Access Token"

3) [Optional] Obtain Google Calendar [API key](https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application)
4) [Optional] Specify custom [Calendar ID](https://xfanatical.com/blog/how-to-find-your-google-calendar-id/)
5) Configure your settings:
   ```shell
   canvasdl --configure
   ```
6) Install package for local file management
   - python-xattr
   - [mediainfo](https://manpages.ubuntu.com/manpages/bionic/man1/mediainfo.1.html)
7) [Optional] Install package for UI progress during synchronization
   - python-pyqt6
   - pip install PyQt6

## Usage
Run command to synchronize all content and check for updates
```shell
canvasdl
```

## Quickstart
To quickly experiment with the package you can run the [quickstart](https://github.com/quintenroets/canvasdl/blob/main/examples/quickstart.ipynb) in Google Collab.
The downloaded content will be available in the folder /root/Documents in the Google Collab session.

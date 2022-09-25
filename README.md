# Canvasdl

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
- Developed for students at Columbia University 
- Useful for any school with (partly) the same platforms
- Developed for Linux OS. 
- Contact developer for other platforms support.

## Installation

1) Install the package
    ```shell
    pip install git+https://github.com/quintenroets/canvasdl
    ```
2) Give the courses you want to synchronize a nickname on courseworks. 
   - This will be the name of their local folder with synchronized content
3) Obtain API key
    - Columbia University students
      - Go to Courseworks > Account > Settings
      - Click on "New Access Token"
    - [General instructions](https://community.canvaslms.com/t4/Admin-Guide/How-do-I-add-a-developer-API-key-for-an-account/ta-p/259)
4) Put API key in config file
   - at $HOME/Scripts/assets/canvasdl/config.yaml

## Usage
Run command to synchronize all content
```shell
canvasdl
```

# ClassFlix
*Please note that this project is under production and is not completed yet!*


## Build Instructions
```
$ git clone https://github.com/kshilledar/class-flix
$ sudo pacman -S python-pipenv (depends on your system)
$ pipenv install
Change the necessary required settings in the config.ini file
$ python3 main.py
```

## Working
This project uses OAuth Method to communicate with the google spreadsheet and google drive API.
The `config.ini` file has the necessary settings to make the project work. 
This project ads shares all the videos in `*.mp4` or `*.mkv` format in a gdrive folder to a spreadsheet.

# Screen_Sender

## Программа для захвата скриншотов и сохранения в заданной директории

## Структура проекта:

```python

screen_sender
│
├── screen_sender
│   └── main.py - основная часть программы
│
├── requirements.txt - зависимости
└── README.md

```

## Инструкция
1. создайте и активируйте виртуальное окружение и установите зависимости:
```python
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. скомпилируйте в .exe:
pyinstaller --noconfirm --noconsole --onefile --name=screen_sender --icon=media/icon_.png main.py


## Остальная информация 

ver. 1.0.0

CompanyName: GMG

FileDescription: Screen sender

InternalName: Click_click_screen

LegalCopyright: © GMG. All rights reserved.

OriginalFilename: screen_sender.exe

ProductName: Screen sender

Author: Berdyshev E.A.

Development and support: Berdyshev E.A.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

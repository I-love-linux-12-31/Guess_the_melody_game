# Игра "Угадай мелодию"
ТиВПО Практическая работа 3. Вариант № 86 - 75 = **11**

## Видео демонстрация
[Смотреть видео](https://disk.yandex.com/i/zAXrgHbguIWZLw) или 
[**Скачать файл**](https://github.com/I-love-linux-12-31/Guess_the_melody_game/raw/refs/heads/main/demo_video_2024-11-17%2014-45-11.mkv)

## Используемые библиотеки:
* unittest
* behave
* PyQt6
* pydub

## Варианты запуска
### Развёртывание окружения
```bash
make build
```
### Загрузка ресурсов
[**Скачать**](https://disk.yandex.com/d/xsyBrPdbvjwvqA) демонстрационные ресурсы.<br>
Источник - **Free Music Archive**, все композиции распространяются под **CC BY** лицензией.<br>
Файлы следует поместить в каталог `./resources/music/`
### Запуск тестов
```bash
source venv/bin/activate  
make test
```
### Запуск игры
```bash
source venv/bin/activate  
make run
```

### При работе на ОС Windows
При работе на ОС Windows может потребоваться ручная установка ffmpeg.
Также для установки PyQt6 может потребоваться загрузка средства сборки MSVC v140+ от Microsoft. 

### Автор - Кунецов Ярослав из ИКБО-02-22

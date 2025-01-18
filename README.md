# Block Device Performance Testing Utility

Утилита для тестирования производительности блочных устройств с помощью FIO и построением графиков через gnuplot.

## Системные требования

Перед установкой убедитесь, что в вашей системе установлены:

-   fio
-   gnuplot

### Ubuntu/Debian

```bash
sudo apt-get install fio gnuplot
```

### CentOS/RHEL

```bash
sudo yum install fio gnuplot
```

### Arch Linux

```bash
sudo pacman -S fio gnuplot
```

## Python требования

-   Python 3.6+

## Установка

```bash
git clone https://github.com/w1sq/blktest.git
cd blktest
pip install .
```

## Использование

```bash
blktest --name "Test Name" --filename /dev/sdX --output result.png
```

### Параметры

-   `--name`: Имя теста
-   `--filename`: Путь к тестируемому устройству или файлу
-   `--output`: Путь для сохранения графика результатов (PNG)

## Результаты

Утилита выполняет:

-   Тесты случайного чтения и записи
-   Варьирование глубины очереди ввода-вывода (IO depth)
-   Построение графика зависимости латентности от глубины очереди

График сохраняется в указанный PNG-файл.

## Лицензия

MIT License. См. файл [LICENSE](LICENSE) для подробностей.

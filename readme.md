# pypsgctrl

English documentation is followed by the Russian translation.
После английского текста приведена русская версия.

## English

A synchronous Python driver for the PSG9080 dual-channel function generator over
USB serial. Supports waveforms, frequency, amplitude, offset, duty cycle, phase,
modulation, measurement, sweep, system settings, and parameter memory.

### Installation

Python 3.10 or newer is required. pyserial is installed automatically.

Install the latest release from PyPI:

```sh
python -m pip install pypsgctrl
```

The package is published on [PyPI](https://pypi.org/project/pypsgctrl/).
To install the development version directly from GitHub:

```sh
python -m pip install "git+https://github.com/realspinner/pypsgctrl.git"
```

To install this release from TestPyPI in a fresh virtual environment:

```sh
python -m pip install pyserial
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps pypsgctrl==0.1.2
```

After cloning the repository, use `python -m pip install -e .` for development. Serial settings: 115200 baud,
8-N-1, without flow control. Replace the macOS example port with your device's port.
Opening a connection does not enable outputs.

### Quick start

```python
from pypsgctrl import PSG9080, Waveform

with PSG9080.connect('/dev/cu.usbserial-2120', timeout=1.0) as generator:
    print(generator.ch1.frequency)       # Decimal, Hz
    generator.ch1.waveform = Waveform.SINE
    generator.ch1.frequency = 1000
    generator.ch1.amplitude = '0.100'    # Vpp, not RMS
    generator.ch1.offset = 0            # V
    generator.set_outputs(True, False)
```

Writes take effect immediately. Physical readbacks use Decimal; numeric strings
and Decimal support exact fractions. Values between device steps are rejected.
Transactions are serialized with an instance lock. After a timeout, close and
reopen the connection. Hardware limits absent from the protocol remain the caller's responsibility.

### Documentation and structure

[English API reference](https://github.com/realspinner/pypsgctrl/blob/main/docs/api_reference_en.md) · [Russian API reference](https://github.com/realspinner/pypsgctrl/blob/main/docs/api_reference_ru.md)

| Module | Purpose |
| --- | --- |
| `pypsgctrl/__init__.py` | Stable public imports and version |
| `pypsgctrl/device.py` | Connection, wire exchange, general settings |
| `pypsgctrl/channel.py` | Channel properties, frequency/output control |
| `pypsgctrl/registers.py` | Register metadata and unit conversion |
| `pypsgctrl/enums.py` | Waveform, frequency, modulation, trigger enums |
| `pypsgctrl/errors.py` | Driver exceptions |
| `pypsgctrl/transport.py` | Injectable transport contract |

Public imports use `from pypsgctrl import PSG9080, Waveform`.
Report bugs through [GitHub Issues](https://github.com/realspinner/pypsgctrl/issues). Source comments use Doxygen
tags. With Doxygen installed, run `doxygen Doxyfile` from the repository root to generate
`build/doxygen/html`.

### License

MIT License, copyright 2026 Oleg Kochetov. See [LICENSE](https://github.com/realspinner/pypsgctrl/blob/main/LICENSE).
Vendor PDFs and recorder calibration utilities are not included in this repository.

## Русский

Синхронный Python-драйвер двухканального генератора PSG9080 по USB serial.
Поддерживает форму, частоту, амплитуду, смещение, duty, фазу, модуляцию,
измерение, sweep, системные настройки и память параметров.

### Установка

Требуется Python 3.10 или новее. pyserial устанавливается автоматически.

Установка последнего релиза с PyPI:

```sh
python -m pip install pypsgctrl
```

Пакет опубликован на [PyPI](https://pypi.org/project/pypsgctrl/).
Для установки версии для разработки непосредственно из GitHub:

```sh
python -m pip install "git+https://github.com/realspinner/pypsgctrl.git"
```

Установка этой версии с TestPyPI в новом виртуальном окружении:

```sh
python -m pip install pyserial
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps pypsgctrl==0.1.2
```

После клонирования для разработки: `python -m pip install -e .`. Порт: 115200 baud, 8-N-1,
без flow control. Замените пример macOS на свой порт. Подключение не включает выходы.

### Быстрый старт

```python
from pypsgctrl import PSG9080, Waveform

with PSG9080.connect('/dev/cu.usbserial-2120', timeout=1.0) as generator:
    print(generator.ch1.frequency)       # Decimal, Hz
    generator.ch1.waveform = Waveform.SINE
    generator.ch1.frequency = 1000
    generator.ch1.amplitude = '0.100'    # Vpp, not RMS
    generator.ch1.offset = 0            # V
    generator.set_outputs(True, False)
```

Записи применяются немедленно. Физические значения возвращаются как Decimal;
строки и Decimal позволяют задать точные дроби. Значения между шагами отвергаются.
Обмен защищён блокировкой экземпляра. После таймаута соединение следует открыть
заново. Неописанные в протоколе аппаратные пределы учитывает вызывающий код.

### Документация и структура

[Справочник на английском](https://github.com/realspinner/pypsgctrl/blob/main/docs/api_reference_en.md) · [Справочник на русском](https://github.com/realspinner/pypsgctrl/blob/main/docs/api_reference_ru.md)

| Модуль | Назначение |
| --- | --- |
| `pypsgctrl/__init__.py` | Стабильные публичные импорты и версия |
| `pypsgctrl/device.py` | Соединение, обмен, общие настройки |
| `pypsgctrl/channel.py` | Свойства канала, частота и управление выходом |
| `pypsgctrl/registers.py` | Метаданные регистров и преобразование единиц |
| `pypsgctrl/enums.py` | Перечисления формы, частоты, модуляции и запуска |
| `pypsgctrl/errors.py` | Исключения драйвера |
| `pypsgctrl/transport.py` | Контракт внедряемого транспорта |

Публичные импорты: `from pypsgctrl import PSG9080, Waveform`.
Об ошибках можно сообщить через [GitHub Issues](https://github.com/realspinner/pypsgctrl/issues). Комментарии оформлены
тегами Doxygen. При установленном Doxygen команда `doxygen Doxyfile` из корня репозитория
генерирует `build/doxygen/html`.

### Лицензия

MIT License, правообладатель — Oleg Kochetov, 2026. См. [LICENSE](https://github.com/realspinner/pypsgctrl/blob/main/LICENSE).
PDF производителя и утилиты калибровки рекордера в репозиторий не включены.

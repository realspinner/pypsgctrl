# pypsg

[English](#english) · [Русский](#русский)

## English

A synchronous Python driver for the PSG9080 dual-channel function generator over
USB serial. Supports waveforms, frequency, amplitude, offset, duty cycle, phase,
modulation, measurement, sweep, system settings, and parameter memory.

### Installation

Python >= 3.10 and pyserial >= 3.5 are required. After cloning the repository,
install from the repository root:

```sh
python -m pip install .
```

For development, use `python -m pip install -e .`. Serial settings: 115200 baud,
8-N-1, without flow control. Replace the macOS example port with your device's port.
Opening a connection does not enable outputs.

### Quick start

```python
from pypsg import PSG9080, Waveform

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

[English API reference](docs/api_reference_en.md) · [Russian API reference](docs/api_reference_ru.md)

| Module | Purpose |
| --- | --- |
| `pypsg/__init__.py` | Stable public imports and version |
| `pypsg/device.py` | Connection, wire exchange, general settings |
| `pypsg/channel.py` | Channel properties, frequency/output control |
| `pypsg/registers.py` | Register metadata and unit conversion |
| `pypsg/enums.py` | Waveform, frequency, modulation, trigger enums |
| `pypsg/errors.py` | Driver exceptions |
| `pypsg/transport.py` | Injectable transport contract |

Imports remain `from pypsg import PSG9080, Waveform`. Source comments use Doxygen
tags. With Doxygen installed, run `doxygen Doxyfile` from the repository root to generate
`build/doxygen/html`.

### Validation

```sh
python -m unittest discover -s tests -v
```

13 library tests use fake transports and require no hardware. They cover wire
commands, scaling, errors, transport lifecycle, serial settings, and readback validation.

Read/write checks were performed on 2026-10-07 at 115200, 8-N-1. The device returned
`:ok` and the user confirmed visible changes. Analog output accuracy was not verified. Protocol ambiguities are documented in the reference.
Initial brightness 101 could not be restored because writes are clamped to 100.

### License

MIT License, copyright 2026 Oleg Kochetov. See [LICENSE](LICENSE).
Vendor PDFs and recorder calibration utilities are not included in this repository.

## Русский

Синхронный Python-драйвер двухканального генератора PSG9080 по USB serial.
Поддерживает форму, частоту, амплитуду, смещение, duty, фазу, модуляцию,
измерение, sweep, системные настройки и память параметров.

### Установка

Требуются Python >= 3.10 и pyserial >= 3.5. После клонирования установите пакет из корня репозитория:

```sh
python -m pip install .
```

Для разработки: `python -m pip install -e .`. Порт: 115200 baud, 8-N-1,
без flow control. Замените пример macOS на свой порт. Подключение не включает выходы.

### Быстрый старт

```python
from pypsg import PSG9080, Waveform

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

[Справочник на английском](docs/api_reference_en.md) · [Справочник на русском](docs/api_reference_ru.md)

| Модуль | Назначение |
| --- | --- |
| `pypsg/__init__.py` | Стабильные публичные импорты и версия |
| `pypsg/device.py` | Соединение, обмен, общие настройки |
| `pypsg/channel.py` | Свойства канала, частота и управление выходом |
| `pypsg/registers.py` | Метаданные регистров и преобразование единиц |
| `pypsg/enums.py` | Перечисления формы, частоты, модуляции и запуска |
| `pypsg/errors.py` | Исключения драйвера |
| `pypsg/transport.py` | Контракт внедряемого транспорта |

Импорты сохранены: `from pypsg import PSG9080, Waveform`. Комментарии оформлены
тегами Doxygen. При установленном Doxygen команда `doxygen Doxyfile` из корня репозитория
генерирует `build/doxygen/html`.

### Проверка

```sh
python -m unittest discover -s tests -v
```

13 тестов библиотеки используют имитацию транспорта и не требуют прибора.
Проверяются команды, масштабы, ошибки, жизненный цикл, serial-настройки и ответы.

Чтение/запись проверены 2026-10-07 с 115200, 8-N-1. Прибор возвращает `:ok`,
пользователь подтвердил видимые изменения. Точность аналогового выхода не проверялась. Неоднозначности протокола описаны в справочнике.
Исходная яркость 101 не восстановилась: прибор ограничивает запись значением 100.

### Лицензия

MIT License, правообладатель — Oleg Kochetov, 2026. См. [LICENSE](LICENSE).
PDF производителя и утилиты калибровки рекордера в репозиторий не включены.

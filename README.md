# PDF Label Generator

Консольное приложение на Python для генерации PDF-файлов с этикетками, каждая из которых содержит **DataMatrix** и текст на кириллице.

Размер страницы: **7×4 см**, макет разделён на левую часть с DataMatrix и правую часть с текстом.

---

## 📦 Зависимости

- Python 3.8+ (подходит и для 3.12)
- [ReportLab](https://pypi.org/project/reportlab/) — генерация PDF
- [Pillow](https://pypi.org/project/Pillow/) — работа с изображениями
- [pystrich](https://pypi.org/project/pystrich/) — генерация DataMatrix

Установить зависимости:

```bash
pip install reportlab Pillow pystrich
```

---

## 🗂 Структура проекта

```
labler/
│
├── main.py          # Скрипт генерации PDF
├── marks.txt        # Файл с данными для DataMatrix (по одной строке на этикетку)
└── DejaVuSans.ttf   # Опционально: локальный шрифт для кириллицы
```

---

## 📝 Использование

1. Подготовьте файл `marks.txt` с одной строкой на этикетку:

```
12345678901234567890
ABCDEF123456
Пробная метка №1
Другая метка 0002
```

2. Запустите скрипт:

```bash
python main.py
```

3. На выходе будет файл `labels.pdf` с одной этикеткой на каждой странице.

---

## ⚙️ Настройка макета

- Размер страницы: `7 × 4 см`
- Левая часть — DataMatrix из `marks.txt`
- Правая часть — текст:

```
Масло "СКАТ"
для 2-тактного
двигателя
бензопилы
0,95 л
```

- Шрифт для кириллицы выбирается автоматически из системы. Можно положить `DejaVuSans.ttf` рядом со скриптом.

---

## 🔧 Дополнительно

Можно добавить:

- Рамку вокруг этикетки для резки:

```python
c.rect(0.1*cm, 0.1*cm, page_width-0.2*cm, page_height-0.2*cm)
```

- Разделительную вертикальную линию между QR и текстом:

```python
c.line(page_width/2, 0.2*cm, page_width/2, page_height-0.2*cm)
```

- Автоматическое центрирование текста по вертикали при изменении количества строк.

---

## ✅ Совместимость

Работает на **Windows, Linux и macOS**.  
Поддерживает Python 3.8–3.12 без установки внешних C-библиотек.api key: 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

import os
import platform
from io import BytesIO

from PIL import Image
from pystrich.datamatrix import DataMatrixEncoder  # ✅ правильный генератор
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def get_font_path():
    """Возвращает путь к шрифту с поддержкой кириллицы."""
    system = platform.system()
    candidates = []

    if system == "Windows":
        candidates = [
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\calibri.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
        ]
    elif system == "Darwin":
        candidates = [
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]

    for path in candidates:
        if os.path.exists(path):
            return path

    local_font = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    if os.path.exists(local_font):
        return local_font

    raise FileNotFoundError("Не найден подходящий TTF-шрифт с поддержкой кириллицы.")


def generate_datamatrix(data: str, size_mm: float = 15.0) -> Image:
    """Генерация DataMatrix с помощью pystrich."""
    encoder = DataMatrixEncoder(data)
    png_bytes = encoder.get_imagedata()  # байты PNG
    img = Image.open(BytesIO(png_bytes))

    dpi = 300
    size_px = int(size_mm / 25.4 * dpi)
    img = img.resize((size_px, size_px), Image.Resampling.NEAREST)
    img = img.convert("1")

    return img


def generate_labels(filename="labels.pdf", marks_file="marks.txt"):
    font_path = get_font_path()
    font_name = "CyrFont"
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    # Размер страницы (7x4 см)
    page_width, page_height = 7 * cm, 4 * cm
    c = canvas.Canvas(filename, pagesize=(page_width, page_height))

    label_text = 'Масло "СКАТ"\nдля 2-тактного\nдвигателя\nбензопилы\n0,95 л'

    if not os.path.exists(marks_file):
        raise FileNotFoundError(f"Файл {marks_file} не найден.")
    with open(marks_file, "r", encoding="utf-8") as f:
        marks = [line.strip() for line in f if line.strip()]

    for mark in marks:
        # DataMatrix
        qr_img = generate_datamatrix(mark, size_mm=20)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG", dpi=(300, 300))
        qr_buffer.seek(0)
        qr_reader = ImageReader(qr_buffer)

        # Левая часть (QR)
        qr_size = 2.0 * cm
        qr_x = 0.7 * cm
        qr_y = (page_height - qr_size) / 2
        c.drawImage(qr_reader, qr_x, qr_y, width=qr_size, height=qr_size, preserveAspectRatio=True, mask="auto")

        # Разделительная линия
        # c.setLineWidth(0.5)
        # c.line(page_width / 2, 0.5 * cm, page_width / 2, page_height - 0.5 * cm)

        # Правая часть (текст)
        text_x = page_width / 2 + 0.1 * cm
        text_y = page_height / 2 + 0.8 * cm
        c.setFont(font_name, 9)
        for line in label_text.split("\n"):
            c.drawString(text_x, text_y, line)
            text_y -= 0.5 * cm

        c.showPage()

    c.save()
    print(f"PDF-файл '{filename}' успешно создан ({len(marks)} этикеток).")


if __name__ == "__main__":
    generate_labels()

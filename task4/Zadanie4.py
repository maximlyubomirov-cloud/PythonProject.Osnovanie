# -*- coding: utf-8 -*-
"""
Графический редактор — Ribbon UI
Единая лента. Панель слоёв — сегментированные карточки.
Тема синхронизируется с Windows 11.

Возможности:
    • Векторное рисование, ластик стирает область = толщине кисти
    • Рисование поверх стёртого
    • Прозрачный слой + ручное масштабирование за квадратики
    • Рисование ограничено пунктирной рамкой слоя
    • Пунктир с отступом внутрь холста, не упирается в край
    • Перетаскивание рамки: Alt + левая кнопка мыши
    • Кнопки Ribbon не мигают светлым в тёмной теме
    • Радиокнопки слоя со стилем Windows 11
    • Глаз 👁 на Canvas
    • Палитра + толщина + прозрачность слоя рисунка — в карточке «Параметры кисти»
    • Кнопка-ластик в ряду выбора цвета кисти
    • Кнопка темы и индикатор активного цвета — в правом верхнем углу ленты
    • Ползунок прозрачности выбранного пункта — в карточке «Слои»
    • Клик по строке «Изображение фона» — открыть изображение
    • Клик по строке «Цвет фона» — выбрать цвет фона
    • Кнопка «Открыть» в ленте — загрузить изображение (PNG/JPEG/BMP/WebP/EXR)
    • Автосохранение с выбором интервала (Выкл / 1 / 5 / 10 / 30 мин)
    • Панель слоёв прокручивается — все элементы видны при маленьком окне
    • Фон: цвет + изображение
    • Сохранение PNG / JPEG / BMP / WebP / EXR
    • Undo / Redo (Ctrl+Z / Ctrl+Y)
    • Горячие клавиши Ctrl+S, Ctrl+O, Ctrl+N, Ctrl+Shift+S, B, E
    • Кэш рендера слоя, интерполированный ластик
    • Всплывающие подсказки на кнопках, ползунках и глазах
    • Сохранить и выйти (с диалогом сохранения)
    • Закрытие окна крестиком тоже спрашивает про сохранение

Зависимости:
    pip install Pillow
    pip install openexr-numpy
"""

from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog as fd
from tkinter import messagebox as mb

try:
    from PIL import Image, ImageDraw, ImageTk, ImageChops

    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    from openexr_numpy import imwrite, imread
    import numpy as np

    EXR_OK = True
except ImportError:
    EXR_OK = False

try:
    import winreg

    WINREG_OK = True
except ImportError:
    WINREG_OK = False

# =========================================================
#  ЦВЕТОВАЯ СХЕМА
# =========================================================
THEME = {
    "light": {
        "bg": "#F3F3F3", "toolbar": "#FAFAFA", "card": "#FFFFFF",
        "hover": "#E5F0FA", "text": "#1C1C1C", "muted": "#616161",
        "accent": "#0067C0", "accent_hov": "#1975C5", "accent_fg": "#FFFFFF",
        "border": "#E5E5E5", "canvas": "#FFFFFF",
        "disabled_fg": "#8A8A8A", "disabled_bg": "#DDDDDD",
        "layer_active": "#E5F0FA",
        "sel_border": "#1C1C1C",
        "checker_a": "#FFFFFF", "checker_b": "#E6E6E6",
        "handle_fill": "#FFFFFF", "handle_outline": "#0067C0",
    },
    "dark": {
        "bg": "#202020", "toolbar": "#2B2B2B", "card": "#2D2D2D",
        "hover": "#3A4A5A", "text": "#FFFFFF", "muted": "#A0A0A0",
        "accent": "#4CC2FF", "accent_hov": "#66CBFF", "accent_fg": "#000000",
        "border": "#3A3A3A", "canvas": "#2D2D2D",
        "disabled_fg": "#B0B0B0", "disabled_bg": "#3A3A3A",
        "layer_active": "#2A5A85",
        "sel_border": "#FFFFFF",
        "checker_a": "#2D2D2D", "checker_b": "#262626",
        "handle_fill": "#2D2D2D", "handle_outline": "#4CC2FF",
    },
}

T = dict(THEME["light"])
theme_name = "light"

FONT = "Segoe UI"
FONT_BTN = (FONT, 10)
FONT_SMALL = (FONT, 9)
ICON_FONT = ("Segoe MDL2 Assets", 16)

HANDLE_SIZE = 5


def is_windows_dark_theme():
    if not WINREG_OK:
        return False
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value == 0
    except Exception:
        return False


# =========================================================
#  ГЛАВНОЕ ОКНО
# =========================================================
root = Tk()
root.title("Графический редактор — векторные линии")
root.geometry("1100x760")
root.minsize(640, 420)
root.configure(bg=T["bg"])

pen_width = 5
color = "#E53935"

canvas_width = 800
canvas_height = 500

opacity_target = 0
draw_mode = "brush"
cursor_x, cursor_y = 0, 0

opacity_var = None
opacity_scale = None
opacity_hint = None
layer_opacity_var = None
layer_opacity_scale = None
width_var = None
width_entry = None
width_scale = None
btn_theme = None

brush_btn = None
eraser_btn = None
eraser_palette_btn = None

rb_choice = None
cb_layer = None
cb_image = None
cb_color = None

eye_layer = None
eye_image = None
eye_color = None

color_indicator = None
palette_frames = []
palette_buttons = []
scale_buttons = {}
layer_rows = {}

# --- Автосохранение ---
autosave_enabled = False
autosave_interval_min = 5
autosave_after_id = None
autosave_last_path = None
autosave_var = None
autosave_menu = None

AUTOSAVE_CHOICES = {
    "Выкл": 0,
    "1 минута": 1,
    "5 минут": 5,
    "10 минут": 10,
    "30 минут": 30,
}

# --- Состояние ручного масштабирования слоя «за квадратики» ---
transform_handle = None
transform_start_bbox = None
transform_start_mouse = None
transform_start_scale = None
transform_guides_visible = True

# --- Состояние перетаскивания рамки целиком (Alt + ЛКМ) ---
drag_active = False
drag_start_mouse = None
drag_start_tx_ty = None


# =========================================================
#  ХЕЛПЕРЫ ЦВЕТА
# =========================================================
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return (int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16))


def hex_to_rgba(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return (r, g, b, 255)


def make_checkerboard(w, h, cell=12):
    w = max(1, w)
    h = max(1, h)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    a = hex_to_rgba(T["checker_a"])
    b = hex_to_rgba(T["checker_b"])
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            col = a if ((x // cell) + (y // cell)) % 2 == 0 else b
            draw.rectangle([x, y, x + cell - 1, y + cell - 1], fill=col)
    return img


def load_image_any(file):
    """
    Универсальная загрузка изображения в PIL.Image (RGBA).
    PNG/JPEG/BMP/WebP — через Pillow; EXR — через openexr-numpy.
    """
    lower = file.lower()
    if lower.endswith(".exr"):
        if not EXR_OK:
            raise RuntimeError(
                "Для открытия .exr установите openexr-numpy:\n"
                "    pip install openexr-numpy"
            )
        arr = imread(file)
        arr = np.clip(arr, 0.0, 1.0)
        arr = (arr * 255.0 + 0.5).astype(np.uint8)

        if arr.ndim == 2:
            img = Image.fromarray(arr, mode="L").convert("RGBA")
        elif arr.shape[2] == 3:
            img = Image.fromarray(arr, mode="RGB").convert("RGBA")
        elif arr.shape[2] == 4:
            img = Image.fromarray(arr, mode="RGBA")
        else:
            raise RuntimeError(
                f"Неподдерживаемое число каналов в EXR: {arr.shape[2]}")
        return img
    else:
        return Image.open(file).convert("RGBA")


# =========================================================
#  МОДЕЛЬ ФОНА
# =========================================================
class Background:
    def __init__(self):
        self.color = "#FFFFFF"
        self.source_image = None
        self.scale_mode = "fit"
        self.filename = None
        self.color_visible = True
        self.image_visible = True
        self.color_opacity = 1.0
        self.image_opacity = 1.0

    def is_image(self):
        return self.source_image is not None

    def clear_image(self):
        self.source_image = None
        self.filename = None

    def render(self, w, h):
        w = max(1, w)
        h = max(1, h)

        if self.color_visible:
            r, g, b = hex_to_rgb(self.color)
            a = int(255 * self.color_opacity)
            base = Image.new("RGBA", (w, h), (r, g, b, a))
        else:
            base = Image.new("RGBA", (w, h), (0, 0, 0, 0))

        if self.is_image() and self.image_visible:
            img = self.source_image.copy()

            if self.scale_mode == "stretch":
                img = img.resize((w, h), Image.LANCZOS)
            elif self.scale_mode == "fit":
                img.thumbnail((w, h), Image.LANCZOS)
                canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                x = (w - img.width) // 2
                y = (h - img.height) // 2
                canvas.paste(img, (x, y), img)
                img = canvas
            elif self.scale_mode == "cover":
                ratio = max(w / img.width, h / img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)
                x = (img.width - w) // 2
                y = (img.height - h) // 2
                img = img.crop((x, y, x + w, y + h))

            if self.image_opacity < 1.0:
                r, g, b, a = img.split()
                a = a.point(lambda v: int(v * self.image_opacity))
                img = Image.merge("RGBA", (r, g, b, a))

            base = Image.alpha_composite(base, img)

        return base


background = Background()


# =========================================================
#  МОДЕЛЬ СЛОЯ
# =========================================================
class Layer:
    _counter = 0

    def __init__(self, name=None, width=None, height=None):
        Layer._counter += 1
        self.name = name or f"Слой {Layer._counter}"
        self.visible = True
        self.opacity = 1.0
        self.scale_mode = "stretch"
        self.tx = 0.0
        self.ty = 0.0
        self.tsx = 1.0
        self.tsy = 1.0

        self.width = width or canvas_width
        self.height = height or canvas_height
        self.shapes = []
        self.erase_mask = Image.new("L", (self.width, self.height), 0)
        self._cache = None
        self._cache_dirty = True

    def clear(self):
        self.shapes.clear()
        self.erase_mask = Image.new("L", (self.width, self.height), 0)
        self.tx = self.ty = 0.0
        self.tsx = self.tsy = 1.0
        self._cache_dirty = True

    def reset_transform(self):
        self.tx = self.ty = 0.0
        self.tsx = self.tsy = 1.0
        self._cache_dirty = True

    def resize(self, new_w, new_h):
        if new_w == self.width and new_h == self.height:
            return
        sx = new_w / self.width
        sy = new_h / self.height

        self.erase_mask = self.erase_mask.resize((new_w, new_h), Image.LANCZOS)

        for s in self.shapes:
            s["points"] = [
                (int(x * sx), int(y * sy)) for (x, y) in s["points"]
            ]

        self.width = new_w
        self.height = new_h
        self._cache_dirty = True

    def clear_erase_in_stroke(self, x0, y0, x1, y1):
        draw = ImageDraw.Draw(self.erase_mask)
        draw.line([x0, y0, x1, y1],
                  fill=0,
                  width=max(1, pen_width))
        self._cache_dirty = True

    def add_point(self, x, y):
        lx, ly = self.canvas_to_layer(x, y)

        if not self.shapes or self.shapes[-1].get("_closed", False):
            self.shapes.append({
                "points": [(lx, ly)],
                "color": color,
                "width": pen_width,
                "_closed": False,
            })
        else:
            last_pt = self.shapes[-1]["points"][-1]
            self.clear_erase_in_stroke(last_pt[0], last_pt[1], lx, ly)
            self.shapes[-1]["points"].append((lx, ly))
        self._cache_dirty = True

    def finish_stroke(self):
        if self.shapes:
            self.shapes[-1]["_closed"] = True
        self._cache_dirty = True

    def erase_at(self, x0, y0, x1, y1, radius):
        lx0, ly0 = self.canvas_to_layer(x0, y0)
        lx1, ly1 = self.canvas_to_layer(x1, y1)

        draw = ImageDraw.Draw(self.erase_mask)
        if lx0 == lx1 and ly0 == ly1:
            draw.ellipse(
                [lx0 - radius, ly0 - radius, lx0 + radius, ly0 + radius],
                fill=255,
            )
        else:
            draw.line([lx0, ly0, lx1, ly1], fill=255, width=radius * 2)
            draw.ellipse(
                [lx1 - radius, ly1 - radius, lx1 + radius, ly1 + radius],
                fill=255,
            )
        self._cache_dirty = True

    def canvas_to_layer(self, x, y):
        w, h = self.width, self.height
        cw, ch = canvas_width, canvas_height

        if self.scale_mode == "fit":
            ratio = min(cw / w, ch / h)
            disp_w = w * ratio
            disp_h = h * ratio
            ox = (cw - disp_w) / 2
            oy = (ch - disp_h) / 2
            lx = (x - ox) / ratio
            ly = (y - oy) / ratio
        elif self.scale_mode == "cover":
            ratio = max(cw / w, ch / h)
            disp_w = w * ratio
            disp_h = h * ratio
            ox = (cw - disp_w) / 2
            oy = (ch - disp_h) / 2
            lx = (x - ox) / ratio
            ly = (y - oy) / ratio
        else:  # stretch
            lx = (x / cw) * w
            ly = (y / ch) * h

        sx = self.tsx if self.tsx != 0 else 1.0
        sy = self.tsy if self.tsy != 0 else 1.0
        cx = w * self.tx
        cy = h * self.ty
        return (lx - cx) / sx, (ly - cy) / sy

    def layer_to_canvas(self, lx, ly):
        w, h = self.width, self.height
        cw, ch = canvas_width, canvas_height

        sx = self.tsx
        sy = self.tsy
        cx = w * self.tx
        cy = h * self.ty
        dx = lx * sx + cx
        dy = ly * sy + cy

        if self.scale_mode == "fit":
            ratio = min(cw / w, ch / h)
            disp_w = w * ratio
            disp_h = h * ratio
            ox = (cw - disp_w) / 2
            oy = (ch - disp_h) / 2
            return ox + dx * ratio, oy + dy * ratio
        elif self.scale_mode == "cover":
            ratio = max(cw / w, ch / h)
            disp_w = w * ratio
            disp_h = h * ratio
            ox = (cw - disp_w) / 2
            oy = (ch - disp_h) / 2
            return ox + dx * ratio, oy + dy * ratio
        else:  # stretch
            return dx * (cw / w), dy * (ch / h)

    def contains_canvas_point(self, x, y, margin=0.0):
        x0, y0, x1, y1 = self.current_bbox()
        return (x0 - margin <= x <= x1 + margin and
                y0 - margin <= y <= y1 + margin)

    def clip_segment_to_bbox(self, x0, y0, x1, y1):
        bx0, by0, bx1, by1 = self.current_bbox()
        dx = x1 - x0
        dy = y1 - y0
        p = [-dx, dx, -dy, dy]
        q = [x0 - bx0, bx1 - x0, y0 - by0, by1 - y0]
        u1, u2 = 0.0, 1.0
        for pi, qi in zip(p, q):
            if pi == 0:
                if qi < 0:
                    return None
            else:
                t = qi / pi
                if pi < 0:
                    if t > u2:
                        return None
                    if t > u1:
                        u1 = t
                else:
                    if t < u1:
                        return None
                    if t < u2:
                        u2 = t
        nx0 = x0 + u1 * dx
        ny0 = y0 + u1 * dy
        nx1 = x0 + u2 * dx
        ny1 = y0 + u2 * dy
        return nx0, ny0, nx1, ny1

    def current_bbox(self):
        x0, y0 = self.layer_to_canvas(0, 0)
        x1, y1 = self.layer_to_canvas(self.width, self.height)
        return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))

    def clamp_to_canvas(self):
        cw, ch = canvas_width, canvas_height

        x0, y0 = self.layer_to_canvas(0, 0)
        x1, y1 = self.layer_to_canvas(self.width, self.height)
        bw = max(1e-6, abs(x1 - x0))
        bh = max(1e-6, abs(y1 - y0))

        kx = bw / (self.width * max(1e-6, self.tsx))
        ky = bh / (self.height * max(1e-6, self.tsy))

        max_tsx = cw / (self.width * kx) if kx > 0 else self.tsx
        max_tsy = ch / (self.height * ky) if ky > 0 else self.tsy
        self.tsx = min(max(0.05, self.tsx), max(0.05, max_tsx))
        self.tsy = min(max(0.05, self.tsy), max(0.05, max_tsy))

        x0, y0 = self.layer_to_canvas(0, 0)
        x1, y1 = self.layer_to_canvas(self.width, self.height)
        bx0, by0 = min(x0, x1), min(y0, y1)
        bx1, by1 = max(x0, x1), max(y0, y1)

        step_x = kx * self.tsx * self.width if self.width else 1.0
        step_y = ky * self.tsy * self.height if self.height else 1.0

        if bx0 < 0:
            self.tx += (-bx0) / step_x
        if by0 < 0:
            self.ty += (-by0) / step_y
        if bx1 > cw:
            self.tx -= (bx1 - cw) / step_x
        if by1 > ch:
            self.ty -= (by1 - ch) / step_y

        self._cache_dirty = True

    def render(self):
        if self._cache is not None and not self._cache_dirty \
                and self._cache.size == (canvas_width, canvas_height):
            return self._cache

        w = canvas_width
        h = canvas_height

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for s in self.shapes:
            pts = s.get("points", [])
            if len(pts) < 2:
                continue
            pts_canvas = [self.layer_to_canvas(x, y) for (x, y) in pts]
            draw.line(pts_canvas,
                      fill=hex_to_rgba(s.get("color", "#000000")),
                      width=s.get("width", 1),
                      joint="curve")

        if self.erase_mask is not None:
            mask_src = self.erase_mask
            new_w = max(1, int(round(self.width * self.tsx)))
            new_h = max(1, int(round(self.height * self.tsy)))
            mask_scaled = mask_src.resize((new_w, new_h), Image.LANCZOS)

            mask_canvas = Image.new("L", (w, h), 0)

            if self.scale_mode == "fit":
                ratio = min(w / self.width, h / self.height)
                disp_w = self.width * ratio
                disp_h = self.height * ratio
                ox = (w - disp_w) / 2
                oy = (h - disp_h) / 2
                target_w = int(round(new_w * ratio))
                target_h = int(round(new_h * ratio))
                px = int(ox + self.width * self.tx * ratio)
                py = int(oy + self.height * self.ty * ratio)
            elif self.scale_mode == "cover":
                ratio = max(w / self.width, h / self.height)
                disp_w = self.width * ratio
                disp_h = self.height * ratio
                ox = (w - disp_w) / 2
                oy = (h - disp_h) / 2
                target_w = int(round(new_w * ratio))
                target_h = int(round(new_h * ratio))
                px = int(ox + self.width * self.tx * ratio)
                py = int(oy + self.height * self.ty * ratio)
            else:  # stretch
                rw = w / self.width
                rh = h / self.height
                target_w = int(round(new_w * rw))
                target_h = int(round(new_h * rh))
                px = int(self.width * self.tx * rw)
                py = int(self.height * self.ty * rh)

            if target_w > 0 and target_h > 0:
                mask_scaled = mask_scaled.resize((target_w, target_h),
                                                 Image.LANCZOS)
                mask_canvas.paste(mask_scaled, (px, py))

            inv = mask_canvas.point(lambda v: 255 - v)
            r, g, b, a = img.split()
            a = ImageChops.multiply(a, inv)
            img.putalpha(a)

        if self.opacity < 1.0:
            r, g, b, a = img.split()
            a = a.point(lambda v: int(v * self.opacity))
            img = Image.merge("RGBA", (r, g, b, a))

        self._cache = img
        self._cache_dirty = False
        return img


layers = []
active_layer_index = 0

# =========================================================
#  UNDO / REDO
# =========================================================
undo_stack = []
redo_stack = []
UNDO_LIMIT = 40


def _snapshot_layer(layer):
    return {
        "shapes": [dict(s, points=list(s["points"])) for s in layer.shapes],
        "mask": layer.erase_mask.copy(),
        "tx": layer.tx, "ty": layer.ty,
        "tsx": layer.tsx, "tsy": layer.tsy,
    }


def push_undo():
    layer = get_draw_layer()
    if layer is None:
        return
    undo_stack.append(_snapshot_layer(layer))
    if len(undo_stack) > UNDO_LIMIT:
        undo_stack.pop(0)
    redo_stack.clear()


def _restore(snapshot):
    layer = get_draw_layer()
    if layer is None:
        return
    layer.shapes = [dict(s, points=list(s["points"]))
                    for s in snapshot["shapes"]]
    layer.erase_mask = snapshot["mask"].copy()
    layer.tx = snapshot["tx"]
    layer.ty = snapshot["ty"]
    layer.tsx = snapshot["tsx"]
    layer.tsy = snapshot["tsy"]
    layer._cache_dirty = True
    redraw_canvas()


def undo():
    if not undo_stack:
        return
    layer = get_draw_layer()
    if layer is None:
        return
    redo_stack.append(_snapshot_layer(layer))
    _restore(undo_stack.pop())


def redo():
    if not redo_stack:
        return
    layer = get_draw_layer()
    if layer is None:
        return
    undo_stack.append(_snapshot_layer(layer))
    _restore(redo_stack.pop())


def _clear_history():
    undo_stack.clear()
    redo_stack.clear()


# =========================================================
#  КОМПОЗИЦИЯ
# =========================================================
def compose():
    base = background.render(canvas_width, canvas_height)
    for layer in layers:
        if not layer.visible:
            continue
        img = layer.render()
        base = Image.alpha_composite(base, img)
    return base


def redraw_canvas():
    composed = compose()
    photo = ImageTk.PhotoImage(composed)
    display_canvas.delete("all")
    display_canvas.create_image(0, 0, anchor=NW, image=photo)
    display_canvas.image = photo

    if transform_guides_visible and layers:
        _draw_transform_guides()

    if draw_mode == "eraser":
        r = max(1, pen_width // 2)
        display_canvas.create_oval(
            cursor_x - r, cursor_y - r,
            cursor_x + r, cursor_y + r,
            outline=T["accent"], width=2, dash=(3, 3)
        )


def _draw_transform_guides():
    layer = get_draw_layer()
    if layer is None:
        return
    x0, y0, x1, y1 = layer.current_bbox()

    MARGIN = 2
    dx0 = x0 + MARGIN
    dy0 = y0 + MARGIN
    dx1 = x1 - MARGIN
    dy1 = y1 - MARGIN

    if dx1 - dx0 < 1 or dy1 - dy0 < 1:
        return

    display_canvas.create_rectangle(
        dx0, dy0, dx1, dy1,
        outline=T["accent"], width=1, dash=(4, 3)
    )
    for name, hx, hy in _handle_positions(dx0, dy0, dx1, dy1):
        display_canvas.create_rectangle(
            hx - HANDLE_SIZE, hy - HANDLE_SIZE,
            hx + HANDLE_SIZE, hy + HANDLE_SIZE,
            fill=T["handle_fill"], outline=T["handle_outline"], width=2
        )


def _handle_positions(x0, y0, x1, y1):
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    return [
        ("nw", x0, y0), ("n", cx, y0), ("ne", x1, y0),
        ("e", x1, cy), ("se", x1, y1), ("s", cx, y1),
        ("sw", x0, y1), ("w", x0, cy),
    ]


def _hit_handle(x, y):
    if not layers:
        return None
    x0, y0, x1, y1 = layers[0].current_bbox()
    MARGIN = 2
    dx0, dy0, dx1, dy1 = x0 + MARGIN, y0 + MARGIN, x1 - MARGIN, y1 - MARGIN
    for name, hx, hy in _handle_positions(dx0, dy0, dx1, dy1):
        if abs(x - hx) <= HANDLE_SIZE + 2 and abs(y - hy) <= HANDLE_SIZE + 2:
            return name
    return None


def _cursor_for_handle(name):
    return {
        "nw": "size_nw_se", "se": "size_nw_se",
        "ne": "size_ne_sw", "sw": "size_ne_sw",
        "n": "size_ns", "s": "size_ns",
        "e": "size_we", "w": "size_we",
    }.get(name, "arrow")


# =========================================================
#  ВСПЛЫВАЮЩАЯ ПОДСКАЗКА
# =========================================================
class ToolTip:
    def __init__(self, widget, text, delay=450):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self.after_id = None

        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._cancel, add="+")
        widget.bind("<ButtonPress>", self._cancel, add="+")

    def _schedule(self, event=None):
        self._cancel()
        try:
            self.after_id = self.widget.after(self.delay, self._show)
        except Exception:
            pass

    def _cancel(self, event=None):
        if self.after_id:
            try:
                self.widget.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None
        self._hide()

    def _show(self):
        if self.tip_window is not None:
            return
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        except Exception:
            return
        self.tip_window = Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        Label(self.tip_window, text=self.text,
              font=(FONT, 9), bg="#FFFFE0", fg="#1F1F1F",
              relief=SOLID, bd=1, padx=8, pady=4,
              justify=LEFT).pack()

    def _hide(self):
        if self.tip_window is not None:
            self.tip_window.destroy()
            self.tip_window = None


# =========================================================
#  RIBBON
# =========================================================
ribbon = Frame(root, bg=T["bg"], height=150)
ribbon.pack(fill=X)
ribbon.pack_propagate(False)

ribbon_content = Frame(ribbon, bg=T["bg"])
ribbon_content.pack(side=LEFT, fill=BOTH, expand=1, padx=8, pady=6)

ribbon_right = Frame(ribbon, bg=T["bg"])
ribbon_right.pack(side=RIGHT, fill=Y, padx=(0, 10), pady=6)


def make_group(parent, title):
    card = Frame(parent, bg=T["card"],
                 highlightthickness=1,
                 highlightbackground=T["border"],
                 bd=0)
    card.pack(side=LEFT, fill=Y, padx=(6, 0), pady=0)

    if title:
        lbl = Label(card, text=title, font=(FONT, 8, "bold"),
                    bg=T["card"], fg=T["muted"], anchor="w")
        lbl._role = "caption"
        lbl.pack(side=TOP, anchor="w", padx=8, pady=(6, 0))

    inner = Frame(card, bg=T["card"])
    inner.pack(side=TOP, fill=BOTH, expand=1, padx=6, pady=(2, 6))
    return inner


def ribbon_button(parent, icon, text, command, primary=False, tooltip=None):
    wrap = Frame(parent, bg=T["card"])
    wrap.pack(side=LEFT, padx=4, pady=4)

    btn = Button(wrap, text=icon, command=command,
                 font=ICON_FONT,
                 bd=0, relief=FLAT,
                 width=3, height=1, cursor="hand2",
                 highlightthickness=0)
    btn.pack()
    btn._primary = primary
    btn._is_palette = False

    lbl = Label(wrap, text=text, font=(FONT, 8),
                bg=T["card"], fg=T["muted"])
    lbl._role = "caption"
    lbl.pack(pady=(2, 0))

    if tooltip:
        ToolTip(btn, tooltip)
        ToolTip(lbl, tooltip)
        ToolTip(wrap, tooltip)

    def _base_bg():
        return T["accent"] if btn._primary else T["card"]

    def _base_fg():
        return T["accent_fg"] if btn._primary else T["text"]

    def _hover_bg():
        return T["accent_hov"] if btn._primary else T["hover"]

    def _apply(state="normal"):
        if state == "hover":
            btn.config(bg=_hover_bg())
        else:
            btn.config(bg=_base_bg(), fg=_base_fg(),
                       activebackground=_hover_bg(),
                       activeforeground=_base_fg())

    def on_enter(e):
        if btn["state"] != DISABLED:
            _apply("hover")

    def on_leave(e):
        if btn["state"] != DISABLED:
            _apply("normal")

    def on_release(e):
        _apply("normal")
        root.after(20, lambda: _apply("normal"))

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<ButtonRelease-1>", on_release)

    _apply("normal")
    return btn


# =========================================================
#  ОСНОВНАЯ ОБЛАСТЬ
# =========================================================
main_area = Frame(root, bg=T["bg"])
main_area.pack(fill=BOTH, expand=1, padx=14, pady=(10, 0))

canvas_column = Frame(main_area, bg=T["bg"])
canvas_column.pack(side=LEFT, fill=BOTH, expand=1)

canvas_wrap = Frame(canvas_column, bg=T["bg"],
                    highlightthickness=1,
                    highlightbackground=T["border"])
canvas_wrap.pack(side=TOP, fill=BOTH, expand=1)

display_canvas = Canvas(canvas_wrap, bg=T["canvas"],
                        highlightthickness=0, bd=0,
                        takefocus=1)
display_canvas.pack(fill=BOTH, expand=1)

# =========================================================
#  ПАНЕЛЬ СЛОЁВ — ПРОКРУЧИВАЕМЫЙ КОНТЕЙНЕР
# =========================================================
layers_outer = Frame(main_area, bg=T["bg"], width=300)
layers_outer.pack(side=RIGHT, fill=Y, padx=(10, 0))
layers_outer.pack_propagate(False)

layers_canvas = Canvas(layers_outer, bg=T["bg"],
                       highlightthickness=0, bd=0)
layers_canvas.pack(side=LEFT, fill=BOTH, expand=1)

layers_scrollbar = Scrollbar(layers_outer, orient=VERTICAL,
                             command=layers_canvas.yview,
                             width=12,
                             bg=T["bg"],
                             troughcolor=T["bg"],
                             bd=0, highlightthickness=0,
                             activebackground=T["hover"])
layers_scrollbar.pack(side=RIGHT, fill=Y)

layers_canvas.configure(yscrollcommand=layers_scrollbar.set)

layers_panel = Frame(layers_canvas, bg=T["bg"])
layers_window_id = layers_canvas.create_window(
    (0, 0), window=layers_panel, anchor="nw")


def _on_layers_canvas_configure(event):
    layers_canvas.itemconfigure(layers_window_id, width=event.width)


layers_canvas.bind("<Configure>", _on_layers_canvas_configure)


def _on_layers_panel_configure(event):
    layers_canvas.configure(scrollregion=layers_canvas.bbox("all"))


layers_panel.bind("<Configure>", _on_layers_panel_configure)


def _on_layers_mousewheel(event):
    delta = 0
    if event.delta:
        delta = -1 * (event.delta // 120)
    layers_canvas.yview_scroll(delta, "units")


def _bind_layers_wheel(widget):
    widget.bind("<MouseWheel>", _on_layers_mousewheel, add="+")
    for child in widget.winfo_children():
        _bind_layers_wheel(child)


layers_canvas.bind("<MouseWheel>", _on_layers_mousewheel, add="+")
layers_panel.bind("<MouseWheel>", _on_layers_mousewheel, add="+")


# =========================================================
#  РАЗМЕР ХОЛСТА
# =========================================================
def on_canvas_resize(event):
    global canvas_width, canvas_height
    new_w = max(1, event.width)
    new_h = max(1, event.height)
    if new_w == canvas_width and new_h == canvas_height:
        return
    canvas_width = new_w
    canvas_height = new_h
    for layer in layers:
        layer.resize(new_w, new_h)
    redraw_canvas()


display_canvas.bind("<Configure>", on_canvas_resize)


# =========================================================
#  СЛОИ
# =========================================================
def get_draw_layer():
    return layers[0] if layers else None


def get_active_layer():
    return layers[0] if layers else None


def ensure_draw_layer():
    global active_layer_index
    layer = get_draw_layer()
    if layer is not None:
        return layer
    layer = Layer(name="Ваш рисунок",
                  width=canvas_width, height=canvas_height)
    layers.append(layer)
    active_layer_index = 0
    redraw_canvas()
    return layer


def _highlight_row(selected_value):
    for value, row in layer_rows.items():
        if value == selected_value:
            row["inner"].configure(bg=T["layer_active"])
            if "outer" in row:
                row["outer"].configure(bg=T["layer_active"])
            row["accent"].configure(bg=T["accent"])
            if "rb" in row:
                row["rb"].configure(bg=T["layer_active"],
                                    activebackground=T["layer_active"])
            for child in row["inner"].winfo_children():
                if isinstance(child, Radiobutton):
                    child.configure(bg=T["layer_active"],
                                    activebackground=T["layer_active"])
        else:
            row["inner"].configure(bg=T["card"])
            if "outer" in row:
                row["outer"].configure(bg=T["card"])
            row["accent"].configure(bg=T["card"])
            if "rb" in row:
                row["rb"].configure(bg=T["card"],
                                    activebackground=T["card"])
            for child in row["inner"].winfo_children():
                if isinstance(child, Radiobutton):
                    child.configure(bg=T["card"],
                                    activebackground=T["card"])


def on_radio_change():
    global opacity_target
    if rb_choice is None:
        return
    opacity_target = rb_choice.get()
    _highlight_row(opacity_target)

    if opacity_var is not None:
        if opacity_target == 0 and layers:
            opacity_var.set(layers[0].opacity)
            if layer_opacity_var is not None:
                layer_opacity_var.set(layers[0].opacity)
        elif opacity_target == 1:
            opacity_var.set(background.image_opacity)
        elif opacity_target == 2:
            opacity_var.set(background.color_opacity)

    if opacity_hint is not None:
        names = {
            0: "Ваш рисунок",
            1: "Изображение фона",
            2: "Цвет фона",
        }
        opacity_hint.configure(
            text=f"(применяется к: {names.get(opacity_target, '—')})")

    _paint_scale_buttons()


def on_vis_change():
    if layers and cb_layer is not None:
        layers[0].visible = cb_layer.get()
    if cb_image is not None:
        background.image_visible = cb_image.get()
    if cb_color is not None:
        background.color_visible = cb_color.get()
    redraw_canvas()


def sync_visibility_vars():
    if cb_layer is not None:
        if layers:
            cb_layer.set(layers[0].visible)
        cb_image.set(background.image_visible)
        cb_color.set(background.color_visible)
    for e in (eye_layer, eye_image, eye_color):
        if e is not None:
            e._redraw()


def on_opacity_change():
    if opacity_var is None:
        return
    v = opacity_var.get()
    if opacity_target == 0:
        layer = get_active_layer()
        if layer is not None:
            layer.opacity = v
            layer._cache_dirty = True
        if layer_opacity_var is not None:
            layer_opacity_var.set(v)
    elif opacity_target == 1:
        background.image_opacity = v
    elif opacity_target == 2:
        background.color_opacity = v
    redraw_canvas()


def on_layer_opacity_change():
    if layer_opacity_var is None:
        return
    layer = get_active_layer()
    if layer is None:
        return
    v = layer_opacity_var.get()
    layer.opacity = v
    layer._cache_dirty = True

    if opacity_target == 0 and opacity_var is not None:
        opacity_var.set(v)

    redraw_canvas()


# =========================================================
#  МАСШТАБ (fit/cover/stretch)
# =========================================================
def set_scale_mode(mode):
    global opacity_target

    if opacity_target == 2:
        mb.showinfo("Масштаб", "К цвету фона масштаб неприменим.")
        return

    if opacity_target == 1:
        if not background.is_image():
            mb.showinfo("Масштаб",
                        "Сначала загрузите фоновое изображение.")
            return
        background.scale_mode = mode
        redraw_canvas()
        _paint_scale_buttons()
        return

    layer = get_active_layer()
    if layer is None:
        return
    layer.scale_mode = mode
    layer._cache_dirty = True
    layer.clamp_to_canvas()
    redraw_canvas()
    _paint_scale_buttons()


def reset_layer_transform():
    layer = get_active_layer()
    if layer is None:
        return
    push_undo()
    layer.reset_transform()
    layer.clamp_to_canvas()
    redraw_canvas()


def _paint_scale_buttons():
    current = None
    if opacity_target == 0:
        layer = get_active_layer()
        if layer is not None:
            current = layer.scale_mode
    elif opacity_target == 1:
        current = background.scale_mode

    for mode, btn in scale_buttons.items():
        if mode == current:
            btn.configure(bg=T["accent"], fg=T["accent_fg"],
                          activebackground=T["accent_hov"],
                          activeforeground=T["accent_fg"])
        else:
            btn.configure(bg=T["card"], fg=T["text"],
                          activebackground=T["hover"],
                          activeforeground=T["text"])


# =========================================================
#  РЕЖИМЫ
# =========================================================
def set_mode_brush():
    global draw_mode
    draw_mode = "brush"
    _update_mode_buttons()
    _paint_palette_selection()
    redraw_canvas()


def set_mode_eraser():
    global draw_mode
    draw_mode = "eraser"
    _update_mode_buttons()
    _paint_palette_selection()
    redraw_canvas()


def _update_mode_buttons():
    def paint(btn, active):
        if btn is None:
            return
        if active:
            btn.configure(bg=T["accent"], fg=T["accent_fg"],
                          activebackground=T["accent_hov"],
                          activeforeground=T["accent_fg"])
        else:
            btn.configure(bg=T["card"], fg=T["text"],
                          activebackground=T["hover"],
                          activeforeground=T["text"])

    paint(brush_btn, draw_mode == "brush")
    paint(eraser_btn, draw_mode == "eraser")


def erase_segment(x0, y0, x1, y1):
    layer = get_draw_layer()
    if layer is None:
        return
    radius = max(1, pen_width // 2)
    layer.erase_at(x0, y0, x1, y1, radius)
    redraw_canvas()


# =========================================================
#  РИСОВАНИЕ И МАСШТАБИРОВАНИЕ
# =========================================================
last_x, last_y = None, None


def _is_alt_pressed(event):
    try:
        state = event.state
    except Exception:
        return False
    return bool(state & (0x0008 | 0x20000))


def start_draw(event):
    global last_x, last_y, transform_handle
    global transform_start_bbox, transform_start_mouse, transform_start_scale
    global drag_active, drag_start_mouse, drag_start_tx_ty

    h = _hit_handle(event.x, event.y)
    if h is not None and layers:
        layer = layers[0]
        push_undo()
        transform_handle = h
        transform_start_bbox = layer.current_bbox()
        transform_start_mouse = (event.x, event.y)
        transform_start_scale = (layer.tsx, layer.tsy)
        last_x, last_y = None, None
        return

    if layers and _is_alt_pressed(event):
        layer = layers[0]
        if layer.contains_canvas_point(event.x, event.y) and layer.visible:
            push_undo()
            drag_active = True
            drag_start_mouse = (event.x, event.y)
            drag_start_tx_ty = (layer.tx, layer.ty)
            last_x, last_y = None, None
            try:
                display_canvas.configure(cursor="fleur")
            except Exception:
                pass
            return

    layer = ensure_draw_layer()
    if layer is None:
        return
    if not layer.visible:
        return
    if not layer.contains_canvas_point(event.x, event.y):
        last_x, last_y = None, None
        return

    push_undo()
    last_x, last_y = event.x, event.y

    if draw_mode == "eraser":
        erase_segment(event.x, event.y, event.x, event.y)
        return

    layer.add_point(event.x, event.y)
    redraw_canvas()


def draw_line_to(event):
    global last_x, last_y

    if transform_handle is not None and layers:
        _apply_transform(event.x, event.y)
        return

    if drag_active and layers:
        _apply_drag(event.x, event.y)
        return

    if last_x is None:
        return

    layer = get_draw_layer()
    if layer is None or not layer.visible:
        return

    clipped = layer.clip_segment_to_bbox(last_x, last_y, event.x, event.y)
    if clipped is None:
        last_x, last_y = event.x, event.y
        return
    cx0, cy0, cx1, cy1 = clipped

    if draw_mode == "eraser":
        erase_segment(cx0, cy0, cx1, cy1)
        last_x, last_y = event.x, event.y
        return

    if not layer.contains_canvas_point(last_x, last_y):
        layer.finish_stroke()
        layer.add_point(cx0, cy0)
    layer.add_point(cx1, cy1)
    last_x, last_y = event.x, event.y
    redraw_canvas()


def stop_draw(event):
    global last_x, last_y, transform_handle
    global transform_start_bbox, transform_start_mouse, transform_start_scale
    global drag_active, drag_start_mouse, drag_start_tx_ty

    if transform_handle is not None:
        layer = get_draw_layer()
        if layer is not None:
            layer.clamp_to_canvas()
        transform_handle = None
        transform_start_bbox = None
        transform_start_mouse = None
        transform_start_scale = None
        redraw_canvas()
        return

    if drag_active:
        drag_active = False
        drag_start_mouse = None
        drag_start_tx_ty = None
        try:
            display_canvas.configure(cursor="crosshair")
        except Exception:
            pass
        redraw_canvas()
        return

    last_x, last_y = None, None
    if draw_mode != "eraser":
        layer = get_draw_layer()
        if layer is not None:
            layer.finish_stroke()


def _apply_transform(mx, my):
    if (transform_handle is None or transform_start_bbox is None
            or transform_start_mouse is None or transform_start_scale is None):
        return
    layer = get_draw_layer()
    if layer is None:
        return

    x0, y0, x1, y1 = transform_start_bbox
    sx0, sy0 = transform_start_mouse
    tsx0, tsy0 = transform_start_scale

    dx = mx - sx0
    dy = my - sy0

    bw = max(1.0, x1 - x0)
    bh = max(1.0, y1 - y0)

    new_tsx, new_tsy = tsx0, tsy0

    if "e" in transform_handle:
        new_tsx = tsx0 * max(0.05, (bw + dx) / bw)
    if "w" in transform_handle:
        new_tsx = tsx0 * max(0.05, (bw - dx) / bw)
    if "s" in transform_handle:
        new_tsy = tsy0 * max(0.05, (bh + dy) / bh)
    if "n" in transform_handle:
        new_tsy = tsy0 * max(0.05, (bh - dy) / bh)

    layer.tsx = new_tsx
    layer.tsy = new_tsy
    layer._cache_dirty = True
    layer.clamp_to_canvas()
    redraw_canvas()


def _apply_drag(mx, my):
    if not drag_active or drag_start_mouse is None or drag_start_tx_ty is None:
        return
    layer = get_draw_layer()
    if layer is None:
        return

    sx, sy = drag_start_mouse
    tx0, ty0 = drag_start_tx_ty
    dx = mx - sx
    dy = my - sy

    x0, y0 = layer.layer_to_canvas(0, 0)
    x1, y1 = layer.layer_to_canvas(layer.width, layer.height)
    bw = max(1e-6, abs(x1 - x0))
    bh = max(1e-6, abs(y1 - y0))
    kx = bw / (layer.width * max(1e-6, layer.tsx))
    ky = bh / (layer.height * max(1e-6, layer.tsy))

    step_x = kx * layer.tsx * layer.width if layer.width else 1.0
    step_y = ky * layer.tsy * layer.height if layer.height else 1.0

    new_tx = tx0 + (dx / step_x if step_x else 0.0)
    new_ty = ty0 + (dy / step_y if step_y else 0.0)

    new_tx = max(-1.0, min(1.0, new_tx))
    new_ty = max(-1.0, min(1.0, new_ty))

    layer.tx = new_tx
    layer.ty = new_ty
    layer._cache_dirty = True
    redraw_canvas()


def on_mouse_move(event):
    global cursor_x, cursor_y
    cursor_x, cursor_y = event.x, event.y

    h = _hit_handle(event.x, event.y)
    if h is not None:
        try:
            display_canvas.configure(cursor=_cursor_for_handle(h))
        except Exception:
            display_canvas.configure(cursor="crosshair")
    else:
        display_canvas.configure(cursor="crosshair")

    if draw_mode == "eraser":
        redraw_canvas()


display_canvas.bind("<Button-1>", start_draw)
display_canvas.bind("<B1-Motion>", draw_line_to)
display_canvas.bind("<ButtonRelease-1>", stop_draw)
display_canvas.bind("<Motion>", on_mouse_move)
display_canvas.bind("<Enter>", lambda e: display_canvas.focus_set(), add="+")


# =========================================================
#  АКТИВНЫЙ ЦВЕТ / ПАЛИТРА
# =========================================================
def select_color(hex_color):
    global color, draw_mode
    color = hex_color
    draw_mode = "brush"
    _update_mode_buttons()
    update_color_indicator()
    _paint_palette_selection()


def update_color_indicator():
    if color_indicator is None:
        return
    color_indicator.delete("all")
    color_indicator.configure(bg=T["bg"])
    color_indicator.create_rectangle(3, 3, 41, 41,
                                     fill=color,
                                     outline=T["sel_border"],
                                     width=3)


def _paint_palette_selection():
    for item in palette_frames:
        c = item["canvas"]
        if draw_mode == "brush" and item["hex"] == color:
            c.itemconfigure("sel", outline=T["sel_border"])
        else:
            c.itemconfigure("sel", outline="")

    if eraser_palette_btn is not None:
        if draw_mode == "eraser":
            eraser_palette_btn.configure(
                bg=T["accent"], fg=T["accent_fg"],
                activebackground=T["accent_hov"],
                activeforeground=T["accent_fg"])
        else:
            eraser_palette_btn.configure(
                bg=T["card"], fg=T["text"],
                activebackground=T["hover"],
                activeforeground=T["text"])


# =========================================================
#  ФОН
# =========================================================
def choose_bg_color():
    color_choice = colorchooser.askcolor(title="Цвет фона")
    if color_choice and color_choice[1]:
        background.color = color_choice[1]
        background.color_visible = True
        background.color_opacity = 1.0
        sync_visibility_vars()
        redraw_canvas()


def choose_bg_image():
    file = fd.askopenfilename(
        title="Выберите фоновое изображение",
        filetypes=(("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.webp;*.gif;*.exr"),
                   ("All files", "*.*")))
    if not file:
        return
    try:
        img = load_image_any(file)
        background.source_image = img
        background.scale_mode = "fit"
        background.filename = file.replace("\\", "/").split("/")[-1]
        background.image_visible = True
        background.image_opacity = 1.0
        sync_visibility_vars()
        redraw_canvas()
    except Exception as e:
        mb.showerror("Ошибка", f"Не удалось открыть изображение:\n{e}")


def reset_bg():
    background.color = "#FFFFFF"
    background.clear_image()
    background.scale_mode = "fit"
    background.filename = None
    background.color_visible = True
    background.image_visible = True
    background.color_opacity = 1.0
    background.image_opacity = 1.0
    sync_visibility_vars()
    redraw_canvas()


# =========================================================
#  НОВЫЙ / ОТКРЫТЬ / СОХРАНЕНИЕ
# =========================================================
def new_file():
    global active_layer_index, pen_width, color, opacity_target, draw_mode
    layer = get_draw_layer()
    has_content = layer is not None and (
            len(layer.shapes) > 0 or
            layer.erase_mask.getbbox() is not None
    )
    if has_content:
        if not mb.askyesno("Новый файл",
                           "Все несохранённые изменения будут потеряны.\n"
                           "Создать новый файл?"):
            return

    layers.clear()
    Layer._counter = 0
    pen_width = 5
    color = "#E53935"
    if width_var is not None:
        width_var.set(str(pen_width))

    background.color = "#FFFFFF"
    background.clear_image()
    background.scale_mode = "fit"
    background.filename = None
    background.color_visible = True
    background.image_visible = True
    background.color_opacity = 1.0
    background.image_opacity = 1.0

    layers.append(Layer(name="Ваш рисунок",
                        width=canvas_width, height=canvas_height))
    active_layer_index = 0
    opacity_target = 0
    draw_mode = "brush"
    _update_mode_buttons()

    if rb_choice is not None:
        rb_choice.set(0)
    if opacity_var is not None:
        opacity_var.set(1.0)
    if layer_opacity_var is not None:
        layer_opacity_var.set(1.0)
    select_color("#E53935")
    sync_visibility_vars()
    _highlight_row(0)
    _clear_history()
    redraw_canvas()


def open_file():
    """Открыть изображение как фон нового документа."""
    global active_layer_index, opacity_target, draw_mode

    layer = get_draw_layer()
    has_content = layer is not None and (
            len(layer.shapes) > 0 or
            layer.erase_mask.getbbox() is not None
    )
    if has_content:
        if not mb.askyesno("Открыть файл",
                           "Все несохранённые изменения будут потеряны.\n"
                           "Открыть другой файл?"):
            return

    file = fd.askopenfilename(
        title="Открыть изображение",
        filetypes=(
            ("Все изображения", "*.png;*.jpg;*.jpeg;*.bmp;*.webp;*.exr"),
            ("PNG image", "*.png"),
            ("JPEG image", "*.jpg;*.jpeg"),
            ("BMP image", "*.bmp"),
            ("WebP image", "*.webp"),
            ("OpenEXR", "*.exr"),
            ("All files", "*.*")))
    if not file:
        return

    try:
        img = load_image_any(file)
    except Exception as e:
        mb.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")
        return

    background.color = "#FFFFFF"
    background.source_image = img
    background.scale_mode = "fit"
    background.filename = file.replace("\\", "/").split("/")[-1]
    background.color_visible = True
    background.image_visible = True
    background.color_opacity = 1.0
    background.image_opacity = 1.0

    layers.clear()
    Layer._counter = 0
    layers.append(Layer(name="Ваш рисунок",
                        width=canvas_width, height=canvas_height))
    active_layer_index = 0
    opacity_target = 0
    draw_mode = "brush"
    _update_mode_buttons()

    if rb_choice is not None:
        rb_choice.set(0)
    if opacity_var is not None:
        opacity_var.set(1.0)
    if layer_opacity_var is not None:
        layer_opacity_var.set(1.0)

    select_color("#E53935")
    sync_visibility_vars()
    _highlight_row(0)
    _clear_history()
    redraw_canvas()


def save_file():
    global autosave_last_path
    file = fd.asksaveasfilename(
        defaultextension=".png",
        filetypes=(
            ("PNG image", "*.png"), ("JPEG image", "*.jpg;*.jpeg"),
            ("BMP image", "*.bmp"), ("WebP image", "*.webp"),
            ("OpenEXR", "*.exr"), ("All files", "*.*")))
    if not file:
        return False
    lower = file.lower()
    try:
        composed = compose()
        if lower.endswith(".exr"):
            if not EXR_OK:
                mb.showerror("Ошибка", "Установите openexr-numpy")
                return False
            arr = np.array(composed.convert("RGBA")).astype(np.float32) / 255.0
            imwrite(file, arr)
        elif lower.endswith((".jpg", ".jpeg")):
            composed.convert("RGB").save(file, "JPEG", quality=95)
        elif lower.endswith(".bmp"):
            composed.convert("RGB").save(file, "BMP")
        elif lower.endswith(".webp"):
            composed.convert("RGB").save(file, "WEBP", quality=95)
        else:
            composed.save(file, "PNG")
        autosave_last_path = file
        mb.showinfo("Готово", f"Файл сохранён:\n{file}")
        return True
    except Exception as e:
        mb.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
        return False


# =========================================================
#  АВТОСОХРАНЕНИЕ
# =========================================================
def _cancel_autosave_timer():
    global autosave_after_id
    if autosave_after_id is not None:
        try:
            root.after_cancel(autosave_after_id)
        except Exception:
            pass
        autosave_after_id = None


def _schedule_autosave():
    global autosave_after_id
    _cancel_autosave_timer()
    if not autosave_enabled:
        return
    delay_ms = autosave_interval_min * 60 * 1000
    autosave_after_id = root.after(delay_ms, _run_autosave)


def _run_autosave():
    global autosave_last_path

    try:
        composed = compose()
    except Exception:
        _schedule_autosave()
        return

    import os
    import time

    target = autosave_last_path
    try:
        if target is None:
            home = os.path.expanduser("~")
            fname = time.strftime("autosave_%Y%m%d_%H%M%S.png")
            target = os.path.join(home, fname)
        else:
            root_path, ext = os.path.splitext(target)
            target = f"{root_path}.autosave{ext}"

        lower = target.lower()
        if lower.endswith(".exr"):
            if EXR_OK:
                arr = np.array(composed.convert("RGBA")).astype(np.float32) / 255.0
                imwrite(target, arr)
        elif lower.endswith((".jpg", ".jpeg")):
            composed.convert("RGB").save(target, "JPEG", quality=95)
        elif lower.endswith(".bmp"):
            composed.convert("RGB").save(target, "BMP")
        elif lower.endswith(".webp"):
            composed.convert("RGB").save(target, "WEBP", quality=95)
        else:
            composed.save(target, "PNG")
    except Exception:
        pass

    _schedule_autosave()


def set_autosave(choice_label):
    global autosave_enabled, autosave_interval_min
    value = AUTOSAVE_CHOICES.get(choice_label, 0)
    if value <= 0:
        autosave_enabled = False
        autosave_interval_min = 5
        _cancel_autosave_timer()
    else:
        autosave_enabled = True
        autosave_interval_min = value
        _schedule_autosave()


def _confirm_save_before_exit():
    layer = get_draw_layer()
    has_content = layer is not None and (
            len(layer.shapes) > 0 or
            layer.erase_mask.getbbox() is not None
    )
    if not has_content:
        return True

    answer = mb.askyesnocancel(
        "Сохранить и выйти",
        "Сохранить текущий рисунок перед выходом?"
    )
    if answer is None:
        return False
    if answer is False:
        return True
    return save_file()


def save_and_exit():
    _cancel_autosave_timer()
    if not _confirm_save_before_exit():
        return
    root.destroy()


def _on_window_close():
    _cancel_autosave_timer()
    if _confirm_save_before_exit():
        root.destroy()


def clear_canvas():
    layer = get_draw_layer()
    if layer is not None:
        push_undo()
        layer.clear()
        redraw_canvas()


# =========================================================
#  СТАТУС-БАР
# =========================================================
status = Frame(root, bg=T["toolbar"], height=26)
status.pack(fill=X)
status.pack_propagate(False)

status_label = Label(status,
                     text="Alt + перетаскивание — двигать рамку",
                     font=FONT_SMALL, bg=T["toolbar"], fg=T["muted"])
status_label.pack(side=LEFT, padx=10)


# =========================================================
#  ГЛАЗ
# =========================================================
def make_eye(parent, var, command, size=22, tooltip=None):
    c = Canvas(parent, width=size, height=size,
               bg=T["card"], highlightthickness=0, bd=0,
               cursor="hand2")

    def redraw():
        c.delete("all")
        w = size
        h = size
        cx, cy = w / 2, h / 2

        if var.get():
            c.create_oval(cx - w * 0.45, cy - h * 0.25,
                          cx + w * 0.45, cy + h * 0.25,
                          outline=T["text"], width=2)
            c.create_oval(cx - w * 0.14, cy - h * 0.14,
                          cx + w * 0.14, cy + h * 0.14,
                          fill=T["text"], outline="")
        else:
            c.create_line(cx - w * 0.45, cy, cx + w * 0.45, cy,
                          fill=T["text"], width=2, capstyle=ROUND)
            c.create_line(cx - w * 0.30, cy - 2, cx - w * 0.30, cy + 4,
                          fill=T["text"], width=2, capstyle=ROUND)
            c.create_line(cx, cy - 3, cx, cy + 5,
                          fill=T["text"], width=2, capstyle=ROUND)
            c.create_line(cx + w * 0.30, cy - 2, cx + w * 0.30, cy + 4,
                          fill=T["text"], width=2, capstyle=ROUND)

    def click(e=None):
        var.set(not var.get())
        redraw()
        command()

    c.bind("<Button-1>", click)
    c._redraw = redraw
    redraw()

    if tooltip:
        ToolTip(c, tooltip)

    return c


# =========================================================
#  ВАЛИДАЦИЯ ТОЛЩИНЫ
# =========================================================
def validate_int(new_value):
    if new_value == "":
        return True
    if not new_value.isdigit():
        return False
    if int(new_value) <= 0:
        return False
    return True


vcmd = (root.register(validate_int), "%P")

# =========================================================
#  ВАЛИДАЦИЯ И УСТАНОВКА ТОЛЩИНЫ ПЕРА (Задание 4)
# =========================================================
def apply_pen_width():
    """Считывает значение из Entry, обрабатывает ошибки и обновляет pen_width."""
    global pen_width
    try:
        # Пытаемся получить целое число из поля ввода
        new_width = int(width_var.get().strip())

        # Проверяем, чтобы число было положительным
        if new_width <= 0:
            raise ValueError("Толщина должна быть больше нуля.")

        pen_width = new_width

        # Синхронизируем ползунок (если он есть), чтобы он показывал новое значение
        if width_scale is not None:
            width_scale.set(pen_width)

    except ValueError:
        # Обработка случая, если введено не целое число или пустая строка
        mb.showerror("Ошибка ввода", "Пожалуйста, введите целое положительное число для толщины пера.")
        # Возвращаем в поле текущее корректное значение
        width_var.set(str(pen_width))
    except Exception as e:
        mb.showerror("Ошибка", f"Не удалось установить толщину: {e}")
        width_var.set(str(pen_width))


def _build_width_widget(parent):
    global width_var, width_entry

    # Создаем переменную, но БЕЗ автоматического обновления через trace_add
    width_var = StringVar(value=str(pen_width))

    # Поле ввода
    width_entry = Entry(parent, width=5, font=FONT_BTN,
                        bd=1, relief=FLAT,
                        bg=T["card"], fg=T["text"],
                        insertbackground=T["text"],
                        highlightthickness=1,
                        highlightbackground=T["border"],
                        highlightcolor=T["accent"],
                        textvariable=width_var)
    width_entry.pack(side=LEFT, padx=(0, 5))

    # Привязываем нажатие Enter к кнопке
    width_entry.bind("<Return>", lambda e: apply_pen_width())

    # Кнопка установки толщины
    btn_apply = Button(parent, text="OK", font=FONT_SMALL,
                       bd=0, relief=FLAT,
                       bg=T["accent"], fg=T["accent_fg"],
                       activebackground=T["accent_hov"],
                       activeforeground=T["accent_fg"],
                       padx=8, pady=2, cursor="hand2",
                       highlightthickness=0,
                       command=apply_pen_width)
    btn_apply.pack(side=LEFT)


# =========================================================
#  ПАНЕЛЬ СЛОЁВ — КАРТОЧКИ
# =========================================================
def make_card(parent, title):
    card = Frame(parent, bg=T["card"],
                 highlightthickness=1,
                 highlightbackground=T["border"],
                 bd=0)
    card.pack(fill=X, padx=6, pady=(6, 0))

    if title:
        lbl = Label(card, text=title, font=(FONT, 9, "bold"),
                    bg=T["card"], fg=T["muted"], anchor="w")
        lbl._role = "caption"
        lbl.pack(side=TOP, anchor="w", padx=8, pady=(6, 2))

    inner = Frame(card, bg=T["card"])
    inner.pack(fill=BOTH, expand=1, padx=6, pady=(0, 6))
    return inner


def build_layers_panel():
    global rb_choice, cb_layer, cb_image, cb_color
    global eye_layer, eye_image, eye_color
    global palette_frames, palette_buttons, width_scale
    global layer_opacity_var, layer_opacity_scale
    global opacity_var, opacity_scale, opacity_hint
    global eraser_palette_btn

    palette_frames.clear()
    palette_buttons.clear()

    lbl = Label(layers_panel, text="Слои и параметры",
                font=(FONT, 11, "bold"),
                bg=T["bg"], fg=T["text"])
    lbl._role = "caption"
    lbl.pack(anchor="w", pady=(6, 4), padx=8)

    rb_choice = IntVar(value=0)
    cb_layer = BooleanVar(value=True)
    cb_image = BooleanVar(value=True)
    cb_color = BooleanVar(value=True)

    # ================ Карточка 1. Слои ================
    card_layers = make_card(layers_panel, "Слои")

    def make_row(parent, text, value, cb_var, row_idx,
                 on_row_click=None,
                 action_tooltip=None):
        outer = Frame(parent, bg=T["card"], cursor="hand2")
        outer.pack(fill=X, padx=2, pady=1)

        accent = Frame(outer, bg=T["card"], width=3)
        accent.pack(side=LEFT, fill=Y)

        inner = Frame(outer, bg=T["card"], cursor="hand2")
        inner.pack(side=LEFT, fill=X, expand=1, padx=4, pady=4)

        rb = Radiobutton(inner, text=text, value=value,
                         variable=rb_choice,
                         font=FONT_BTN, bg=T["card"], fg=T["text"],
                         activebackground=T["card"],
                         activeforeground=T["text"],
                         selectcolor=T["card"],
                         bd=0, highlightthickness=0, anchor="w",
                         cursor="hand2",
                         command=on_radio_change)
        rb.pack(side=LEFT)

        eye = make_eye(inner, cb_var, on_vis_change, size=22,
                       tooltip="Показать / скрыть")
        eye.pack(side=RIGHT)

        if row_idx == 1:
            globals()['eye_image'] = eye
        elif row_idx == 2:
            globals()['eye_color'] = eye

        layer_rows[value] = {"inner": inner, "accent": accent,
                             "outer": outer, "rb": rb}

        def _row_click(event=None):
            rb_choice.set(value)
            on_radio_change()
            if on_row_click is not None:
                on_row_click()

        def _row_enter(e):
            if rb_choice.get() != value:
                outer.configure(bg=T["hover"])
                inner.configure(bg=T["hover"])
                rb.configure(bg=T["hover"],
                             activebackground=T["hover"])

        def _row_leave(e):
            if rb_choice.get() != value:
                outer.configure(bg=T["card"])
                inner.configure(bg=T["card"])
                rb.configure(bg=T["card"],
                             activebackground=T["card"])

        for w in (outer, inner, rb):
            w.bind("<Button-1>", _row_click, add="+")
            w.bind("<Enter>", _row_enter, add="+")
            w.bind("<Leave>", _row_leave, add="+")

        if action_tooltip:
            ToolTip(inner, action_tooltip)
            ToolTip(rb, action_tooltip)
            ToolTip(outer, action_tooltip)

    def build_scale_row():
        wrap = Frame(card_layers, bg=T["card"])
        wrap.pack(fill=X, padx=10, pady=(0, 4))

        lbl_ms = Label(wrap, text="Масштаб изображения фона:",
                       font=FONT_SMALL, bg=T["card"], fg=T["muted"])
        lbl_ms._role = "caption"
        lbl_ms.pack(anchor="w")

        row = Frame(wrap, bg=T["card"])
        row.pack(fill=X, pady=(2, 0))

        SCALE_ICONS = {
            "fit": "\uE9A6",
            "cover": "\uE744",
            "stretch": "\uE740",
        }
        SCALE_TIPS = {
            "fit": "Вписать целиком",
            "cover": "Заполнить, обрезая края",
            "stretch": "Растянуть по холсту",
        }

        def make_small(mode):
            b = Button(row, text=SCALE_ICONS.get(mode, "?"),
                       font=ICON_FONT,
                       bd=0, relief=FLAT,
                       bg=T["card"], fg=T["text"],
                       activebackground=T["hover"],
                       activeforeground=T["text"],
                       padx=6, pady=2, cursor="hand2",
                       highlightthickness=0,
                       command=lambda m=mode: set_scale_mode(m))
            b.pack(side=LEFT, padx=2)
            scale_buttons[mode] = b
            ToolTip(b, SCALE_TIPS[mode])

            def on_release(e):
                root.after(10, _paint_scale_buttons)

            b.bind("<ButtonRelease-1>", on_release)

        make_small("fit")
        make_small("cover")
        make_small("stretch")

        btn_reset = Button(wrap, text="Сбросить масштабирование",
                           font=FONT_SMALL, bd=0, relief=FLAT,
                           padx=8, pady=3, cursor="hand2",
                           highlightthickness=0,
                           command=reset_layer_transform)
        btn_reset.pack(fill=X, pady=(4, 0))
        ToolTip(btn_reset, "Вернуть слой к исходному размеру (за квадратики)")

        def _refresh_reset():
            btn_reset.configure(bg=T["card"], fg=T["text"],
                                activebackground=T["hover"],
                                activeforeground=T["text"])

        def on_enter_r(e):
            btn_reset.config(bg=T["hover"])

        def on_leave_r(e):
            _refresh_reset()

        def on_release_r(e):
            _refresh_reset()
            root.after(20, _refresh_reset)

        btn_reset.bind("<Enter>", on_enter_r)
        btn_reset.bind("<Leave>", on_leave_r)
        btn_reset.bind("<ButtonRelease-1>", on_release_r)
        _refresh_reset()

    make_row(card_layers, "Изображение фона", 1, cb_image, 1,
             on_row_click=lambda: choose_bg_image(),
             action_tooltip="Клик — открыть фоновое изображение")

    build_scale_row()

    make_row(card_layers, "Цвет фона", 2, cb_color, 2,
             on_row_click=lambda: choose_bg_color(),
             action_tooltip="Клик — выбрать цвет фона")

    # ================ Карточка 2. Параметры кисти ================
    card_brush = make_card(layers_panel, "Параметры кисти")

    outer = Frame(card_brush, bg=T["card"])
    outer.pack(fill=X, padx=2, pady=1)

    accent = Frame(outer, bg=T["card"], width=3)
    accent.pack(side=LEFT, fill=Y)

    inner = Frame(outer, bg=T["card"])
    inner.pack(side=LEFT, fill=X, expand=1, padx=4, pady=3)

    rb_layer = Radiobutton(inner, text="Ваш рисунок", value=0,
                           variable=rb_choice,
                           font=FONT_BTN, bg=T["card"], fg=T["text"],
                           activebackground=T["card"],
                           activeforeground=T["text"],
                           selectcolor=T["card"],
                           bd=0, highlightthickness=0, anchor="w",
                           command=on_radio_change)
    rb_layer.pack(side=LEFT)

    eye_layer_w = make_eye(inner, cb_layer, on_vis_change, size=22,
                           tooltip="Показать / скрыть слой рисунка")
    eye_layer_w.pack(side=RIGHT)

    globals()['eye_layer'] = eye_layer_w
    layer_rows[0] = {"inner": inner, "accent": accent,
                     "outer": outer, "rb": rb_layer}

    lbl_c = Label(card_brush, text="Цвет:", font=FONT_SMALL,
                  bg=T["card"], fg=T["muted"])
    lbl_c._role = "caption"
    lbl_c.pack(anchor="w", padx=4)

    row_colors = Frame(card_brush, bg=T["card"])
    row_colors.pack(anchor="w", pady=(2, 6), padx=4)

    COLORS = [("#E53935", "Красный"), ("#43A047", "Зелёный"),
              ("#1E88E5", "Синий"), ("#1F1F1F", "Чёрный"),
              ("#FB8C00", "Оранжевый"), ("#8E24AA", "Фиолетовый")]

    for hex_color, name in COLORS:
        swatch = Canvas(row_colors, width=22, height=22,
                        bg=T["card"], highlightthickness=0, bd=0,
                        cursor="hand2")
        swatch.pack(side=LEFT, padx=2)
        swatch.create_rectangle(2, 2, 20, 20,
                                fill=hex_color, outline="",
                                tags="rect")
        swatch.create_rectangle(0, 0, 22, 22,
                                fill="", outline="",
                                width=2, tags="sel")
        swatch.bind("<Button-1>",
                    lambda e, h=hex_color: select_color(h))
        ToolTip(swatch, name)
        palette_frames.append({"hex": hex_color, "canvas": swatch})
        palette_buttons.append(swatch)

    sep = Frame(row_colors, bg=T["border"], width=1)
    sep.pack(side=LEFT, fill=Y, padx=6, pady=2)

    eraser_palette_btn = Button(
        row_colors, text="\uE75C",
        font=ICON_FONT,
        bd=0, relief=FLAT,
        bg=T["card"], fg=T["text"],
        activebackground=T["hover"],
        activeforeground=T["text"],
        width=2, height=1,
        cursor="hand2", highlightthickness=0,
        command=set_mode_eraser)
    eraser_palette_btn.pack(side=LEFT, padx=2)
    ToolTip(eraser_palette_btn, "Ластик (E)")

    lbl_t = Label(card_brush, text="Толщина:", font=FONT_SMALL,
                  bg=T["card"], fg=T["muted"])
    lbl_t._role = "caption"
    lbl_t.pack(anchor="w", padx=4, pady=(4, 0))

    row_width = Frame(card_brush, bg=T["card"])
    row_width.pack(anchor="w", padx=4, pady=(2, 0))
    _build_width_widget(row_width)

    width_scale = Scale(
        card_brush, from_=1, to=100, resolution=1,
        orient=HORIZONTAL,
        variable=width_var,
        showvalue=False, length=200,
        bg=T["card"], fg=T["text"], troughcolor=T["hover"],
        highlightthickness=0, bd=0,
    )
    width_scale.pack(anchor="w", padx=4, pady=(4, 6))
    ToolTip(width_scale, "Толщина кисти и ластика")

    lbl_lo = Label(card_brush, text="Прозрачность слоя рисунка:",
                   font=FONT_SMALL, bg=T["card"], fg=T["muted"])
    lbl_lo._role = "caption"
    lbl_lo.pack(anchor="w", padx=4, pady=(2, 0))

    layer_opacity_var = DoubleVar(value=1.0)
    layer_opacity_scale = Scale(
        card_brush, from_=0.0, to=1.0, resolution=0.05,
        orient=HORIZONTAL, variable=layer_opacity_var,
        showvalue=True, length=200,
        bg=T["card"], fg=T["text"], troughcolor=T["hover"],
        highlightthickness=0, bd=0,
        command=lambda v: on_layer_opacity_change())
    layer_opacity_scale.pack(anchor="w", padx=4, pady=(2, 6))
    ToolTip(layer_opacity_scale, "Прозрачность нарисованного слоя")

    lbl_op = Label(card_layers, text="Прозрачность выбранного:",
                   font=FONT_SMALL, bg=T["card"], fg=T["muted"])
    lbl_op._role = "caption"
    lbl_op.pack(anchor="w", padx=10, pady=(6, 0))

    opacity_var = DoubleVar(value=1.0)
    opacity_scale = Scale(
        card_layers, from_=0.0, to=1.0, resolution=0.05,
        orient=HORIZONTAL, variable=opacity_var,
        showvalue=True, length=200,
        bg=T["card"], fg=T["text"], troughcolor=T["hover"],
        highlightthickness=0, bd=0,
        command=lambda v: on_opacity_change())
    opacity_scale.pack(anchor="w", padx=10, pady=(2, 0))
    ToolTip(opacity_scale, "Прозрачность выбранного пункта")

    opacity_hint = Label(card_layers, text="",
                         font=FONT_SMALL, bg=T["card"], fg=T["muted"])
    opacity_hint.pack(anchor="w", padx=10, pady=(0, 6))

    _highlight_row(0)


# =========================================================
#  ПОСТРОЕНИЕ RIBBON
# =========================================================
def build_ribbon():
    global brush_btn, eraser_btn, autosave_var, autosave_menu

    ICON_NEW = "\uE7C3"
    ICON_OPEN = "\uE8E5"
    ICON_SAVE = "\uE74E"
    ICON_EXIT = "\uE8BB"
    ICON_COLOR = "\uE790"
    ICON_IMAGE = "\uEB9F"
    ICON_DEL = "\uE74D"
    ICON_BRUSH = "\uE790"
    ICON_ERASE = "\uE75C"
    ICON_UNDO = "\uE7A7"
    ICON_REDO = "\uE7A6"
    ICON_TIMER = "\uE823"

    g = make_group(ribbon_content, "Документ")
    ribbon_button(g, ICON_NEW, "Новый", lambda: new_file(),
                  tooltip="Создать новый файл (Ctrl+N)")
    ribbon_button(g, ICON_OPEN, "Открыть", lambda: open_file(),
                  tooltip="Открыть изображение (Ctrl+O)")
    ribbon_button(g, ICON_SAVE, "Сохранить", lambda: save_file(),
                  primary=True, tooltip="Сохранить файл (Ctrl+S)")
    ribbon_button(g, ICON_EXIT, "Сохранить и выйти",
                  lambda: save_and_exit(),
                  tooltip="Сохранить и закрыть редактор (Ctrl+Shift+S)")

    autosave_var = StringVar(value="Выкл")

    wrap_as = Frame(g, bg=T["card"])
    wrap_as.pack(side=LEFT, padx=4, pady=4)

    btn_as = Button(wrap_as, text=ICON_TIMER,
                    font=ICON_FONT,
                    bd=0, relief=FLAT,
                    width=3, height=1, cursor="hand2",
                    highlightthickness=0,
                    bg=T["card"], fg=T["text"],
                    activebackground=T["hover"],
                    activeforeground=T["text"])
    btn_as.pack()

    lbl_as = Label(wrap_as, text="Автосохр.", font=(FONT, 8),
                   bg=T["card"], fg=T["muted"])
    lbl_as._role = "caption"
    lbl_as.pack(pady=(2, 0))

    autosave_menu = Menu(btn_as, tearoff=0,
                         bg=T["card"], fg=T["text"],
                         activebackground=T["hover"],
                         activeforeground=T["text"],
                         bd=0)

    for label in AUTOSAVE_CHOICES.keys():
        autosave_menu.add_radiobutton(
            label=label,
            variable=autosave_var,
            value=label,
            command=lambda l=label: set_autosave(l),
        )

    def _show_as_menu(e=None):
        try:
            autosave_menu.tk_popup(
                btn_as.winfo_rootx(),
                btn_as.winfo_rooty() + btn_as.winfo_height())
        finally:
            autosave_menu.grab_release()

    btn_as.bind("<Button-1>", _show_as_menu)
    ToolTip(btn_as, "Автосохранение: выберите интервал")
    ToolTip(lbl_as, "Автосохранение: выберите интервал")

    def _as_enter(e):
        btn_as.configure(bg=T["hover"])

    def _as_leave(e):
        btn_as.configure(bg=T["card"], fg=T["text"],
                         activebackground=T["hover"],
                         activeforeground=T["text"])

    btn_as.bind("<Enter>", _as_enter, add="+")
    btn_as.bind("<Leave>", _as_leave, add="+")

    g_edit = make_group(ribbon_content, "Правка")
    ribbon_button(g_edit, ICON_UNDO, "Отменить", lambda: undo(),
                  tooltip="Отменить последнее действие (Ctrl+Z)")
    ribbon_button(g_edit, ICON_REDO, "Вернуть", lambda: redo(),
                  tooltip="Вернуть отменённое действие (Ctrl+Y)")

    g_bg = make_group(ribbon_content, "Фон")
    ribbon_button(g_bg, ICON_COLOR, "Фон", lambda: choose_bg_color(),
                  tooltip="Выбрать цвет фона")
    ribbon_button(g_bg, ICON_IMAGE, "Изображение", lambda: choose_bg_image(),
                  tooltip="Загрузить фоновое изображение")
    ribbon_button(g_bg, ICON_DEL, "Удалить фон", lambda: reset_bg(),
                  tooltip="Сбросить фон к белому цвету")

    g_mode = make_group(ribbon_content, "Инструмент")
    brush_btn = ribbon_button(g_mode, ICON_BRUSH, "Кисть",
                              lambda: set_mode_brush(), primary=True,
                              tooltip="Кисть (B)")
    eraser_btn = ribbon_button(g_mode, ICON_ERASE, "Ластик",
                               lambda: set_mode_eraser(),
                               tooltip="Ластик (E)")


# =========================================================
#  ПЕРЕКРАСКА
# =========================================================
def _repaint_ribbon(widget):
    try:
        cls = widget.winfo_class()

        if cls == "Frame":
            if widget is ribbon or widget is ribbon_content or widget is ribbon_right:
                widget.configure(bg=T["bg"])
            else:
                widget.configure(bg=T["card"])
                try:
                    if widget.cget("highlightthickness"):
                        widget.configure(highlightbackground=T["border"])
                except Exception:
                    pass

        elif cls == "Canvas":
            widget.configure(bg=T["card"])

        elif cls == "Label":
            if getattr(widget, "_role", None) == "caption":
                widget.configure(bg=T["card"], fg=T["muted"])
            else:
                widget.configure(bg=T["card"], fg=T["text"])

        elif cls == "Button":
            if getattr(widget, "_is_palette", False):
                pass
            elif getattr(widget, "_primary", False):
                widget.configure(
                    bg=T["accent"], fg=T["accent_fg"],
                    activebackground=T["accent_hov"],
                    activeforeground=T["accent_fg"])
            else:
                widget.configure(
                    bg=T["card"], fg=T["text"],
                    activebackground=T["hover"],
                    activeforeground=T["text"])

        elif cls == "Entry":
            widget.configure(
                bg=T["card"], fg=T["text"],
                insertbackground=T["text"],
                highlightbackground=T["border"],
                highlightcolor=T["accent"])
    except Exception:
        pass

    for child in widget.winfo_children():
        _repaint_ribbon(child)


def _repaint_layers_panel(widget, inside_card=False):
    try:
        cls = widget.winfo_class()

        if cls == "Frame":
            try:
                is_card = widget.cget("highlightthickness") == 1
            except Exception:
                is_card = False

            if is_card or inside_card:
                widget.configure(bg=T["card"])
                if is_card:
                    widget.configure(highlightbackground=T["border"])
            else:
                widget.configure(bg=T["bg"])

            for child in widget.winfo_children():
                _repaint_layers_panel(child, inside_card=is_card or inside_card)

        elif cls in ("Radiobutton", "Checkbutton"):
            bg = T["card"] if inside_card else T["bg"]
            widget.configure(bg=bg, fg=T["text"],
                             activebackground=bg,
                             activeforeground=T["text"],
                             selectcolor=T["card"])

        elif cls == "Label":
            bg = T["card"] if inside_card else T["bg"]
            fg = T["muted"] if getattr(widget, "_role", None) == "caption" else T["text"]
            widget.configure(bg=bg, fg=fg)

        elif cls == "Button":
            widget.configure(bg=T["card"], fg=T["text"],
                             activebackground=T["hover"],
                             activeforeground=T["text"])

        elif cls == "Canvas":
            bg = T["card"] if inside_card else T["bg"]
            widget.configure(bg=bg)

        elif cls == "Entry":
            widget.configure(bg=T["card"], fg=T["text"],
                             insertbackground=T["text"],
                             highlightbackground=T["border"],
                             highlightcolor=T["accent"])

        elif cls == "Scale":
            widget.configure(bg=T["card"], fg=T["text"],
                             troughcolor=T["hover"])
    except Exception:
        pass


# =========================================================
#  ПРИМЕНЕНИЕ ТЕМЫ
# =========================================================
def _apply_theme_colors():
    root.configure(bg=T["bg"])
    ribbon.configure(bg=T["bg"])
    ribbon_content.configure(bg=T["bg"])
    ribbon_right.configure(bg=T["bg"])
    main_area.configure(bg=T["bg"])
    canvas_column.configure(bg=T["bg"])
    canvas_wrap.configure(bg=T["bg"])
    display_canvas.configure(bg=T["canvas"])
    layers_outer.configure(bg=T["bg"])
    layers_canvas.configure(bg=T["bg"])
    try:
        layers_scrollbar.configure(bg=T["bg"], troughcolor=T["bg"],
                                   activebackground=T["hover"])
    except Exception:
        pass
    layers_panel.configure(bg=T["bg"])
    status.configure(bg=T["toolbar"])
    status_label.configure(bg=T["toolbar"], fg=T["muted"])

    _repaint_ribbon(ribbon)
    _repaint_layers_panel(layers_panel)

    for e in (eye_layer, eye_image, eye_color):
        if e is not None:
            e.configure(bg=T["card"])
            e._redraw()

    _highlight_row(opacity_target)

    if opacity_hint is not None:
        opacity_hint.configure(bg=T["card"], fg=T["muted"])
    if opacity_scale is not None:
        opacity_scale.configure(bg=T["card"], fg=T["text"],
                                troughcolor=T["hover"])
    if width_scale is not None:
        width_scale.configure(bg=T["card"], fg=T["text"],
                              troughcolor=T["hover"])
    if layer_opacity_scale is not None:
        layer_opacity_scale.configure(bg=T["card"], fg=T["text"],
                                      troughcolor=T["hover"])

    for item in palette_frames:
        item["canvas"].configure(bg=T["card"])

    if width_entry is not None:
        width_entry.configure(
            bg=T["card"], fg=T["text"],
            insertbackground=T["text"],
            highlightbackground=T["border"],
            highlightcolor=T["accent"])

    if color_indicator is not None:
        color_indicator.configure(bg=T["bg"])
        update_color_indicator()

    if autosave_menu is not None:
        try:
            autosave_menu.configure(bg=T["card"], fg=T["text"],
                                    activebackground=T["hover"],
                                    activeforeground=T["text"])
        except Exception:
            pass

    _paint_scale_buttons()
    _update_mode_buttons()
    _paint_palette_selection()

    if btn_theme is not None:
        btn_theme.configure(bg=T["card"], fg=T["text"],
                            activebackground=T["hover"],
                            activeforeground=T["text"])

    redraw_canvas()
    root.update_idletasks()


def toggle_theme():
    global T, theme_name
    theme_name = "dark" if theme_name == "light" else "light"
    T = dict(THEME[theme_name])
    _apply_theme_colors()


def apply_system_theme():
    global T, theme_name
    theme_name = "dark" if is_windows_dark_theme() else "light"
    T = dict(THEME[theme_name])
    _apply_theme_colors()


# =========================================================
#  ГОРЯЧИЕ КЛАВИШИ
# =========================================================
def _bind_hotkeys():
    root.bind_all("<Control-s>", lambda e: save_file())
    root.bind_all("<Control-S>", lambda e: save_file())
    root.bind_all("<Control-n>", lambda e: new_file())
    root.bind_all("<Control-N>", lambda e: new_file())
    root.bind_all("<Control-o>", lambda e: open_file())
    root.bind_all("<Control-O>", lambda e: open_file())
    root.bind_all("<Control-z>", lambda e: undo())
    root.bind_all("<Control-Z>", lambda e: undo())
    root.bind_all("<Control-y>", lambda e: redo())
    root.bind_all("<Control-Y>", lambda e: redo())
    root.bind_all("<Control-Shift-Z>", lambda e: redo())
    root.bind_all("<Control-Shift-S>", lambda e: save_and_exit())
    root.bind_all("<Control-Shift-s>", lambda e: save_and_exit())

    display_canvas.bind("<Key-b>", lambda e: set_mode_brush())
    display_canvas.bind("<Key-B>", lambda e: set_mode_brush())
    display_canvas.bind("<Key-e>", lambda e: set_mode_eraser())
    display_canvas.bind("<Key-E>", lambda e: set_mode_eraser())


# =========================================================
#  ИНИЦИАЛИЗАЦИЯ
# =========================================================
root.update_idletasks()

canvas_width = max(1, display_canvas.winfo_width())
canvas_height = max(1, display_canvas.winfo_height())

if canvas_width <= 1:
    canvas_width = 800
if canvas_height <= 1:
    canvas_height = 500

build_layers_panel()
build_ribbon()

# Прокрутка колёсиком на всей панели слоёв (после построения)
_bind_layers_wheel(layers_panel)

# --- Кнопка темы (правый верхний угол ленты) ---
btn_theme = Button(ribbon_right, text="☾  Тема",
                   font=FONT_BTN, bd=0, relief=FLAT,
                   padx=12, pady=6, cursor="hand2",
                   highlightthickness=0,
                   command=lambda: toggle_theme())
btn_theme.pack(side=TOP, anchor="e")
ToolTip(btn_theme, "Переключить тёмную / светлую тему")


def _theme_refresh():
    btn_theme.configure(bg=T["card"], fg=T["text"],
                        activebackground=T["hover"],
                        activeforeground=T["text"])


def _theme_enter(e):
    btn_theme.configure(bg=T["hover"])


def _theme_leave(e):
    _theme_refresh()


def _theme_release(e):
    _theme_refresh()
    root.after(20, _theme_refresh)


btn_theme.bind("<Enter>", _theme_enter)
btn_theme.bind("<Leave>", _theme_leave)
btn_theme.bind("<ButtonRelease-1>", _theme_release)
_theme_refresh()

# --- Индикатор активного цвета (под кнопкой темы) ---
color_indicator = Canvas(ribbon_right, width=44, height=44,
                         bg=T["bg"], highlightthickness=0, bd=0)
color_indicator.pack(side=TOP, anchor="e", pady=(6, 0))
ToolTip(color_indicator, "Активный цвет кисти")

layers.append(Layer(name="Ваш рисунок",
                    width=canvas_width, height=canvas_height))
active_layer_index = 0
opacity_target = 0

select_color("#E53935")
_highlight_row(0)

apply_system_theme()
redraw_canvas()

_bind_hotkeys()

root.protocol("WM_DELETE_WINDOW", _on_window_close)

# =========================================================
#  ЗАПУСК
# =========================================================
root.mainloop()

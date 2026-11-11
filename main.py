# Rolex Day-Date style analog watch face - smooth sweep + Roman numerals.
# Pure Kivy, no extra libraries. Paste into main.py and run.

from datetime import datetime
from math import sin, cos, radians

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.graphics import (
    Color,
    Ellipse,
    InstructionGroup,
    Line,
    PopMatrix,
    PushMatrix,
    Quad,
    Rectangle,
    Rotate,
    Triangle,
)
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
SWEEP_FPS = 30          # 30 = smooth glide; 60 = silkier but more battery
SHOW_MONTH = True       # month window at 6 oclock
RADIAL_NUMERALS = True  # rotate numerals to face outwards (Rolex style)

Window.clearcolor = get_color_from_hex("#0E1014")

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
GOLD        = get_color_from_hex("#C9A24B")
GOLD_LIGHT  = get_color_from_hex("#EEDBA0")
GOLD_MID    = get_color_from_hex("#D9BC6B")
GOLD_DARK   = get_color_from_hex("#8A6C2C")
DIAL        = get_color_from_hex("#F2E4C2")
DIAL_HI     = get_color_from_hex("#FFF7E2")
DIAL_EDGE   = get_color_from_hex("#CBB98D")
TEXT_DARK   = get_color_from_hex("#2A2A2A")
TEXT_SOFT   = get_color_from_hex("#5B503A")
HAND_GOLD   = get_color_from_hex("#D9B95C")
HAND_FACET  = get_color_from_hex("#F6E7B4")
HAND_EDGE   = get_color_from_hex("#6B5122")
SECOND_GOLD = get_color_from_hex("#B8860B")
WINDOW_BG   = get_color_from_hex("#FFFDF4")

# IIII (not IV) is the traditional watchmaking form Rolex uses.
ROMAN = ["XII", "I", "II", "III", "IIII", "V",
         "VI", "VII", "VIII", "IX", "X", "XI"]


def tint(color, alpha):
    # Re-colour an rgba tuple with a new alpha.
    return (color[0], color[1], color[2], alpha)


class RolexFace(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # text textures are cached so we are not re-rasterising every frame
        self._labels = []
        self._textures = {}

        # three layers: static dial, calendar windows, moving hands
        self.dial_layer = InstructionGroup()
        self.cal_layer = InstructionGroup()
        self.hand_layer = InstructionGroup()
        self.canvas.add(self.dial_layer)
        self.canvas.add(self.cal_layer)
        self.canvas.add(self.hand_layer)

        self._cal_key = None

        self.bind(pos=self._rebuild, size=self._rebuild)
        Clock.schedule_interval(self._tick, 1.0 / SWEEP_FPS)

    # ------------------------------------------------------------------
    # geometry helpers
    # ------------------------------------------------------------------
    def _geom(self):
        cx, cy = self.center_x, self.center_y
        R = min(self.width, self.height) * 0.44
        return cx, cy, R

    @staticmethod
    def _pt(cx, cy, r, ang):
        a = radians(ang)
        return (cx + r * sin(a), cy + r * cos(a))

    @staticmethod
    def _flat(points):
        return [v for p in points for v in p]

    # ------------------------------------------------------------------
    # frame loop
    # ------------------------------------------------------------------
    def _rebuild(self, *args):
        if self.width < 4 or self.height < 4:
            return
        self._labels.clear()
        self._textures.clear()
        self._cal_key = None
        self._draw_dial()
        self._tick(0)

    def _tick(self, _dt):
        now = datetime.now()
        key = (now.year, now.month, now.day)
        if key != self._cal_key:
            self._cal_key = key
            self._draw_calendar(now)
        self._draw_hands(now)

    # ------------------------------------------------------------------
    # text helper
    # ------------------------------------------------------------------
    def _text(self, layer, text, x, y, size, color, bold=True, angle=0.0):
        key = (text, int(size), bold)
        lbl = self._textures.get(key)
        if lbl is None:
            lbl = CoreLabel(text=text, font_size=size, bold=bold)
            lbl.refresh()
            self._textures[key] = lbl
            self._labels.append(lbl)
        tex = lbl.texture
        w, h = tex.size
        layer.add(Color(*color))
        if angle:
            layer.add(PushMatrix())
            layer.add(Rotate(angle=angle, origin=(x, y)))
        layer.add(Rectangle(texture=tex, pos=(x - w / 2.0, y - h / 2.0),
                            size=(w, h)))
        if angle:
            layer.add(PopMatrix())

    # ------------------------------------------------------------------
    # static dial
    # ------------------------------------------------------------------
    def _draw_dial(self):
        layer = self.dial_layer
        layer.clear()
        cx, cy, R = self._geom()

        # ---------- fluted gold bezel ----------
        flutes = 60
        step = 360.0 / flutes
        for i in range(flutes):
            a0 = i * step
            am = a0 + step * 0.5
            a1 = a0 + step
            i0 = self._pt(cx, cy, R * 1.02, a0)
            i1 = self._pt(cx, cy, R * 1.02, am)
            i2 = self._pt(cx, cy, R * 1.02, a1)
            o0 = self._pt(cx, cy, R * 1.14, a0)
            om = self._pt(cx, cy, R * 1.14, am)
            o1 = self._pt(cx, cy, R * 1.14, a1)
            layer.add(Color(*GOLD_LIGHT))
            layer.add(Quad(points=self._flat([i0, i1, om, o0])))
            layer.add(Color(*GOLD_MID))
            layer.add(Quad(points=self._flat([i1, i2, o1, om])))

        layer.add(Color(*GOLD_DARK))
        layer.add(Line(circle=(cx, cy, R * 1.14), width=max(1.0, R * 0.010)))
        layer.add(Color(*GOLD_DARK))
        layer.add(Line(circle=(cx, cy, R * 1.02), width=max(1.0, R * 0.008)))

        # ---------- dial discs ----------
        layer.add(Color(*GOLD_MID))
        layer.add(Ellipse(pos=(cx - R * 1.01, cy - R * 1.01),
                          size=(R * 2.02, R * 2.02)))
        layer.add(Color(*DIAL_EDGE))
        layer.add(Ellipse(pos=(cx - R * 0.995, cy - R * 0.995),
                          size=(R * 1.99, R * 1.99)))
        layer.add(Color(*DIAL))
        layer.add(Ellipse(pos=(cx - R * 0.97, cy - R * 0.97),
                          size=(R * 1.94, R * 1.94)))

        # ---------- sunburst ----------
        rays = 60
        step = 360.0 / rays
        for i in range(0, rays, 2):
            a0 = i * step
            a1 = a0 + step
            p0 = self._pt(cx, cy, R * 0.97, a0)
            p1 = self._pt(cx, cy, R * 0.97, a1)
            layer.add(Color(*tint(DIAL_HI, 0.16)))
            layer.add(Triangle(points=self._flat([(cx, cy), p0, p1])))

        # ---------- minute track ----------
        for i in range(60):
            ang = i * 6.0
            big = (i % 5 == 0)
            r1 = R * 0.885 if big else R * 0.910
            p0 = self._pt(cx, cy, r1, ang)
            p1 = self._pt(cx, cy, R * 0.950, ang)
            layer.add(Color(*(TEXT_SOFT if big else GOLD_DARK)))
            layer.add(Line(points=self._flat([p0, p1]),
                           width=max(1.0, R * (0.011 if big else 0.005))))

        # ---------- Roman numerals ----------
        for h in range(12):
            if h in (0, 3):
                continue
            if h == 6 and SHOW_MONTH:
                continue
            ang = h * 30.0
            x, y = self._pt(cx, cy, R * 0.72, ang)
            self._text(layer, ROMAN[h], x, y, R * 0.125, GOLD_DARK,
                       bold=True,
                       angle=(-ang if RADIAL_NUMERALS else 0.0))

        # ---------- brand text ----------
        self._text(layer, "Rolex", cx, cy + R * 0.34, R * 0.100, GOLD_DARK)
        self._text(layer, "OYSTER PERPETUAL", cx, cy + R * 0.245,
                   R * 0.046, TEXT_SOFT)
        self._text(layer, "SUPERLATIVE CHRONOMETER", cx, cy - R * 0.255,
                   R * 0.040, TEXT_SOFT)
        self._text(layer, "OFFICIALLY CERTIFIED", cx, cy - R * 0.310,
                   R * 0.040, TEXT_SOFT)

    # ------------------------------------------------------------------
    # day / date / month windows
    # ------------------------------------------------------------------
    def _window(self, layer, x, y, w, h):
        layer.add(Color(*GOLD_DARK))
        layer.add(Rectangle(pos=(x - w / 2.0, y - h / 2.0), size=(w, h)))
        inset = max(1.0, w * 0.05)
        layer.add(Color(*WINDOW_BG))
        layer.add(Rectangle(pos=(x - w / 2.0 + inset, y - h / 2.0 + inset),
                            size=(w - inset * 2, h - inset * 2)))

    def _draw_calendar(self, now):
        layer = self.cal_layer
        layer.clear()
        cx, cy, R = self._geom()

        # ---------- DAY window (12) ----------
        day = now.strftime("%A").upper()
        self._window(layer, cx, cy + R * 0.55, R * 0.60, R * 0.175)
        self._text(layer, day, cx, cy + R * 0.55, R * 0.098, TEXT_DARK)

        # ---------- DATE window (3) with cyclops halo ----------
        date = now.strftime("%d")
        qx, qy = cx + R * 0.63, cy
        qw, qh = R * 0.185, R * 0.155

        layer.add(Color(*tint(GOLD_LIGHT, 0.40)))
        layer.add(Ellipse(pos=(qx - qw * 1.15, qy - qh * 1.30),
                          size=(qw * 2.30, qh * 2.60)))
        self._window(layer, qx, qy, qw, qh)
        self._text(layer, date, qx, qy, R * 0.115, TEXT_DARK)

        # ---------- MONTH window (6) ----------
        if SHOW_MONTH:
            month = now.strftime("%B").upper()
            self._window(layer, cx, cy - R * 0.55, R * 0.52, R * 0.165)
            self._text(layer, month, cx, cy - R * 0.55, R * 0.082, TEXT_DARK)

    # ------------------------------------------------------------------
    # hands
    # ------------------------------------------------------------------
    def _dauphine(self, layer, cx, cy, ang, length, half_w, tail):
        a = radians(ang)
        dx, dy = sin(a), cos(a)
        nx, ny = dy, -dx

        def q(r, s=0.0):
            return (cx + dx * r + nx * s, cy + dy * r + ny * s)

        tip = q(length)
        left = q(length * 0.30, half_w)
        right = q(length * 0.30, -half_w)
        back = q(-tail)
        body = [tip, left, back, right]

        layer.add(Color(*HAND_GOLD))
        layer.add(Quad(points=self._flat(body)))
        layer.add(Color(*HAND_FACET))
        layer.add(Triangle(points=self._flat([tip, left, back])))
        layer.add(Color(*HAND_EDGE))
        layer.add(Line(points=self._flat(body), close=True,
                       width=max(1.0, half_w * 0.28)))

    def _draw_hands(self, now):
        layer = self.hand_layer
        layer.clear()
        cx, cy, R = self._geom()

        # sub-second precision -> the sweep is continuous, not ticking
        secs = now.second + now.microsecond / 1000000.0
        mins = now.minute + secs / 60.0
        hrs = (now.hour % 12) + mins / 60.0

        # hour hand
        self._dauphine(layer, cx, cy, hrs * 30.0, R * 0.50, R * 0.055, R * 0.09)
        # minute hand
        self._dauphine(layer, cx, cy, mins * 6.0, R * 0.76, R * 0.040, R * 0.11)

        # second hand
        sec_ang = secs * 6.0
        tip = self._pt(cx, cy, R * 0.86, sec_ang)
        tail = self._pt(cx, cy, R * 0.20, sec_ang + 180.0)
        layer.add(Color(*SECOND_GOLD))
        layer.add(Line(points=self._flat([tail, tip]),
                       width=max(1.2, R * 0.010), cap="round"))
        bw = max(3.0, R * 0.045)
        bx, by = self._pt(cx, cy, R * 0.145, sec_ang + 180.0)
        layer.add(Ellipse(pos=(bx - bw / 2.0, by - bw / 2.0), size=(bw, bw)))

        # ---------- centre cap ----------
        layer.add(Color(*GOLD_DARK))
        layer.add(Ellipse(pos=(cx - R * 0.048, cy - R * 0.048),
                          size=(R * 0.096, R * 0.096)))
        layer.add(Color(*GOLD_LIGHT))
        layer.add(Ellipse(pos=(cx - R * 0.030, cy - R * 0.030),
                          size=(R * 0.060, R * 0.060)))


class RolexApp(App):
    def build(self):
        self.title = "Rolex Day-Date"
        return RolexFace()


if __name__ == "__main__":
    RolexApp().run()

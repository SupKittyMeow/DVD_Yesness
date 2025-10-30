import sys
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor, QImage
from PySide6.QtWidgets import QApplication, QWidget
from PIL import Image, ImageQt

SCALE_FACTOR = 10
SPEED = 5  # pixels per frame for snappier movement
FPS = 60
FRAME_INTERVAL = 1000 // FPS

def get_resample(method_name):
    # Try to resolve 'LANCZOS'/'BICUBIC' from Pillow version
    for mod in (getattr(Image, 'Resampling', None), Image):
        if mod and hasattr(mod, method_name):
            return getattr(mod, method_name)
    return None

class DvdWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Load image with alpha and robust resampling
        pil_image = Image.open("src/DVD_Yesness/image.png").convert("RGBA")
        self.img_width, self.img_height = pil_image.size
        self.img_width //= SCALE_FACTOR
        self.img_height //= SCALE_FACTOR
        resample = get_resample('LANCZOS') or get_resample('BICUBIC') or 0
        pil_image = pil_image.resize((self.img_width, self.img_height), resample)
        self.bgL = pil_image.convert("L")
        self.orig_pil_image = pil_image

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.img_width, self.img_height)

        # cache first pixmap
        self.current_img = pil_image
        self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(self.current_img))

        # Get usable (safe) screen area excluding menubar/dock
        safe_area = QApplication.primaryScreen().availableGeometry()
        self.screen_width = safe_area.width()
        self.screen_height = safe_area.height()
        self.safe_x = safe_area.x()
        self.safe_y = safe_area.y()

        # initial position, integer velocities (avoid name conflict with QWidget.x/y)
        self.pos_x = random.randint(0, self.screen_width - self.img_width)
        self.pos_y = random.randint(0, self.screen_height - self.img_height)
        self.xVel = SPEED if random.randint(0, 1) == 0 else -SPEED
        self.yVel = SPEED if random.randint(0, 1) == 0 else -SPEED
        self.move(self.safe_x + self.pos_x, self.safe_y + self.pos_y)

        # Animation timer at display refresh rate
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(FRAME_INTERVAL)

    def randColor(self):
        newImg = Image.new('RGB', (self.img_width, self.img_height),
                           color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        colored = Image.composite(newImg, self.orig_pil_image, self.bgL)
        rgba = colored.convert('RGBA')
        # Keep original alpha!
        alpha = self.orig_pil_image.split()[-1]
        rgba.putalpha(alpha)
        return rgba

    def tick(self):
        bounced = False
        next_x = self.pos_x + self.xVel
        next_y = self.pos_y + self.yVel

        if next_x >= self.screen_width - self.img_width or next_x <= 0:
            self.xVel = -self.xVel
            bounced = True

        if next_y >= self.screen_height - self.img_height or next_y <= 0:
            self.yVel = -self.yVel
            bounced = True

        self.pos_x += self.xVel
        self.pos_y += self.yVel
        self.move(self.safe_x + self.pos_x, self.safe_y + self.pos_y)

        if bounced:
            # Only update the pixmap/trigger repaint on bounce
            self.current_img = self.randColor()
            self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(self.current_img))
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        # Use correct render hints attributes for PySide6
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        p.drawPixmap(0, 0, self.pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dvd = DvdWidget()
    dvd.show()
    sys.exit(app.exec())

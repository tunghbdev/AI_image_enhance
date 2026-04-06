# desktop_app_qt_modern.py
import sys, io
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
from PIL import Image

API_URL = "http://localhost:8000/enhance"

class ImageEnhancerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ AI Image Enhancement")
        self.resize(950, 550)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f0f0f0;
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QComboBox {
                padding: 4px;
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #2e2e3e;
                color: white;
            }
            QLabel {
                color: #dddddd;
            }
        """)

        # --- Header ---
        header = QLabel("🚀 AI Image Enhancement (Denoise + Low-Light)")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)

        # --- Buttons & controls ---
        self.btn_select = QPushButton("📂 Chọn ảnh")
        self.btn_select.clicked.connect(self.load_image)

        self.cmb_mode = QComboBox()
        self.cmb_mode.addItems(["auto", "denoise", "lowlight"])

        self.btn_process = QPushButton("⚡ Xử lý ảnh")
        self.btn_process.clicked.connect(self.process_image)

        self.btn_save = QPushButton("💾 Lưu kết quả")
        self.btn_save.clicked.connect(self.save_result)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.btn_select)
        top_layout.addWidget(self.cmb_mode)
        top_layout.addWidget(self.btn_process)
        top_layout.addWidget(self.btn_save)

        # --- Image display ---
        self.lbl_original = QLabel("Ảnh gốc")
        self._style_img_label(self.lbl_original)

        self.lbl_result = QLabel("Kết quả")
        self._style_img_label(self.lbl_result)

        img_layout = QHBoxLayout()
        img_layout.addWidget(self.lbl_original)
        img_layout.addWidget(self.lbl_result)

        # --- Main layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(header)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(img_layout)

        self.setLayout(main_layout)

        self.original_image = None
        self.result_image = None

    def _style_img_label(self, label):
        label.setFixedSize(420, 420)
        label.setStyleSheet("border: 2px dashed #888; border-radius: 10px;")
        label.setAlignment(Qt.AlignCenter)
        label.setScaledContents(True)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.original_image = Image.open(file_path).convert("RGB")
            self.lbl_original.setPixmap(QPixmap(file_path))

    def process_image(self):
        if self.original_image is None:
            QMessageBox.warning(self, "Chưa chọn ảnh", "Vui lòng chọn ảnh trước khi xử lý.")
            return

        mode = self.cmb_mode.currentText()

        buf = io.BytesIO()
        self.original_image.save(buf, format="JPEG")
        buf.seek(0)

        files = {"file": ("image.jpg", buf, "image/jpeg")}
        url = f"{API_URL}?mode={mode}"
        try:
            res = requests.post(url, files=files, timeout=60)
            if res.status_code == 200:
                qimg = QImage.fromData(res.content)
                self.lbl_result.setPixmap(QPixmap.fromImage(qimg))
                self.result_image = Image.open(io.BytesIO(res.content))
            else:
                QMessageBox.critical(self, "Lỗi server", f"Mã lỗi: {res.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi kết nối", str(e))

    def save_result(self):
        if self.result_image is None:
            QMessageBox.information(self, "Chưa có kết quả", "Hãy xử lý ảnh trước khi lưu.")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Lưu ảnh", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
        if file_path:
            self.result_image.save(file_path)
            QMessageBox.information(self, "Thành công", f"Ảnh đã lưu tại: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEnhancerApp()
    window.show()
    sys.exit(app.exec_())

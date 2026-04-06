import os, sys
import pytest

# Bảo đảm import được 'app.enhancers.desktop_app_qt_modern'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.enhancers.desktop_app_qt_modern import ImageEnhancerApp  # type: ignore

@pytest.fixture
def app(qtbot):
    ui = ImageEnhancerApp()
    qtbot.addWidget(ui)
    return ui

def test_ui_loads(app):
    assert app.windowTitle() != ""
    assert app.btn_select.text() != ""
    assert app.btn_process.text() != ""
    assert app.cmb_mode.count() > 0
    assert app.lbl_original is not None
    assert app.lbl_result is not None

def test_mode_selection(app, qtbot):
    app.cmb_mode.setCurrentText("denoise")
    assert app.cmb_mode.currentText() == "denoise"

def test_save_without_result(app, qtbot):
    app.result_image = None
    app.save_result()
    # Không crash và vẫn chưa có ảnh kết quả
    assert app.result_image is None

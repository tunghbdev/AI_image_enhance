#!/usr/bin/env bash
set -euo pipefail

echo "=== [1] Kích hoạt venv ==="
source .venv/bin/activate

echo "=== [2] Tạo thư mục reports nếu chưa có ==="
mkdir -p reports

echo "=== [3] Chạy pytest và xuất JUnit XML ==="
PYTHONPATH=. pytest -q tests/ --junitxml=reports/junit.xml

echo "=== [4] Cập nhật kết quả vào Excel ==="
python scripts/xml_to_excel.py reports/junit.xml iqe_desktop_tests.xlsx

echo "=== [5] Mở file Excel kết quả ==="
open iqe_desktop_tests.xlsx || echo "⚠️ Không thể tự động mở Excel. Hãy mở thủ công: iqe_desktop_tests.xlsx"

echo "=== ✅ Hoàn tất! ==="
#!/usr/bin/env bash
set -euo pipefail

echo "=== [1] Kích hoạt venv ==="
source .venv/bin/activate

echo "=== [2] Tạo thư mục reports nếu chưa có ==="
mkdir -p reports

echo "=== [3] Chạy pytest và xuất JUnit XML ==="
PYTHONPATH=. pytest -q tests/ --junitxml=reports/junit.xml

echo "=== [4] Cập nhật kết quả vào Excel ==="
python scripts/xml_to_excel.py reports/junit.xml iqe_desktop_tests.xlsx

echo "=== ✅ Hoàn tất! Mở file iqe_desktop_tests.xlsx để xem kết quả ==="


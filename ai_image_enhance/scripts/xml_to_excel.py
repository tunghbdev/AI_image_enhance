
import sys
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def junit_to_excel(xml_file, excel_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    if root.tag == "testsuites":
        suites = root.findall("testsuite")
    else:
        suites = [root]

    summary = []
    for suite in suites:
        ts = {
            "Run Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Suite": suite.attrib.get("name", "pytest"),
            "Total": int(suite.attrib.get("tests", 0)),
            "Passed": int(suite.attrib.get("tests", 0)) - int(suite.attrib.get("failures", 0)) - int(suite.attrib.get("errors", 0)) - int(suite.attrib.get("skipped", 0)),
            "Failed": int(suite.attrib.get("failures", 0)) + int(suite.attrib.get("errors", 0)),
            "Skipped": int(suite.attrib.get("skipped", 0)),
            "Duration(s)": float(suite.attrib.get("time", 0.0)),
        }
        summary.append(ts)

    df_summary = pd.DataFrame(summary)

    try:
        # Đọc dữ liệu cũ nếu có
        existing = pd.read_excel(excel_file, sheet_name="Test_Run_Summary")
        df_all = pd.concat([existing, df_summary], ignore_index=True)
        with pd.ExcelWriter(excel_file, mode="w", engine="openpyxl") as writer:
            df_all.to_excel(writer, sheet_name="Test_Run_Summary", index=False)
        print(f"✅ Appended new test run at {df_summary['Run Timestamp'].iloc[0]} into {excel_file}")
    except FileNotFoundError:
        # Nếu chưa có thì tạo mới
        with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
            df_summary.to_excel(writer, sheet_name="Test_Run_Summary", index=False)
        print(f"📄 Created new {excel_file} with first test run")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/xml_to_excel.py reports/junit.xml iqe_desktop_tests.xlsx")
    else:
        junit_to_excel(sys.argv[1], sys.argv[2])
import sys
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def junit_to_excel(xml_file, excel_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    if root.tag == "testsuites":
        suites = root.findall("testsuite")
    else:
        suites = [root]

    summary = []
    for suite in suites:
        ts = {
            "Run Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Suite": suite.attrib.get("name", ""),
            "Total": int(suite.attrib.get("tests", 0)),
            "Passed": int(suite.attrib.get("tests", 0)) - int(suite.attrib.get("failures", 0)) - int(suite.attrib.get("errors", 0)) - int(suite.attrib.get("skipped", 0)),
            "Failed": int(suite.attrib.get("failures", 0)) + int(suite.attrib.get("errors", 0)),
            "Skipped": int(suite.attrib.get("skipped", 0)),
            "Duration(s)": float(suite.attrib.get("time", 0.0)),
        }
        summary.append(ts)

    df_summary = pd.DataFrame(summary)

    try:
        # Nếu Excel có sẵn thì append
        with pd.ExcelWriter(excel_file, mode="a", if_sheet_exists="overlay", engine="openpyxl") as writer:
            existing = pd.read_excel(excel_file, sheet_name="Test_Run_Summary")
            df_all = pd.concat([existing, df_summary], ignore_index=True)
            df_all.to_excel(writer, sheet_name="Test_Run_Summary", index=False)
        print(f"✅ Updated {excel_file} with new test run summary")
    except FileNotFoundError:
        # Nếu chưa có thì tạo mới
        with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
            df_summary.to_excel(writer, sheet_name="Test_Run_Summary", index=False)
        print(f"📄 Created new {excel_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/xml_to_excel.py reports/junit.xml iqe_desktop_tests.xlsx")
    else:
        junit_to_excel(sys.argv[1], sys.argv[2])



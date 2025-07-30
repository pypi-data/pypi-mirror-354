from typing import Dict
from jsonschema.validators import Draft7Validator
import json
import re
from pypdf import PdfReader

from parser_notam_package import NOTAMParser
from parser_notam_package.schema import schema_notam


class NOTAMSchema:
    def __init__(self):
        self.notam_schema = schema_notam
    # def missing_value_notam(self, notam_json: Dict) -> Dict:
    #     json = {}
    #     properties = self.notam_schema["properties"]
    #
    #     for field_name, field_def in properties.items():
    #         if field_name in notam_json:
    #             json[field_name] = notam_json[field_name]
    #         else:
    #             field_type = field_def.get("type")
    #             if isinstance(field_type, list):
    #                 json[field_name] = None
    #             elif field_type == "string":
    #                 json[field_name] = ""
    #             elif field_type == "number":
    #                 json[field_name] = 0
    #             elif field_type == "object":
    #                 json[field_name] = {}
    #             elif field_type == "array":
    #                 json[field_name] = []
    #             else:
    #                 json[field_name] = None
    #
    #     return json

    def validate_detail(self, notam_json: Dict) -> bool:
        validator = Draft7Validator(self.notam_schema)
        errors = list(validator.iter_errors(notam_json))

        if not errors:
            return True

        print(f"Lỗi validate nội dung:")
        for error in errors:
            path = '.'.join(str(p) for p in error.path) if error.path else "NOTAM"
            print(f"  - Field: {path} -> {error.message} (Value: {error.instance})")
        return False

    def process_and_validate_pdf(self, pdf_path: str, output_json_path: str):
        """
        Đọc file PDF, xử lý và validate NOTAM theo các quy tắc mới.
        """
        parser = NOTAMParser()
        print(f"Reading pdf file from {pdf_path}...")
        try:
            reader = PdfReader(pdf_path)
            full_text = "\n".join([page.extract_text() for page in reader.pages])
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file '{pdf_path}'.")
            return
        except Exception as e:
            print(f"Lỗi khi đọc file PDF: {e}")
            return
        notam_texts = re.split(r'\n(?=(?:[A-Z]\d{4}/\d{2}\s+)?NOTAM[NRC])', full_text)
        notam_texts = [notam.strip() for notam in notam_texts if notam.strip()]

        if not notam_texts:
            print("Không tìm thấy NOTAM nào trong file PDF.")
            return

        print(f"Tìm thấy {len(notam_texts)} NOTAM. Bắt đầu xử lý...")
        print("-------------------------------------------------")

        valid_notams_json = []
        invalid_notam_ids = []

        for notam_text in notam_texts:
            notam_id = parser.parse_notam_id(notam_text) or f"UNKNOWN_ID ({notam_text[:20]}...)"
            parsed_data, messages = parser.parse_notam(notam_text)
            if parsed_data is None:
                invalid_notam_ids.append(notam_id)
                print(f"ID: {notam_id}")
                for msg in messages:
                    print(f"- {msg}. Sẽ không được ghi vào JSON.")
                continue
            notam_json = parsed_data
            if messages:
                print(f"ID: {notam_id}")
                for msg in messages:
                    print(f"  └─ {msg}")

            if self.validate_detail(notam_json):
                valid_notams_json.append(notam_json)
            else:

                invalid_notam_ids.append(notam_id)
                print("- NOTAM này sẽ không được ghi vào JSON do lỗi validate nội dung.")


        print("-------------------------------------------------")
        if valid_notams_json:
            print(f"\n>>> Ghi {len(valid_notams_json)} NOTAM hợp lệ vào file: {output_json_path}")
            try:
                with open(output_json_path, 'w', encoding='utf-8') as f:
                    json.dump(valid_notams_json, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Lỗi khi ghi file JSON: {e}")
        else:
            print("\n>>> Không có NOTAM nào hợp lệ để ghi ra file.")

        # if invalid_notam_ids:
        #     print("\n-------------------------------------------------")
        #     print(f"Danh sách các NOTAM không hợp lệ hoặc bị lỗi:")
        #     for invalid_id in sorted(list(set(invalid_notam_ids))):
        #         print(f"   - ID: {invalid_id}")
        print("\nHoàn tất.")

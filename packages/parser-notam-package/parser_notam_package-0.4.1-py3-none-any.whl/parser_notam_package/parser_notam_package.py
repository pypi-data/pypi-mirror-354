import re
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, Set, List

from geopy.geocoders import Nominatim

from parser_notam_package.ICAO_dict.ICAO_abbr import abbr
from parser_notam_package.ICAO_dict.ICAO_entity import entity
from parser_notam_package.ICAO_dict.ICAO_location import location_code_prefix
from parser_notam_package.ICAO_dict.ICAO_status import status


class NOTAMParser:
    def __init__(self):
        self.abbreviations = abbr
        self.ICAO_FIELDS = {"A", "B", "C", "D", "E", "F", "G", "Q"}
        self.MANDATORY_FIELDS = {"Q", "A", "B", "C", "E"}
        self.notam_types = {
            "NOTAMN": "NEW",
            "NOTAMC": "CANCEL",
            "NOTAMR": "REPLACE"
        }

    def parse_notam_id(self, notam_text: str) -> str:
        """Parse NOTAM ID from line 1"""
        match = re.search(r'([A-Z]\d{4}/\d{2})', notam_text)
        return match.group(1) if match else None

    def parse_notam_type(self, notam_text: str) -> Dict:
        """Parse NOTAM type from line 1 and extract referenced NOTAM ID if applicable"""
        result = {
            'type': None,
            'referenced_notam': None
        }
        if "NOTAMR" in notam_text:
            result['type'] = "REPLACE"
            replace_match = re.search(r'NOTAMR\s+([A-Z]\d{4}/\d{2})', notam_text)
            if replace_match:
                result['referenced_notam'] = replace_match.group(1)
        elif "NOTAMC" in notam_text:
            result['type'] = "CANCEL"
            cancel_match = re.search(r'NOTAMC\s+([A-Z]\d{4}/\d{2})', notam_text)
            if cancel_match:
                result['referenced_notam'] = cancel_match.group(1)
        elif "NOTAMN" in notam_text:
            result['type'] = "NEW"

        return result

    def parse_q_line(self, notam_text: str) -> Dict:
        """
        Phân tích Q-line với regex CHẶT CHẼ, yêu cầu đầy đủ 8 thành phần.
        Phiên bản này đã được sửa để chấp nhận các độ dài ký tự chính xác.
        """
        q_match = re.search(
            r'Q\)\s*'
            r'([A-Z]{4})/'  # Group 1: FIR (4 ký tự, ví dụ: VVCR)
            r'([A-Z]{5})/'  # Group 2: NOTAM Code (5 ký tự, ví dụ: QCSAS)
            r'([A-Z]{1,2})/'  # Group 3: Traffic (1-2 ký tự, ví dụ: I)
            r'([A-Z]{1,3})/'  # Group 4: Purpose (1-3 ký tự, ví dụ: B)
            r'([A-Z]{1,3})/'  # Group 5: Scope (1-3 ký tự, ví dụ: AE)
            r'(\d{3})/'  # Group 6: Lower Limit (3 chữ số)
            r'(\d{3})/'  # Group 7: Upper Limit (3 chữ số)
            r'(\d{4}[NS]\d{5}[EW]\d{3})',  # Group 8: Coordinate + Radius
            notam_text
        )

        if not q_match:
            # Nếu không khớp với định dạng chặt chẽ này, trả về dictionary rỗng
            return {}

        # Nếu khớp, trích xuất thông tin
        fir = q_match.group(1)
        notam_code = q_match.group(2)
        coord_full_str = q_match.group(8)

        coord_str = coord_full_str[:-3]
        radius = int(coord_full_str[-3:])
        lat_match = re.search(r'(\d{4})([NS])', coord_str)
        lon_match = re.search(r'(\d{5})([EW])', coord_str)

        coordinate = {}
        if lat_match and lon_match:
            coordinate = {
                'lat': lat_match.group(1) + lat_match.group(2),
                'lon': lon_match.group(1) + lon_match.group(2),
                'radius': radius
            }

        return {
            'fir': fir,
            'notam_code': notam_code,
            'coordinate': coordinate
        }

    def parse_notam_code(self, notam):
        q_info = self.parse_q_line(notam)
        notam_code = q_info.get('notam_code', '')
        return notam_code

    def parse_fir(self, notam):
        q_info = self.parse_q_line(notam)
        fir = q_info.get('fir', '')
        return fir

    def parse_coordinate(self, notam):
        q_info = self.parse_q_line(notam)
        area = q_info.get('coordinate', {})
        return area

    def parse_q_code(self, notam: str):
        q_info = self.parse_q_line(notam)
        q_notam = q_info.get('notam_code', '')
        entity_code = q_notam[1:3]
        status_code = q_notam[3:5]

        entity_info = entity.get(entity_code, {})
        category_area = entity_info.get('area', '')
        sub_area = entity_info.get('sub_area', '')
        subject = entity_info.get('subject', '')

        status_info = status.get(status_code, {})
        condition = status_info.get('condition', '')
        modifier = status_info.get('modifier', '')

        return {
            'entity': entity_code,
            'category_area': category_area,
            'sub_area': sub_area,
            'subject': subject,
            'status': status_code,
            'condition': condition,
            'modifier': modifier,
        }

    def parse_entity(self, notam: str):
        q_info = self.parse_q_line(notam)
        q_notam = q_info.get('notam_code', '')
        entity_code = q_notam[1:3]
        return entity_code

    def parse_category_area(self, notam: str):
        q_info = self.parse_q_line(notam)
        q_notam = q_info.get('notam_code', '')
        entity_code = q_notam[1:3]
        entity_info = entity.get(entity_code, {})
        category_area = entity_info.get('area', '')
        return category_area

    def parse_sub_category_area(self, notam: str):
        q_info = self.parse_q_line(notam)
        q_notam = q_info.get('notam_code', '')
        entity_code = q_notam[1:3]
        entity_info = entity.get(entity_code, {})
        sub_area = entity_info.get('sub_area', '')
        return sub_area

    def parse_subject(self, notam: str):
        q_info = self.parse_q_line(notam)
        q_notam = q_info.get('notam_code', '')
        entity_code = q_notam[1:3]
        entity_info = entity.get(entity_code, {})
        subject = entity_info.get('subject', '')
        return subject

    def parse_status(self, notam: str):
        q_info = self.parse_q_line(notam)
        q_notam = q_info.get('notam_code', '')
        status = q_notam[3:5]
        return status

    def parse_condition(self, notam: str):
        q_info = self.parse_q_line(notam)
        q_notam = q_info.get('notam_code', '')
        status_code = q_notam[3:5]
        status_info = status.get(status_code, {})
        condition = status_info.get('condition', '')
        return condition

    def parse_modifier(self, notam: str):
        q_info = self.parse_q_line(notam)
        q_notam = q_info.get('notam_code', '')
        status_code = q_notam[3:5]
        status_info = status.get(status_code, {})
        modifier = status_info.get('modifier', '')
        return modifier

    def parse_location(self, notam_text: str) -> str:
        """Parse location from field A"""
        a_match = re.search(r'A\)\s*([A-Z]{4})', notam_text)
        return a_match.group(1) if a_match else ''

    def parse_state(self, notam: str) -> str:
        location = self.parse_location(notam)
        state = location[0:2]
        return location_code_prefix.get(state)

    def parse_datetime(self, datetime_str: str) -> Optional[datetime]:
        """Parse datetime from format YYMMDDHHmm"""
        try:
            if len(datetime_str) == 10:
                year = 2000 + int(datetime_str[:2])
                month = int(datetime_str[2:4])
                day = int(datetime_str[4:6])
                hour = int(datetime_str[6:8])
                minute = int(datetime_str[8:10])
                return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)
        except:
            pass
        return None

    def parse_dates(self, notam_text: str):
        b_match = re.search(r'B\)\s*(\d{10})', notam_text)
        c_match = re.search(r'C\)\s*([A-Z]{4,}|[0-9]{10})', notam_text.strip())

        valid_from = self.parse_datetime(b_match.group(1)) if b_match else None
        valid_till = None
        if c_match:
            c_value = c_match.group(1)
            if c_value.isdigit():
                valid_till = self.parse_datetime(c_value)
            else:
                valid_till = c_value

        return valid_from, valid_till

    def parse_schedule(self, notam_text: str) -> str:
        """Parse D line to get Schedule"""
        d_match = re.search(r'D\)\s*(.*?)\s*E\)', notam_text, re.DOTALL)
        return self.expand_abbreviations(d_match.group(1).strip()) if d_match else "None"

    def parse_body(self, notam_text: str) -> str:
        """Parse E line to get body content"""

        e_match = re.search(r'E\)\s*(.*?)(?=\n\s*[FG]\)|\Z)', notam_text, re.DOTALL)
        if e_match:
            body = e_match.group(1).strip()
            body = re.sub(r'\s+', ' ', body)
            return self.expand_abbreviations(body)
        return ""

    def parse_created(self, notam_text: str):
        """Parse Created time in Body"""
        created_pattern = r'CREATED:\s*(\d{1,2})\s+(\w{3})\s+(\d{4})\s+(\d{2}):(\d{2}):(\d{2})'

        match = re.search(created_pattern, self.parse_body(notam_text))
        if not match:
            return 'None'

        day, month_str, year, hour, minute, second = match.groups()
        months = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }

        month = months.get(month_str)
        if not month:
            return 'None'

        try:
            dt = datetime(int(year), month, int(day), int(hour), int(minute), int(second))
            return dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        except ValueError:
            return 'None'

    def geopy_address(self, notam_text: str):
        q_match = re.search(r'Q\)\s*([^/]+)/([^/]+)/[^/]+/[^/]+/[^/]+/(\d{3})/(\d{3})/(\d{4}[NS]\d{5}[EW])(\d{3})',
                            notam_text)
        coord_str = q_match.group(5)

        lat_match = re.search(r'(\d{4})([NS])', coord_str)
        lon_match = re.search(r'(\d{5})([EW])', coord_str)

        lat_num = lat_match.group(1)
        lat_dir = lat_match.group(2)

        lon_num = lon_match.group(1)
        lon_dir = lon_match.group(2)

        lat_deg = int(lat_num[:2])
        lat_min = int(lat_num[2:])

        lon_deg = int(lon_num[:3])
        lon_min = int(lon_num[3:])
        lat = lat_deg + lat_min / 60
        lon = lon_deg + lon_min / 60

        if lat_dir == 'S':
            lat = -lat
        if lon_dir == 'W':
            lon = -lon

        geolocator = Nominatim(user_agent="notam_tool")
        location = geolocator.reverse((lat, lon), language='en')
        return location.address

    def parse_limits(self, notam_text: str) -> Tuple[str, str]:
        match = re.search(r'F\)\s*(.*?)\s*G\)\s*(.*)', notam_text, re.DOTALL)
        if match:
            lower_limit = match.group(1).strip()
            upper_limit = match.group(2).strip()
        else:
            f_match = re.search(r'\nF\)\s*(.*)', notam_text)
            g_match = re.search(r'\nG\)\s*(.*)', notam_text)

            lower_limit = f_match.group(1).strip() if f_match else "None"
            upper_limit = g_match.group(1).strip() if g_match else "None"

        return lower_limit, upper_limit

    # Trong lớp NOTAMParser
    def expand_abbreviations(self, text: str) -> str:
        if not isinstance(text, str):
            return text

        expanded_text = text
        sorted_abbrs = sorted(self.abbreviations.items(), key=lambda x: len(x[0]), reverse=True)

        for abbr, full_form in sorted_abbrs:
            pattern = r'(?<![A-Z])' + re.escape(abbr) + r'\b'
            expanded_text = re.sub(pattern, full_form, expanded_text, flags=re.IGNORECASE)

        return expanded_text

    def find_present_fields(self, notam_text: str) -> Set[str]:
        """Tìm và trả về một tập hợp các chữ cái của field có trong NOTAM."""
        return set(re.findall(r'([A-Z])\)', notam_text))

    def preprocess_and_warn_invalid_fields(self, notam_text: str) -> Tuple[str, List[str]]:
        """
        Làm sạch NOTAM bằng cách xóa các field không hợp lệ ("field rác")
        và trả về văn bản sạch cùng danh sách cảnh báo.
        """
        lines = notam_text.splitlines()
        cleaned_lines = []
        warnings = []
        is_in_invalid_block = False

        if lines:
            cleaned_lines.append(lines[0])

        for line in lines[1:]:
            match = re.match(r'^\s*([A-Z])\)', line)
            if match:
                field_letter = match.group(1)
                if field_letter in self.ICAO_FIELDS:
                    is_in_invalid_block = False
                    cleaned_lines.append(line)
                else:
                    is_in_invalid_block = True
                    warnings.append(
                        f"Cảnh báo: Phát hiện và loại bỏ field rác '{field_letter})' ở NOTAM: {self.parse_notam_id(notam_text)}.")
            elif not is_in_invalid_block:
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines), warnings

    def parse_notam(self, notam_text: str) -> Tuple[Optional[Dict], List[str]]:
        clean_notam_text, warnings = self.preprocess_and_warn_invalid_fields(notam_text)
        messages = warnings

        present_fields = self.find_present_fields(clean_notam_text)
        missing_fields = self.MANDATORY_FIELDS - present_fields

        if missing_fields:
            error_message = f"Lỗi: Thiếu các trường bắt buộc: {sorted(list(missing_fields))}"
            messages.append(error_message)
            return None, messages
        try:
            notam_id = self.parse_notam_id(clean_notam_text)
            notam_type_info = self.parse_notam_type(clean_notam_text)
            q_info = self.parse_q_line(clean_notam_text)
            if q_info == {}:
                messages.append(f"Không tìm thấy Q line hoặc Q line sai format: {notam_id}.")
                return None, messages
            location = self.parse_location(clean_notam_text)
            state_name = self.parse_state(clean_notam_text)
            q_code_info = self.parse_q_code(clean_notam_text)
            valid_from, valid_till = self.parse_dates(clean_notam_text)
            valid_from_str = valid_from.isoformat() if isinstance(valid_from, datetime) else valid_from
            valid_till_str = valid_till.isoformat() if isinstance(valid_till, datetime) else valid_till
            schedule_raw = self.parse_schedule(clean_notam_text)
            body_raw = self.parse_body(clean_notam_text)
            lower_limit_raw, upper_limit_raw = self.parse_limits(clean_notam_text)
            schedule_expanded = self.expand_abbreviations(schedule_raw)
            body_expanded = self.expand_abbreviations(body_raw)
            lower_limit_expanded = self.expand_abbreviations(lower_limit_raw)
            upper_limit_expanded = self.expand_abbreviations(upper_limit_raw)

            if (notam_type_info['type'] == 'REPLACE' or notam_type_info['type'] == 'CANCEL') and notam_type_info[
                'referenced_notam'] is None:
                messages.append(f"Cảnh báo: NOTAM loại '{notam_type_info['type']}' thiếu mã NOTAM tham chiếu.")

            result = {
                'state': state_name,
                'id': notam_id,
                'notam_type': notam_type_info['type'],
                'referenced_notam': notam_type_info['referenced_notam'],
                'fir': q_info.get('fir', ''),
                'notam_code': q_info.get('notam_code', ''),
                'entity': q_code_info.get('entity', ''),
                'status': q_code_info.get('status', ''),
                'category_area': q_code_info.get('category_area', ''),
                'sub_area': q_code_info.get('sub_area', ''),
                'subject': q_code_info.get('subject', ''),
                'condition': q_code_info.get('condition', ''),
                'modifier': q_code_info.get('modifier', ''),
                'coordinate': q_info.get('coordinate', {}),
                'location': location,
                'valid_from': valid_from_str,
                'valid_till': valid_till_str,
                'schedule': schedule_expanded,
                'body': body_expanded,
                'lower_limit': lower_limit_expanded,
                'upper_limit': upper_limit_expanded
            }
            return result, warnings
        except Exception as e:
            return None, [f"Lỗi không xác định trong quá trình parse: {e}"]

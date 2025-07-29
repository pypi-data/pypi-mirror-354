import logging
from datetime import datetime
from typing import List, Dict, Callable, Any, Tuple

from .converters import safe_float

FIELDS_POSITIONS = [
    ('STN', 0, 6),
    ('WBAN', 7, 12),
    ('YEARMODA', 13, 21),
    ('TEMP', 21, 27),
    ('TEMP_QUAL', 27, 28),
    ('DEWP', 28, 34),
    ('DEWP_QUAL', 34, 35),
    ('SLP', 35, 41),
    ('SLP_QUAL', 41, 42),
    ('STP', 42, 48),
    ('STP_QUAL', 48, 49),
    ('VISIB', 49, 55),
    ('VISIB_QUAL', 55, 56),
    ('WDSP', 56, 62),
    ('WDSP_QUAL', 62, 63),
    ('MXSPD', 63, 69),
    ('MXSPD_QUAL', 69, 70),
    ('GUST', 70, 76),
    ('GUST_QUAL', 76, 77),
    ('MAX', 77, 83),
    ('MAX_QUAL', 83, 84),
    ('MIN', 84, 90),
    ('MIN_QUAL', 90, 91),
    ('PRCP', 91, 97),
    ('PRCP_QUAL', 97, 98),
    ('SNDP', 98, 104),
    ('SNDP_QUAL', 104, 105),
    ('FRSHTT', 105, 111),
]

class SafeConverterParser:
    def __init__(
            self,
            field_config: Dict[str, List[Callable[[Any], Any]]] = None,
            date_fields: List[str] = None
    ):
        """
        :param field_config: {'FIELD_NAME': [функции_конвертации]}
        :param date_fields: список названий полей с датой
        """
        self.field_config = field_config or {}
        self.date_fields = date_fields or ['DATE', 'YEARMODA']

    @staticmethod
    def parse_header_line(header_line: str) -> List[Tuple[str, int, int]]:
        fields = []
        in_field = False
        for i, ch in enumerate(header_line):
            if ch != ' ' and not in_field:
                start = i
                in_field = True
            elif ch == ' ' and in_field:
                end = i
                field_name = header_line[start:end].strip()
                fields.append((field_name, start, end))
                in_field = False
        if in_field:
            field_name = header_line[start:].strip()
            fields.append((field_name, start, len(header_line)))
        normalized_fields = []
        for name, start, end in fields:
            norm_name = name.replace('-', '').strip().upper()
            normalized_fields.append((norm_name, start, end))
        return normalized_fields

    def parse_line_by_fields(self, line: str, fields: List[Tuple[str, int, int]]) -> Dict[str, Any]:
        record = {}
        for name, start, end in fields:
            raw_val = line[start:end]
            val = raw_val.rstrip('\n\r')
            val_clean = val.strip().replace('*', '').replace('I', '')
            parts = val_clean.split()
            if parts:
                number_part = parts[0]
                try:
                    val_float = float(number_part)
                    record[name] = val_float
                except Exception:
                    record[name] = val_clean
            else:
                record[name] = val_clean
            logging.debug(f"Parsed field '{name}': raw='{raw_val}', cleaned='{val_clean}', value='{record[name]}'")
        record = self.apply_conversions(record)
        record = self.convert_date_fields(record)
        return record

    def apply_conversions(self, record: Dict[str, Any]) -> Dict[str, Any]:
        for field, funcs in self.field_config.items():
            val = safe_float(record.get(field))
            for func in funcs:
                val = func(val)
            record[field] = val
        return record

    @staticmethod
    def safe_parse_date(date_value):
        try:
            if isinstance(date_value, float):
                date_str = str(int(date_value))
            else:
                date_str = str(date_value).split('.')[0]
            dt = datetime.strptime(date_str, '%Y%m%d')
            return dt.isoformat()
        except Exception as e:
            logging.warning(f'Ошибка преобразования даты "{date_value}": {e}')
            return None

    def convert_date_fields(self, record: Dict[str, Any]) -> Dict[str, Any]:
        for key in record.keys():
            if any(df in key.upper() for df in self.date_fields):
                dt_iso = self.safe_parse_date(record[key])
                if dt_iso:
                    record[key] = dt_iso
        return record

    def parse_op_file(self, file_path: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        records = []
        try:
            with open(file_path, encoding='utf-8', errors='ignore') as f:
                header_line = f.readline()
                fields = FIELDS_POSITIONS
                fieldnames = [name for name, _, _ in fields]
                if 'flag' not in [fn.lower() for fn in fieldnames]:
                    fieldnames.append('flag')
                for line_num, line in enumerate(f, start=2):
                    if len(line) < fields[-1][2]:
                        logging.warning(f'Строка {line_num} слишком короткая, пропускаем')
                        continue
                    record = self.parse_line_by_fields(line, fields)
                    if 'flag' not in record and 'flag' in fieldnames:
                        record['flag'] = ''
                    records.append(record)
        except Exception as e:
            logging.error(f'Ошибка чтения файла {file_path}: {e}')
            return [], []
        return records, fieldnames

import logging
from datetime import datetime
from typing import List, Dict, Callable, Any, Tuple

from .converters import safe_float  # Ваш модуль с функцией safe_float


class SafeConverterParser:
    def __init__(
            self,
            field_config: Dict[str, List[Callable[[Any], Any]]] = None,
            date_fields: List[str] = None
    ):
        self.field_config = field_config or {}
        self.date_fields = date_fields or ['DATE', 'YEARMODA']

    @staticmethod
    def parse_header_line(header_line: str, field_widths: List[int]) -> List[Tuple[str, int, int]]:
        fields = []
        start = 0
        for width in field_widths:
            end = start + width
            field_name = header_line[start:end].strip()
            fields.append((field_name, start, end))
            start = end

        # Объединяем поля с кодом качества с предыдущим полем (если необходимо)
        merged_fields = []
        skip_next = False
        for i, (name, start, end) in enumerate(fields):
            if skip_next:
                skip_next = False
                continue
            if i + 1 < len(fields) and fields[i + 1][0].endswith('QUAL'):
                merged_fields.append((name, start, fields[i + 1][2]))
                skip_next = True
            else:
                merged_fields.append((name, start, end))

        normalized_fields = []
        for name, start, end in merged_fields:
            norm_name = name.replace('-', '').strip().upper()
            normalized_fields.append((norm_name, start, end))
        return normalized_fields

    def parse_line_by_fields(self, line: str, fields: List[Tuple[str, int, int]]) -> Dict[str, Any]:
        record = {}
        for name, start, end in fields:
            raw_val = line[start:end]
            val = raw_val.rstrip('\n\r')
            val_clean = val.strip().replace('*', '').replace('I', '')
            if name == 'SLP':
                parts = val_clean.split()
                try:
                    val_float = float(parts[0]) if parts else None
                    if val_float in (9999, 9999.9, 999.9, 999.0, 999):
                        val_float = None
                    record[name] = val_float
                except Exception:
                    record[name] = None
            else:
                parts = val_clean.split()
                if parts:
                    try:
                        val_float = float(parts[0])
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
            if len(date_str) != 8:
                logging.warning(f'Некорректная длина даты "{date_str}", пропускаем преобразование')
                return None
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
                # Пример ширины полей, подберите под свой формат данных
                field_widths = [
                    6,  # STN
                    5,  # WBAN
                    8,  # YEARMODA
                    6,  # TEMP + QUAL
                    6,  # DEWP + QUAL
                    6,  # SLP + QUAL
                    6,  # STP + QUAL
                    6,  # VISIB + QUAL
                    6,  # WDSP + QUAL
                    6,  # MXSPD + QUAL
                    6,  # GUST + QUAL
                    6,  # MAX + QUAL
                    6,  # MIN + QUAL
                    6,  # PRCP + QUAL
                    6,  # SNDP + QUAL
                    6  # FRSHTT
                ]

                fields = self.parse_header_line(header_line, field_widths)
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

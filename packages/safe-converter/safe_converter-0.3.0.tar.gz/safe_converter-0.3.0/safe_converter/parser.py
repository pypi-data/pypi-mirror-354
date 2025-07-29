import logging
from datetime import datetime
from typing import List, Dict, Callable, Any, Tuple

# from .converters import safe_float  # Ваш модуль с функцией safe_float


class SafeConverterParser:
    def __init__(
            self,
            field_config: Dict[str, List[Callable[[Any], Any]]] = None,
            date_fields: List[str] = None
    ):
        self.field_config = field_config or {}
        self.date_fields = date_fields or ['DATE', 'YEARMODA']

    @staticmethod
    def parse_header_line(header_line: str) -> List[Tuple[str, int, int]]:
        # Фиксированные позиции полей
        field_positions = [
            ('STN', 0, 6),
            ('WBAN', 6, 12),
            ('YEARMODA', 12, 20),
            ('TEMP', 20, 26),
            ('DEWP', 26, 32),
            ('SLP', 32, 38),
            ('STP', 38, 44),
            ('VISIB', 44, 50),
            ('WDSP', 50, 56),
            ('MXSPD', 56, 62),
            ('GUST', 62, 68),
            ('MAX', 68, 74),
            ('MIN', 74, 80),
            ('PRCP', 80, 86),
            ('SNDP', 86, 92),
            ('FRSHTT', 92, 98),
        ]
        return [(name, start, end) for name, start, end in field_positions]

    def parse_line_by_fields(self, line: str, fields: List[Tuple[str, int, int]]) -> Dict[str, Any]:
        record = {}
        for name, start, end in fields:
            raw_val = line[start:end]
            val = raw_val.rstrip('\n\r')
            val_clean = val.strip().replace('*', '').replace('I', '')
            try:
                val_float = float(val_clean)
                if val_float in (9999, 9999.9, 999.9, 999.0, 999):
                    val_float = None
                record[name] = val_float
            except Exception:
                record[name] = val_clean
            logging.debug(f"Parsed field '{name}': raw='{raw_val}', cleaned='{val_clean}', value='{record[name]}'")
        record = self.apply_conversions(record)
        record = self.convert_date_fields(record)
        return record

    def apply_conversions(self, record: Dict[str, Any]) -> Dict[str, Any]:
        for field, funcs in self.field_config.items():
            val = record.get(field)
            if val is not None:
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
                fields = self.parse_header_line(header_line)
                fieldnames = [name for name, _, _ in fields]
                if 'flag' not in [fn.lower() for fn in fieldnames]:
                    fieldnames.append('flag')
                for line_num, line in enumerate(f, start=2):
                    if len(line) < 98:  # Сумма всех ширин
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

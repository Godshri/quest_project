import random
from datetime import datetime
import zlib

def generate_kvant_id():
    """Генерация уникального KVANT ID"""
    # Префикс
    prefix = 'KVANT-'
    
    # Текущая дата в формате DDMM
    now = datetime.now()
    date_part = now.strftime('%d%m')
    
    # Случайные блоки
    block1 = ''.join(random.choices('0123456789ABCDEF', k=8))
    block2 = ''.join(random.choices('0123456789ABCDEF', k=4))
    block3 = ''.join(random.choices('0123456789ABCDEF', k=4))
    block4 = ''.join(random.choices('0123456789ABCDEF', k=4))
    
    # Объединяем случайную часть для вычисления контрольной суммы
    random_part = block1 + block2 + block3 + block4
    random_part_lower = random_part.lower()
    
    # Вычисляем CRC32 и берем последние 4 символа
    crc = zlib.crc32(random_part_lower.encode('utf-8'))
    checksum = f"{crc & 0xFFFFFFFF:08X}"[-4:]
    
    # Формируем итоговый ID
    return f"{prefix}{date_part}-{block1}-{block2}-{block3}-{block4}-{checksum}"

def validate_kvant_id(kvant_id):
    """Проверка валидности KVANT ID"""
    try:
        parts = kvant_id.split('-')
        if len(parts) != 7 or parts[0] != 'KVANT':
            return False
        
        random_part = parts[2] + parts[3] + parts[4] + parts[5]
        provided_checksum = parts[6]
        
        # Вычисляем ожидаемую контрольную сумму
        random_part_lower = random_part.lower()
        crc = zlib.crc32(random_part_lower.encode('utf-8'))
        expected_checksum = f"{crc & 0xFFFFFFFF:08X}"[-4:]
        
        return provided_checksum == expected_checksum
    except:
        return False
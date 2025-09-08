// Функция для вычисления CRC32 контрольной суммы
function crc32(str) {
    let crc = 0xFFFFFFFF;
    for (let i = 0; i < str.length; i++) {
        crc ^= str.charCodeAt(i);
        for (let j = 0; j < 8; j++) {
            crc = (crc >>> 1) ^ (crc & 1 ? 0xEDB88320 : 0);
        }
    }
    return (crc ^ 0xFFFFFFFF) >>> 0;
}

// Генерация случайного HEX блока
function generateRandomHex(length) {
    let result = '';
    const characters = '0123456789ABCDEF';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

// Генерация уникального ID
function generateKvantId() {
    // Префикс
    const prefix = 'KVANT-';
    
    // Текущая дата в формате DDMM
    const now = new Date();
    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const datePart = day + month;
    
    // Случайные блоки
    const block1 = generateRandomHex(8); // 8 символов
    const block2 = generateRandomHex(4); // 4 символа
    const block3 = generateRandomHex(4); // 4 символа
    const block4 = generateRandomHex(4); // 4 символа
    
    // Объединяем случайную часть для вычисления контрольной суммы
    const randomPart = block1 + block2 + block3 + block4;
    const randomPartLower = randomPart.toLowerCase();
    
    // Вычисляем CRC32 и берем последние 4 символа
    const crc = crc32(randomPartLower);
    const checksum = crc.toString(16).toUpperCase().slice(-4);
    
    // Формируем итоговый ID
    return `${prefix}${datePart}-${block1}-${block2}-${block3}-${block4}-${checksum}`;
}

// Проверка валидности ID
function validateKvantId(id) {
    try {
        const parts = id.split('-');
        if (parts.length !== 7 || parts[0] !== 'KVANT') {
            return false;
        }
        
        const datePart = parts[1];
        const randomPart = parts[2] + parts[3] + parts[4] + parts[5];
        const providedChecksum = parts[6];
        
        // Вычисляем ожидаемую контрольную сумму
        const randomPartLower = randomPart.toLowerCase();
        const crc = crc32(randomPartLower);
        const expectedChecksum = crc.toString(16).toUpperCase().slice(-4);
        
        return providedChecksum === expectedChecksum;
    } catch (error) {
        return false;
    }
}
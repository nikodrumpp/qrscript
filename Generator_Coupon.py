import random
import string
from datetime import datetime
import json

def handle(data):
    """
    Главная функция для Salebot.
    Принимает параметры в виде строки JSON и возвращает JSON с результатом.
    
    Параметры data могут содержать:
    - action: "generate_single" или "generate_multiple"
    - count: количество кодов для генерации (по умолчанию 1)
    - prefix: префикс кода (по умолчанию "CP")
    """
    try:
        # Парсим JSON строку в словарь
        if isinstance(data, str):
            params = json.loads(data)
        else:
            params = data
            
        # Получаем параметры
        action = params.get('action', 'generate_single')
        count = int(params.get('count', 1))
        prefix = params.get('prefix', 'CP')
        
        # Выполняем действие
        if action == 'generate_single':
            code = generate_coupon_code(prefix)
            return json.dumps({
                'success': True,
                'code': code,
                'message': f'Код успешно сгенерирован: {code}'
            }, ensure_ascii=False)
        
        elif action == 'generate_multiple':
            codes = generate_multiple_codes(count, prefix)
            return json.dumps({
                'success': True,
                'codes': codes,
                'count': len(codes),
                'message': f'Успешно сгенерировано {len(codes)} кодов'
            }, ensure_ascii=False)
        
        else:
            return json.dumps({
                'success': False,
                'error': f'Неизвестное действие: {action}'
            }, ensure_ascii=False)
            
    except json.JSONDecodeError as e:
        return json.dumps({
            'success': False,
            'error': f'Ошибка парсинга JSON: {str(e)}'
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e)
        }, ensure_ascii=False)


def generate_coupon_code(prefix="CP"):
    """
    Генерирует один код купона в формате CP2106-ABC123
    
    Формат:
    - CP (или другой prefix) - константные заглавные буквы
    - 2106 - текущий день и месяц (ДДММ)
    - ABC - случайные заглавные буквы
    - 123 - случайное трёхзначное число
    """
    # Получаем текущую дату
    current_date = datetime.now()
    day_month = current_date.strftime("%d%m")  # Формат ДДММ
    
    # Генерируем случайные буквы (3 заглавные буквы)
    random_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    
    # Генерируем случайное трёхзначное число (100-999)
    random_number = random.randint(100, 999)
    
    # Собираем код
    code = f"{prefix}{day_month}-{random_letters}{random_number}"
    
    return code


def generate_multiple_codes(count, prefix="CP"):
    """
    Генерирует несколько уникальных кодов купонов
    
    Параметры:
    - count: количество кодов для генерации
    - prefix: префикс для кодов
    """
    codes = set()  # Используем множество для гарантии уникальности
    
    while len(codes) < count:
        code = generate_coupon_code(prefix)
        codes.add(code)
    
    return list(codes)


# Дополнительные вспомогательные функции для расширенного использования

def validate_code_format(code, prefix="CP"):
    """
    Проверяет, соответствует ли код заданному формату
    """
    import re
    
    # Паттерн для проверки формата: PREFIX + 4 цифры + дефис + 3 буквы + 3 цифры
    pattern = f"^{prefix}\\d{{4}}-[A-Z]{{3}}\\d{{3}}$"
    
    return bool(re.match(pattern, code))


def parse_code(code):
    """
    Разбирает код на составные части
    """
    try:
        # Находим позицию дефиса
        dash_pos = code.index('-')
        
        # Извлекаем части кода
        prefix = code[:2]
        date_part = code[2:dash_pos]
        letters = code[dash_pos+1:dash_pos+4]
        numbers = code[dash_pos+4:]
        
        return {
            'prefix': prefix,
            'date': date_part,
            'letters': letters,
            'numbers': numbers,
            'full_code': code
        }
    except:
        return None


# Пример использования для тестирования локально
if __name__ == "__main__":
    # Тест функции handle как в Salebot
    test_data = {
        'action': 'generate_single',
        'prefix': 'CP'
    }
    
    result = handle(test_data)
    print("Результат для Salebot:")
    print(result)
    
    # Тест генерации нескольких кодов
    test_data_multiple = {
        'action': 'generate_multiple',
        'count': 5,
        'prefix': 'QR'
    }
    
    result_multiple = handle(test_data_multiple)
    print("\nРезультат генерации нескольких кодов:")
    print(result_multiple)
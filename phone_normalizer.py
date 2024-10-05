import re
import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

SPECIAL_SYMBOL = "+"
COUNTRY_CODE = "38"
ADDITIONAL_CODE = "0"
REG_EXP = r"[^\d+]"
MAX_LENGTH = 9


def normalize_phone(phone_number: str) -> str:
    if not isinstance(phone_number, str):
        logging.warning(f"Вхідний номер не є рядком: {phone_number}")
        return ''

    # Видаляємо всі символи, крім цифр та '+'
    cleaned_number = re.sub(REG_EXP, "", phone_number).strip()
    logging.debug(f"Очищений номер: {cleaned_number}")

    normalized = ''

    # Обробка номерів, що починаються з '+'
    if cleaned_number.startswith(SPECIAL_SYMBOL):
        if cleaned_number.startswith(f"{SPECIAL_SYMBOL}{COUNTRY_CODE}"):
            normalized = cleaned_number
            logging.debug(
                f"Номер починається з '+{COUNTRY_CODE}': {normalized}")
        else:
            # Некоректний міжнародний код
            logging.warning(
                f"Некоректний міжнародний код у номері: {phone_number}")
            return ''
    elif cleaned_number.startswith(f"{COUNTRY_CODE}{ADDITIONAL_CODE}"):
        # Номер починається з '380'
        normalized = f"{SPECIAL_SYMBOL}{cleaned_number}"
        logging.debug(
            f"Номер починається з '{COUNTRY_CODE}{ADDITIONAL_CODE}': {normalized}")
    elif cleaned_number.startswith(ADDITIONAL_CODE):
        # Номер починається з '0'
        normalized = f"{SPECIAL_SYMBOL}{COUNTRY_CODE}{cleaned_number[1:]}"
        logging.debug(f"Номер починається з '{ADDITIONAL_CODE}': {normalized}")
    else:
        # Номер без міжнародного коду
        normalized = f"{SPECIAL_SYMBOL}{COUNTRY_CODE}{cleaned_number}"
        logging.debug(f"Номер без міжнародного коду: {normalized}")

    # Валідація формату номера: '+38' + MAX_LENGTH цифр
    if re.fullmatch(rf'\+{COUNTRY_CODE}\d{{{MAX_LENGTH}}}', normalized):
        return normalized
    else:
        # Якщо формат некоректний, логуємо попередження та повертаємо порожній рядок
        logging.warning(
            f"Нормалізований номер не відповідає формату '+{COUNTRY_CODE}XXXXXXXXX': {normalized}")
        return ''


# Приклад використання:
if __name__ == "__main__":
    raw_numbers = [
        "067\t123 4567",
        "(095) 234-5678\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
        "12345",                  # Некоректний номер
        "+1(234)567-8901",        # Некоректний міжнародний код
        "05034512345",            # Занадто багато цифр
        "050345123",              # Занадто мало цифр
        "",                        # Порожній рядок
        None,                      # Некоректний тип
    ]

    sanitized_numbers = [num for num in (
        normalize_phone(num) for num in raw_numbers) if num]
    print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)

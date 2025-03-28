import os
import translation_agent as ta
import argparse
import subprocess
import time

def measure_time(func):
    """Декоратор для измерения времени выполнения функции."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        
        print(f"Функция '{func.__name__}' выполнилась за {formatted_time}")
        return result
    return wrapper

def parse_arguments():
    parser = argparse.ArgumentParser(description="Перевод документов")

    ##### Аргументы для перевода #####
    parser.add_argument(
        "-i", "--input_language",
        required=False,
        help="Язык ввода (например, 'en', 'fr', 'de')"
    )
    parser.add_argument(
        "-o", "--output_language",
        required=True,
        help="Язык вывода (например, 'ru')"
    )
    parser.add_argument(
        "--do_reflection",
        action="store_true",
        help="Многостадийный перевод для повышения качества, True\False"
    )
    parser.add_argument(
        "-c", "--country",
        required=False,
        help="Страна (например, 'USA', 'France', 'Russia'). Необходимо для уточнения многостадийного перевода"
    )
    parser.add_argument(
        "-f", "--input_file",
        required=True,
        help="Путь к входному файлу"
    )
    parser.add_argument(
        "-d", "--output_dir",
        required=True,
        help="Путь к выходной директории"
    )

    ##### Аргументы для OCR #####
    parser.add_argument(
        "--paginate",
        action="store_true",
        help="Разбивать на страницы."
    )
    parser.add_argument(
        "--force_ocr",
        action="store_true",
        help="Форсировать OCR (может улучшить результаты OCR)."
    )
    parser.add_argument(
        "--page_range",
        required=False,
        help="Номера страниц документа для обработки, e.g. 1-5, 7"
    )

    # Парсим аргументы
    args = parser.parse_args()

    return args

@measure_time
def translate():

    # Получаем аргументы
    args = parse_arguments()

    # Выводим полученные значения для проверки
    source_lang = args.input_language
    target_lang = args.output_language
    country = args.country
    input_file = args.input_file
    output_dir = args.output_dir
    paginate = args.paginate
    force_ocr = args.force_ocr
    page_range = args.page_range
    do_reflection = args.do_reflection

    # Формируем команду для subprocess
    command = ["marker_single "] 
    command.extend([input_file])
    command.extend(["--output_dir", output_dir])
    if paginate:
        command.extend(["--paginate_output"])
    if force_ocr:
        command.extend(["--force_ocr"])
    if page_range:
        command.extend(["--page_range", str(page_range)])

    # Проверка существования входного файла
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Файл {input_file} не найден.")

    print("Запускаю OCR...")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Ошибка при выполнении OCR: {result.stderr}")
    
    print("OCR выполнен успешно.")

    file_name = os.path.basename(input_file).split(".")[0]

    input_path = os.path.join(output_dir, file_name, file_name + '.md')
    output_path = os.path.join(output_dir, file_name, file_name + '_translated.md')

    with open(input_path, encoding="utf-8") as file:
        source_text = file.read()

    translation = ta.translate(
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=source_text,
        do_reflection=do_reflection,
        country=country,
    )
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(translation)

    print(f"Документ успешно переведен и сохранен в {output_path}")


if __name__ == "__main__":
    try:
        translate()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
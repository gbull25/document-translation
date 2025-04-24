import os
import translation_agent as ta
import subprocess
import re
from helpers import *


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

    file_name, file_extension = os.path.splitext(os.path.basename(input_file))
    file_extension=str(file_extension)
    print(file_name, file_extension)

    input_path = os.path.join(output_dir, file_name, file_name + '.md')
    output_file_path = os.path.join(output_dir, file_name, file_name + '_translated' + file_extension)
    output_file_md = os.path.join(output_dir, file_name, file_name + '_translated' + '.md')
    output_final_dir = os.path.join(output_dir, file_name)

    with open(input_path, encoding="utf-8") as file:
        source_text = file.read()

    source_text = replace_pagination(source_text)
    page_break = '<div style="page-break-after: always"></div>'
    pages = re.split(page_break, source_text)
    pagination_markers = re.findall(page_break, source_text)

    translated_pages = []
    for i, page in enumerate(pages):
        print(f"Перевожу страницу {i + 1}/{len(pages)}...")
        translated_page = ta.translate(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=page,
            do_reflection=args.do_reflection,
            country=country,
        )

        # Извлечение ссылок на изображения из исходного текста
        image_pattern = r'!\[\]\((.*?)\)'
        original_images = re.findall(image_pattern, page)

        # Проверка наличия ссылок на изображения в переведенном тексте
        translated_images = re.findall(image_pattern, translated_page)
        missing_images = set(original_images) - set(translated_images)

        # Если есть потерянные ссылки на изображения, добавляем их в конец переведенного текста
        if missing_images:
            print(f"Обнаружены потерянные ссылки на изображения: {missing_images}")
            translated_page += "\n\n" + "\n".join([f"![]({image})" for image in missing_images])  
        
        translated_pages.append(translated_page)

    # Собираем итоговый текст с восстановленными маркерами пагинации
    final_text = ""
    for i in range(len(pages)):
        final_text += translated_pages[i]
        if i < len(pagination_markers):
            final_text += "\n\n" + pagination_markers[i] + "\n\n"

    translation = final_text

    # Переводим изображения
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    image_files = [f for f in os.listdir(output_final_dir) if f.lower().endswith(image_extensions)]
    print(f'Найдено {len(image_files)} изображений')
    for image_file in image_files:
        image_path = os.path.join(output_final_dir, image_file)
        print(f"Переводим изображение: {image_file}")
        try:
            translate_image(image_path,source_lang,target_lang, do_reflection, country)
        except Exception as e:
            print(f"Ошибка при обработке изображения {image_path}: {e}")

    # Сохранение перевода в зависимости от формата
    if file_extension == ".docx":
        save_as_docx(translation, output_file_path)
    elif file_extension == ".pdf":
        save_as_pdf(translation, output_file_path)
    elif file_extension == ".pptx":
        save_as_pptx(translation, output_file_path)
    elif file_extension == ".xlsx":
        save_as_xlsx(translation, output_file_path)
    elif file_extension == ".html":
        save_as_html(translation, output_file_path)
    elif file_extension == ".epub":
        save_as_epub(translation, output_file_path)
    
    # Сохранение перевода в md
    with open(output_file_md, "w", encoding="utf-8") as file:
            file.write(translation)

    print(f"Документ успешно переведен и сохранен в {output_final_dir}")

if __name__ == "__main__":
    try:
        translate()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
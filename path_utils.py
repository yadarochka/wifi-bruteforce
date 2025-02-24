from pathlib import Path
import json

got_password_path = Path("C:\\Users\\astonuser\\Desktop\\wifi\\got_password.json")

def save_in_json(data):
    # Чтение текущих данных из файла
    try:
        with open(got_password_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        # Если файл не существует, создаём пустой словарь
        existing_data = {}

    # Фильтрация данных: оставляем только те ключи, которых нет в существующих данных
    new_data = {key: value for key, value in data.items() if key not in existing_data}

    # Объединение данных
    existing_data.update(new_data)

    # Запись объединённых данных обратно в файл
    with open(got_password_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, indent=4)

    print("Данные успешно записаны в JSON.")

def get_passwords_files():
    with open('password_files_path.json', 'r') as file:
        json_data = json.load(file)

    path = json_data["passwords_directory_path"]

    directory = Path(path)

    if not directory.exists():
        print("Путь не существует. Измените директорию в JSON")
        exit(1)

    print(f"Поиск списков паролей в директории {directory}\t(Директорию можно поменять в JSON)")

    txt_files = list(directory.glob('*.txt'))

    if not any(txt_files):
        print(f"В директории {path} файлы с паролями не найдены. Добавьте файлы в эту директорию, либо измените директорию в JSON")
        exit(1)


    print(f"{'№':<3} {'Файл':<63} {'Паролей':<10}")
    print("-" * 60)  # Разделительная линия
    print(f"{"0":<2}\t{"Все файлы по очереди":<40}\t\t\t\t\t\t{"...":<10} паролей")
    for index, file in enumerate(txt_files, start=1):
        line_count = sum(1 for line in open(file))
        print(f"{index:.<2}\t{file.name:<40}\t\t\t\t\t\t{line_count:<10} паролей")

        # Запрашиваем у пользователя номер файла
    passwords_lists = []
    while True:
        try:
            file_number = int(input("Введите номер файла для выбора: "))
            if file_number == 0:
                print("Вы выбрали все файлы")
                return txt_files
            if 1 <= file_number <= len(txt_files):
                selected_file = txt_files[file_number - 1]
                print(f"Вы выбрали файл: {selected_file}")
                return [selected_file]
            else:
                print("Неверный номер файла.")
        except ValueError:
            print("Пожалуйста, введите цифру.")

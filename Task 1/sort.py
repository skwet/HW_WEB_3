import os
import shutil
import threading
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

extension_categories = {
    ('mp3', 'wav'): 'audio',
    ('mp4', 'avi'): 'video',
    ('jpeg', 'png', 'gif', 'jpg'): 'photo',
    ('txt','docx'): 'docs'
}

def get_files_to_sort(folder_path):
    files_to_sort = {category: [] for category in set(extension_categories.values())}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            _, extension = os.path.splitext(filename)
            extension = extension.lower()[1:]  
            for exts, category in extension_categories.items():
                if extension in exts:
                    files_to_sort[category].append(file_path)
                    break
    return files_to_sort

def create_category_folder(folder_path, category):
    category_folder = os.path.join(folder_path, category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
        logging.info(f"Створено папку для категорії '{category}'")

def move_files(files, category_folder):
    for file in files:
        shutil.move(file, category_folder)
        logging.info(f"Файл '{os.path.basename(file)}' переміщено у папку '{category_folder}'")

def sort_category_files(folder_path, category, files):
    category_folder = os.path.join(folder_path, category)
    create_category_folder(folder_path, category)
    move_files(files, category_folder)

def remove_empty_folders(folder_path):
    for category in extension_categories.values():
        category_folder = os.path.join(folder_path, category)
        if os.path.exists(category_folder) and not os.listdir(category_folder):
            os.rmdir(category_folder)
            logging.info(f"Видалено порожню папку '{category_folder}'")

def sort_files_by_extension(folder_path):
    files_to_sort = get_files_to_sort(folder_path)

    threads = []
    for category, files in files_to_sort.items():
        thread = threading.Thread(target=sort_category_files, args=(folder_path, category, files))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    remove_empty_folders(folder_path)

    logging.info("Сортування завершено.")

def main():
    folder_path = "C:\garbage"  
    sort_files_by_extension(folder_path)

if __name__ == "__main__":
    main()

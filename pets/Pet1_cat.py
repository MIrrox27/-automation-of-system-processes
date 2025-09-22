from ourClass.ClassPets import Pets
import os

if __name__ == '__main__':
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке с проектом

    animations = {
        "poop": [f'{project_dir}\\photos\\cat\\frame1\\sprite_{i}.png' for i in range(1, 16)], # +1 к индексу последней фотки
        "lasy": [f'{project_dir}\\photos\\cat\\frame2\\sprite_{i}.png' for i in range(1, 131)],
        "normal": [f'{project_dir}\\photos\\cat\\frame3\\sprite_{i}.png' for i in range(1, 2)]
    }



    # Шансы для каждой анимации (сумма должна быть 100)
    chances = [10, 10, 80]  #
    cat = Pets(128, 128, 1400, 845, animations, chances, 200)
    Pets.start(cat)


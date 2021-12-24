import os
import time

from PIL import Image


def get_path(path, add):
    return os.path.join(path, add)


def save_logs(log, path_out, name_logger):
    if log:
        log += "\n"
        with open(get_path(path_out, name_logger), 'a') as logfile:
            logfile.write(log)


class ImageScaler:
    def __init__(self):
        self.max_wight_size = (890, 890)
        self.max_height_size = (295, 890)
        self.path_in = os.getcwd()
        self.path_out = get_path(self.path_in, 'out')
        self.extensions = ['jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp', 'webp']
        self.list_images = self.read_folder()
        self.name_logger = '_report.txt'
        self.log = ''''''
        self.name_err_logger = '_errors.txt'
        self.error = ''''''
        if not os.path.exists(self.path_out):
            os.makedirs(self.path_out)

    def read_folder(self):
        list_images = []
        for i in os.listdir(self.path_in):
            if i[i.rfind(".") + 1:].lower() in self.extensions:
                list_images.append(i)
        return list_images

    def load_image(self, image_name):
        with Image.open(get_path(self.path_in, image_name)) as image:
            image.convert('RGB')
            return image

    def save_image(self, image, image_name):
        def check(check_name):
            k = 2
            while True:
                if os.path.exists(get_path(self.path_out, check_name)):
                    check_name = check_name.rsplit('.', 1)[0] + '.ver_' + str(k) + '.' + check_name.rsplit('.', 1)[1]
                    k += 1
                else:
                    break
            return check_name

        old_name = image_name
        if image.format != 'JPEG':
            image_name = image_name.rsplit('.', 1)[0] + '.jpg'
        try:
            image_name = check(image_name)
            image.save(get_path(self.path_out, image_name))
        except:
            origine_name = old_name
            old_name = check(old_name)
            image.save(get_path(self.path_out, old_name))
            os.remove(get_path(self.path_out, image_name))
            self.logger(f'Произошла ошибка, файл {origine_name} сохранен в первоначальном формате!\n', True)
        image.close()

    def logger(self, message, err=False):
        if err:
            self.error += message
        else:
            self.log += message


def scale_images():
    start_time = time.time()
    im = ImageScaler()
    for name in im.list_images:
        try:
            image = im.load_image(name)
            if image.width >= image.height:
                max_size = im.max_wight_size
            else:
                max_size = im.max_height_size
            try:
                image.thumbnail(max_size, Image.ANTIALIAS)
            except:
                im.logger(f'Файл {name} не масштабировался.\n', True)
            try:
                im.save_image(image, name)
                im.logger(f'{name} сохранен.\n')
            except:
                im.logger(f'Произошла ошибка, файл {name} не был сохранен!\n', True)
        except:
            im.logger(f'Произошла ошибка, файл {name} не удалось прочитать!\n', True)

    work_time = time.time() - start_time
    im.logger(f'--- Время выполнения скрипта {work_time} секунд ---\n')
    save_logs(im.log, im.path_out, im.name_logger)
    save_logs(im.error, im.path_out, im.name_err_logger)


if __name__ == '__main__':
    scale_images()

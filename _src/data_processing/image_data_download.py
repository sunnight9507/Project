import pymysql
import urllib.request
import os
import socket

# set download timeout
socket.setdefaulttimeout(30)

# DB connect
conn = pymysql.connect(host='localhost', user='root', password='1234',
                       db='project', charset='utf8')

def load_image():
    '''
    crawling 된 데이터 load
    :return: crawling data
    '''
    curs = conn.cursor()
    # 최근 crawling된 data부터 load
    sql = 'SELECT distinct image, number, kind from protect_animals_url1 ORDER BY NO desc'
    curs.execute(sql)
    images = curs.fetchall()
    return images
def download_image(images):
    '''
    crawling된 data download
    :param images: crawling data(image url, number, kind)
    :return: None
    '''

    path = '../../_db/data/Crawling_data/'

    for url, number, class_name in images:
        dog_cat, *class_name = class_name.split()

        tmp_path = path + dog_cat
        # file 유무 확인 후 없을 경우 생성
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)

        class_name = '_'.join(class_name) if len(class_name) else 'none'

        tmp_path = tmp_path + '/' + class_name
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)

        try:
            # download image
            print(class_name + '_' + number)
            # file 존재할 경우 break
            if os.path.isfile(tmp_path + '/' + class_name + '_' + number + ".jpg"): break
            else: urllib.request.urlretrieve(url, tmp_path + '/' + class_name + '_' + number + ".jpg")

        except:
            # 해당 file remove
            if os.path.isfile(tmp_path + '/' + class_name + '_' + number + ".jpg"):
                os.remove(tmp_path + '/' + class_name + '_' + number + ".jpg")
            print('download error : ' + number)

        # break

if __name__ == '__main__':
    # load image url, name
    images = load_image()

    # download image
    download_image(images)

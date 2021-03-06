import numpy as np
from PIL import Image
import cv2
import os
import pandas as pd
from predict_dog_data import get_steps, make_generators, make_model, make_predictions
from dog_breed_similarity_comparison import load_data, cos_sim, euc_sim, pearson

def get_data_sets(dir, image_size):
    '''
    load image data
    :param dir: input image directory
    :param image_size:
    :return: image, file name
    '''
    data = []
    files = []
    dir_lists = os.listdir(dir)

    for image_dir in dir_lists:
        file_path = os.path.join(dir, image_dir)
        if os.path.isfile(file_path):
            # 한글 directory 오류 방지
            ff = np.fromfile(file_path, np.uint8)
            img = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
            image_array = Image.fromarray(img, 'RGB')
            data.append(np.array(image_array.resize((image_size, image_size))))

            files.append(image_dir)

    return np.array(data), np.array(files)
def compare_similarities_and_show_results(predict, image_path, location, sim_func = pearson, n=10):
    '''
    유사도 비교 후 높은 순으로 10개 보여주기
    :param predict: softmax 확률값
    :param image_path:
    :param n: 보여줄 image 갯수
    :return: None
    '''
    # data = load_data().reset_index()
    # data = data[data['file_name'].apply(lambda x : True if location in x else False)].set_index('file_name')

    data = load_data()

    # file_list = data.apply(lambda x: sim_func(x, predict[0]), axis=1).sort_values(ascending=False).index[:n]
    new_data = data.apply(lambda x: sim_func(x, predict[0]), axis=1).sort_values(ascending=False)

    print(new_data[new_data.apply(lambda x : x[0] > 0)])

    new_data = new_data[new_data.apply(lambda x: x[0] > 0)]

    # print(new_data[new_data > -0.7])

    return new_data
    # print(file_list)
    #
    # img_lst = []
    # for i in file_list:
    #     img_lst.append(Image.open(image_path + '/' + i))
    # init_font()
    # draw_plot(file_list, img_lst)
def show_similar_images(source_dir,output_dir,image_path, location,image_size=224,rand_seed=128):
    '''
    입력한 이미지와 저장되어 있는 공고 데이터와의 유사도 비교 후 10개 보여주기
    :param source_dir: input image directory
    :param output_dir: model and softmax data directory
    :param image_path: 저장되어 있는 image directory
    :param image_size:
    :param rand_seed:
    :return: None
    '''
    # load one image
    test_data, test_files = get_data_sets(source_dir,image_size)
    t_steps, t_batch_size = get_steps(test_data)
    test_gen = make_generators(test_data, t_batch_size)

    # init model
    model = make_model(rand_seed)
    # predcit
    predict = make_predictions(output_dir, test_gen, t_steps, model)

    # result = pd.DataFrame(predict)

    # print(predict)
    
    # 유사한 image 보여주기
    file_path = compare_similarities_and_show_results(predict, image_path, location, sim_func = pearson)

    return file_path

if __name__ == '__main__':
    source_dir= '../../../_db/data/model_data/test'
    output_dir= '../../../_db/data/model_data/working'
    image_path = '../../../_db/data/Crawling_data/[개]'
    # image_path = '../../../_db/data/model_data/input/dog_data/ours_dog/test'
    location = '경북'

    image_size=224
    rand_seed=256

    file_path = show_similar_images(source_dir,output_dir,image_path,location,image_size=image_size,rand_seed=rand_seed)

    print(file_path)

    pd.DataFrame(file_path).to_csv('test.csv', encoding = 'utf-8')
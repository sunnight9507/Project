import argparse
import scipy.io
import torch
import numpy as np
import os
import pandas as pd
from torchvision import datasets
import matplotlib

matplotlib.use('agg')
import cv2
import matplotlib.pyplot as plt

#####################################################################
# Show result
def imshow(path, title=None):
    """Imshow for Tensor."""
    im = plt.imread(path)
    plt.imshow(im)
    plt.savefig("demo.png")
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated

#######################################################################
# sort the images
# def sort_img(qf, ql, gf, gl ):

def sort_img(qf, gf):
    query = qf.view(-1, 1)
    # print(query.shape)
    score = torch.mm(gf, query)
    score = score.squeeze(1).cpu()
    score = score.numpy()
    #print(score)

    # predict index
    index = np.argsort(score)  # from small to large
    index = index[::-1]
    #print(index)
    return index, score


def main(result,image_datasets):
    ######################################################################
    # Options
    # --------
    query_index = 0
    test_dir= 'C:/Users/kdan/BigJob12/main_project/_db/data/model_data'

    # load data
    data_dir = test_dir
    image_datasets = image_datasets
    result = result

    #image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x)) for x in ['gallery', 'query']}
    #result = scipy.io.loadmat('pytorch_result.mat')
    query_feature = torch.FloatTensor(result['query_f'])
    gallery_feature = torch.FloatTensor(result['gallery_f'])

    query_feature = query_feature.cuda()
    gallery_feature = gallery_feature.cuda()


    i = query_index
    index, score = sort_img(query_feature[i], gallery_feature)
    print('sort index= ', index)
    ########################################################################
    # Visualize the rank result
    query_path, _ = image_datasets['query'].imgs[i]
    print(query_path)

    print('Top 10 images are as follow:')
    try:  # Visualize Ranking Result
        # Graphical User Interface is needed
        fig = plt.figure(figsize=(16, 8))
        ax = plt.subplot(2, 11, 1)
        ax.axis('off')
        #imshow(query_path, 'query')

        # save result for web
        result = [image_datasets['gallery'].imgs[index[_]][0].split('\\')[-1][:-4].split('_')[-1] for _ in range(10)]
        print(result)
        pd.DataFrame(result).to_csv('C:/Users/kdan/BigJob12/main_project/_db/data/model_data/working/to_web.csv')


        #####DEBUG 용#####
        # for i in range(10):
        #     ax = plt.subplot(1, 11, i + 2)
        #     ax.axis('off')
        #     img_path, _ = image_datasets['gallery'].imgs[index[i]]
        #     ax.set_title('%d : %0.4f' % (i+1, score[index[i]]), color='red')
        #     # cv2.imwrite('./%d.jpg' %(i), img_path)
        #     print(img_path, index[i], score[index[i]])

    except RuntimeError:
        for i in range(20):
            img_path = image_datasets.imgs[index[i]]
            print(img_path[0])
        print('If you want to see the visualization of the ranking result, graphical user interface is needed.')

    fig.savefig("show.png")


if __name__ == '__main__':
    main()
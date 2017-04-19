from topN_gfusion import topN_gfusion
from topN_sort import topN_sort
from topN_shuffle import topN_shuffle
from FS_Weight import FS_Weight
from FS_Threshold import FS_Threshold
from surprise import Reader, Dataset

reader = Reader(line_format='user item rating', sep=':')
train_file = 'data/usr_ratings.train'
test_file = 'data/usr_ratings.test'
data = Dataset.load_from_folds([(train_file, test_file)], reader)

trainset, testset = data.folds().next()

algos=[FS_Weight(), FS_Threshold(), topN_gfusion(), topN_shuffle(), topN_sort()]

for algo in algos:

    with open('result/topN_' + algo.__class__.__name__ + '.txt', mode='w') as f:
        print("testing " + algo.__class__.__name__)
        algo.train(trainset)
        for k in [5, 10, 15, 20, 25]:
            for nitem in [10, 20]:
                precision, recall, coverage = algo.precisionAndRecallAndCoverage(testset, k, nitem)
                f.write("%d,%d,%f,%f,%f\n" % (k, nitem, precision, recall, coverage))
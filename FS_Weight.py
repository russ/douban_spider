# coding=utf-8
from UBCFBase import UBCFBase
from surprise import PredictionImpossible
from surprise import Reader
from surprise import Dataset
from surprise import evaluate, print_perf
from surprise import GridSearch
import numpy as np

class FS_Weight(UBCFBase):
    def __init__(self, k=40, min_k=1, alpha=0.5, file='new_ratings_all.txt', sim_options={}, **kwargs):
        UBCFBase.__init__(self, file, k, min_k, sim_options, **kwargs)
        self.alpha = alpha

    def train(self, trainset):
        UBCFBase.train(self, trainset)

        self.fusion_sim = self.get_fusion_sim(self.sim, self.behavior_sim)

    def get_fusion_sim(self, sim, behavior_sim):

        return self.alpha * sim + (1 - self.alpha) * behavior_sim

    def estimate(self, u, i):

        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unkown.')

        neighbors = [(v, self.fusion_sim[u, v], r) for (v, r) in self.trainset.ir[i]]
        # sort neighbors by fusion similarity
        neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)
        # compute weighted average
        sum_sim = sum_ratings = actual_k = 0
        for (_, sim, r) in neighbors[:self.k]:
            if sim > 0:
                sum_sim += sim
                sum_ratings += sim * r
                actual_k += 1
        if actual_k < self.min_k:
            raise PredictionImpossible('Not enough neighbors.')
        est = sum_ratings / sum_sim
        details = {'actual_k': actual_k}
        return est, details

if __name__ == '__main__':

    reader = Reader(line_format='user item rating', sep=':')
    data = Dataset.load_from_file('new_usr_ratings.txt', reader=reader)

    data.split(n_folds=3)

    param_grid = {'alpha' : np.arange(0, 1, 0.1)}
    grid_search = GridSearch(FS_Weight, param_grid, measures=['RMSE', 'FCP', 'MAE'])

    grid_search.evaluate(data)

    print(grid_search.best_score['RMSE'])
    print(grid_search.best_params['RMSE'])

    print(grid_search.best_score['FCP'])
    print(grid_search.best_params['FCP'])

    print(grid_search.best_score['MAE'])
    print(grid_search.best_params['MAE'])
    # algo = FS_Weight()


    # perf = evaluate(algo, data, measures=['RMSE', 'MAE'])

    # print_perf(perf)

else:
    pass
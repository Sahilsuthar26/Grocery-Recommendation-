import pandas as pd
import numpy as np
# from user import *
from scipy.spatial.distance import hamming
import warnings
import random

class GroceryRecommendation:

    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.grocery_data = pd.read_csv("C:\\Disk E\\grocery recommendation system\\dataset\\grocery_data.csv",
                                        error_bad_lines=False, header=0, usecols=[0, 1, 2], index_col=0,
                                        names=['product_id', 'product', 'category'])
        print("-------------------------------------------------------------------------------------------------------")
        print(self.grocery_data.head())
        print("-------------------------------------------------------------------------------------------------------")
        print(self.grocery_data.describe())
        print("-------------------------------------------------------------------------------------------------------")
        self.ratings_data = pd.read_csv('C:\\Disk E\\grocery recommendation system\\dataset\\grocery_ratings_data.csv',
                                        error_bad_lines=False,
                                        usecols=[0, 1, 2], header=0, names=['user_id', 'product_id', 'rating'])
        print(self.ratings_data.head())
        print("-------------------------------------------------------------------------------------------------------")
        print(self.ratings_data.describe())
        print("-------------------------------------------------------------------------------------------------------")
        print(self.grocery_product(1))
        print("-------------------------------------------------------------------------------------------------------")
        print(self.grocery_category(1))
        print("-------------------------------------------------------------------------------------------------------")
        print(self.frequently_buyied_grocery(1, 10))

        print("\n")

        # Setup Rating Matrix------------------
        print("Setup Rating Matrix------------------")
        print(self.ratings_data.shape, self.grocery_data.shape)
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        self.user_per_product_id = self.ratings_data.product_id.value_counts()
        print(self.user_per_product_id.head())
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        print(self.user_per_product_id.shape)
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        self.user_grocery_rating_matrix = pd.pivot_table(self.ratings_data, index=['user_id'], columns=['product_id'],
                                                         values='rating')
        print(self.user_grocery_rating_matrix.head(10))

        print("\n")

        # Find K Nearest Neighbours------------------
        print("Find K Nearest Neighbours-------------")
        self.user1_ratings = self.user_grocery_rating_matrix.transpose()[self.user1]
        print(self.user1_ratings.head())
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        self.user2_ratings = self.user_grocery_rating_matrix.transpose()[self.user2]
        print(self.user2_ratings.head())
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        # hamming() returns a value which shows the percentage of disagreement
        print(hamming(self.user1_ratings, self.user2_ratings))
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        print(self.distance(self.user1, self.user2))
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        self.user = self.user2
        self.allusers = pd.DataFrame(self.user_grocery_rating_matrix.index)
        # Removing the active user
        self.allusers = self.allusers[self.allusers.user_id != self.user]
        print(self.allusers.head())
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        self.allusers['distance'] = self.allusers['user_id'].apply(lambda N: self.distance(self.user, N))
        print(self.allusers.head())
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        self.K = 10
        self.k_nearest_user = self.allusers.sort_values(['distance'], ascending=True)['user_id'][:self.K]
        print(self.k_nearest_user)
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        self.k_nearest_neighbours = self.nearest_neighbours(self.user1, 5)
        print(self.k_nearest_neighbours)

        print("\n")

        # Find Top N Recommendations
        print("Find K Nearest Neighbours-------------")

        # Nearest Neighbours ratings
        self.nn_ratings = self.user_grocery_rating_matrix[self.user_grocery_rating_matrix.index.isin(self.k_nearest_neighbours)]
        print(self.nn_ratings)
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        # Getting the average rating of each frequentlty buyes by Nearest Neighbours of active user
        self.avg_ratings = self.nn_ratings.apply(np.nanmean).dropna()
        print(self.avg_ratings.head())
        # warning where the columns of NNratings are completely empty(nan)
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        self.grocery_already_buyed = self.user_grocery_rating_matrix.transpose()[self.user].dropna().index
        print(self.grocery_already_buyed)
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        # Removing the grcoery which are already buyed by user
        self.avg_ratings = self.avg_ratings[~self.avg_ratings.index.isin(self.grocery_already_buyed)]
        self.N = 3
        self.top_n_product_id = self.avg_ratings.sort_values(ascending=False).index[:self.N]
        print(self.top_n_product_id)
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        print(pd.Series(self.top_n_product_id).apply(self.grocery_product))
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        print(pd.Series(self.top_n_product_id).apply(self.grocery_category))
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        print(self.frequently_buyied_grocery(self.user2, 5))
        print("        ->>>>>>>>->------------------------------------------------------------------------------------")
        # To remove the RunTimeWarning error
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        # category of recommend grocery are nearly same as that of frequently buyed by active user
        print(self.top_n(self.user2, 10))
        self.recommendations = self.top_n(self.user2, 10)



    def grocery_product(self, product_id):
        product = self.grocery_data.at[product_id, 'product']
        return product

    def grocery_category(self, product_id):
        product_category = self.grocery_data.at[product_id, 'category']
        return product_category

    def frequently_buyied_grocery(self, user_id, N):
        user_ratings = self.ratings_data[self.ratings_data.user_id == user_id]
        sorted_ratings = pd.DataFrame.sort_values(user_ratings, ['rating'], ascending=[0])[:N]
        sorted_ratings['product'] = sorted_ratings['product_id'].apply(self.grocery_product)
        sorted_ratings['category'] = sorted_ratings['product_id'].apply(self.grocery_category)
        return sorted_ratings

    # Wrapping it up in a function
    def distance(self, user1, user2):
        try:
            user1_ratings = self.user_grocery_rating_matrix.transpose()[user1]
            user2_ratings = self.user_grocery_rating_matrix.transpose()[user2]
            distance = hamming(user1_ratings, user2_ratings)
        except Exception as e:
            distance = np.nan
        return distance

    # Wrapping it up in a function
    def nearest_neighbours(self, user, k=10):
        allusers = pd.DataFrame(self.user_grocery_rating_matrix.index)
        allusers = allusers[allusers.user_id != user]
        allusers['distance'] = allusers['user_id'].apply(lambda N:self.distance(user, N))
        k_nearest_users = allusers.sort_values(['distance'], ascending=True)['user_id'][:k]
        return k_nearest_users

    # Wrapping it up in a function
    def top_n(self, user, N = 10):
        k_nearest_users = self.nearest_neighbours(user)
        nn_ratings = self.user_grocery_rating_matrix[self.user_grocery_rating_matrix.index.isin(k_nearest_users)]
        avg_ratings = nn_ratings.apply(np.nanmean).dropna()
        grocery_already_buyed = self.user_grocery_rating_matrix.transpose()[user].dropna().index
        avg_ratings = avg_ratings[~avg_ratings.index.isin(grocery_already_buyed)]
        top_n_product_id = avg_ratings.sort_values(ascending=False).index[:N]
        return pd.DataFrame({'product': pd.Series(top_n_product_id).apply(self.grocery_product),
                             'category': pd.Series(top_n_product_id).apply(self.grocery_category)})

    def get_recommendation(self):
        df = self.recommendations
        val = df.to_dict('split')
        recommended_products = []
        for i in val["data"]:
            recommended_products.append(i[0])
        final_recommended_products = []
        for i in range(3):
            final_recommended_products.append(recommended_products[random.randint(0, 9)])
        return final_recommended_products

# if __name__ == '__main__':
#     val = return_users("rice")
#     print(val[0], val[1])
#     re=GroceryRecommendation(val[0], val[1])
#     print(re.get_recommendation())


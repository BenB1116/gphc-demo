import pandas as pd

class knn:
    def __init__(self, checkout_df, k) -> None:
        self.checkout_df = checkout_df
        self.k = k

    def jaccard(self, item_set1 = set(), item_set2 = set()):
        # 
        num = len(item_set1.intersection(item_set2))
        den = len(item_set1.union(item_set2))

        if den == 0:
            return 0 

        return num / den
    
    def get_jaccard_score(self, item1, item2):
        item1_df = self.checkout_df[self.checkout_df['item_id'] == item1]
        item1_patrons = set(item1_df['patron_id'].values.tolist())

        item2_df = self.checkout_df[self.checkout_df['item_id'] == item2]
        item2_patrons = set(item2_df['patron_id'].values.tolist())

        return self.jaccard(item1_patrons, item2_patrons)


    def get_canidates(self, item):
        # Select all patrons that have checked out item
        can_df = self.checkout_df[self.checkout_df['item_id'] == item]
        can_patrons = set(can_df['patron_id'].values.tolist())

        # Aggregate all items that the list fo patrons have read
        can_items = set()
        for patron in can_patrons:
            can_df = self.checkout_df[self.checkout_df['patron_id'] == patron]
            can_items.update(can_df['item_id'].values.tolist())
        
        return can_items
    
        



patron_df = pd.read_csv('data\clean\patron_data.csv')
new_knn = knn(patron_df, 6)

# print(new_knn.get_canidates(3))

# print(new_knn.jaccard({1,2,3}, {2,3}))

print(new_knn.get_jaccard_score(3, 100))
import pandas as pd
from statistics import mean
from collections import defaultdict

class knn:
    def __init__(self, checkout_df, k, n) -> None:
        self.checkout_df = checkout_df
        self.k = k
        self.n = n


    def jaccard(self, item_set1 = set(), item_set2 = set()):
        # Calculate the numerator and denomenator for Jaccard similarity
        num = len(item_set1.intersection(item_set2))
        den = len(item_set1.union(item_set2))

        if den == 0:
            return 0 

        return num / den
    

    def get_jaccard_score(self, item1, item2):
        # Gather the patrons that have read item1
        item1_df = self.checkout_df[self.checkout_df['item_id'] == item1]
        item1_patrons = set(item1_df['patron_id'].values.tolist())

        # Gather the patrons that have read item2
        item2_df = self.checkout_df[self.checkout_df['item_id'] == item2]
        item2_patrons = set(item2_df['patron_id'].values.tolist())

        # Calculate the Jaccard similarity
        return self.jaccard(item1_patrons, item2_patrons)


    def get_canidates(self, item):
        # Select all patrons that have checked out item
        can_df = self.checkout_df[self.checkout_df['item_id'] == item]
        can_patrons = set(can_df['patron_id'].values.tolist())

        # Aggregate all items that the list of patrons have read
        can_items = set()
        for patron in can_patrons:
            can_df = self.checkout_df[self.checkout_df['patron_id'] == patron]
            can_items.update(can_df['item_id'].values.tolist())
        
        return can_items
    

    def gen_sim_dict(self, item):
        # Get a list of canidate patrons
        can_patrons = self.get_canidates(item)

        # Compuer the simlarity between every item in the canidate item list
        sim_dict = {item2: self.get_jaccard_score(item, item2) for item2 in can_patrons}
        return sim_dict
    

    def average_dicts(self, item_list):
        dict_list = []
        # Generate the similarity dictionary for every item in the item list
        for item in item_list:
            dict_list.append(self.gen_sim_dict(item))

        # Combine all simlarity dictionaries into one dictionary
        merged_dict = defaultdict(list)
        for d in dict_list:
            for key, value in d.items():
                merged_dict[key].append(value)

        # Take the k-average over the merged dictionary
        for key, value in merged_dict.items():
            temp = merged_dict[key]
            # Sort each list in descending order
            temp.sort(reverse=True)
            # Add zeroes up to k or truncate at k
            merged_dict[key] = mean(temp[:self.k] + [0 for _ in range(self.k - len(temp))])

        return merged_dict
    
    def top_n_closest(self, item_list):
        average_dict = self.average_dicts(item_list)
        # Sort the dictinary by values
        average_dict = {k: v for k, v in sorted(average_dict.items(), key=lambda item: item[1], reverse=True)}

        # Remove the elements that are in item_list
        top_list = set(average_dict.keys()) - set(item_list)

        # Return the first n elements
        return list(top_list)[:self.n]

        
# patron_df = pd.read_csv('data\clean\patron_data.csv')
# new_knn = knn(patron_df, 3, 5)

# print(new_knn.top_n_closests([224, 236, 714, 730]))
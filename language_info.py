'''This class is for interacting with the WALS database. It implements the following 
functionalities:
1. Get the list of features in the database, ordered by feature ID, 
and a mapping featureID2idx: feature ID --> index in language vector
as well as a featureidx2desc: index --> description of feature
2. For a given language, get information about that language: language name and ISO-code,
place spoken, phylogenetic family.
For a given language, get the language vector given some set of features: 
values of above features ordered by feature ID (all features by default)
3. Return sets of features of interest, e.g. syntactic features
'''

import os, sys
import csv
from typing import List

WALS_DIR = "cldf-datasets-wals-878ea47/cldf/"

class wals:
    def __init__(self, wals_datapath = None, binary = False):
        '''
        Initialize the WALS object
        Args:
            - wals_datapath (str): path to the WALS data directory
            - binary (bool): whether to use binary features (default: False). Each multi-value feature 
                             is converted to a set of binary features, one for each value. feature2idx
                             and idx2feature are updated accordingly to contain corresponding feature names;
                             this is done internally.

        '''
        print("Reading WALS from ", wals_datapath)
        self.datapath = wals_datapath if wals_datapath else WALS_DIR
        # print(self.datapath, wals_datapath)
        self.feature2idx = {}
        self.idx2feature = {}
        self.feature2desc = {}
        
        self.binary = binary

        self.wals_values_path = os.path.join(self.datapath, "values.csv")
        self.wals_codes_path = os.path.join(self.datapath, "codes.csv")
        self.wals_languages_path = os.path.join(self.datapath, "languages.csv")
        self.lang2desc = {}

        self.get_feature_description() # fills in self.feature2desc
        self.init_language_info() # fills in self.lang2desc
        # print(self.wals_codes_path)

    def get_feature_description(self):
        '''Get the list of features in the database, ordered by feature ID'''
        # Extract columns named "ID" and "Description from self.wals_codes_path"
        # and store them in self.feature2desc
        # This creates a dict of structure
        # feature2desc = {gen_feature_id: {feature_id1: {"Description": feature_description},
        #                                  feature_id2: {"Description": feature_description},
        #                                   "max_value": max_value for that param_id}

        with open(self.wals_codes_path, 'r') as f:

            reader = csv.reader(f)
            header = next(reader)
            paramid_idx = header.index("Parameter_ID")
            desc_idx = header.index("Description")
            id_idx = header.index("ID")

            for row in reader:
                if row[paramid_idx] not in self.feature2desc:
                    self.feature2desc[row[paramid_idx]] = {}
                    self.feature2desc[row[paramid_idx]]["max_value"] = 0
                id = int(row[id_idx].split("-")[1])
                self.feature2desc[row[paramid_idx]][row[id_idx]] = {"Description": row[desc_idx]}
                self.feature2desc[row[paramid_idx]]["max_value"] = \
                    max(self.feature2desc[row[paramid_idx]]["max_value"], id)


    def init_language_info(self):
        '''For all languages, get language name and ISO-code,
        place spoken, phylogenetic family.
        Returns: lang2desc (dict): mapping from language id to language name, iso-code, place, family'''
        with open(self.wals_languages_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            id_idx = header.index("ID")
            name_idx = header.index("Name")
            iso639_code = header.index("ISO639P3code")
            place_idx = header.index("Macroarea")
            family_idx = header.index("Family")
            subfamily_idx = header.index("Subfamily")
            genus_idx = header.index("Genus")

            for row in reader:
                self.lang2desc[row[iso639_code]] = {"Name": row[name_idx], \
                                            "ISO639P3code": row[iso639_code], \
                                            "Macroarea": row[place_idx], \
                                            "Family": row[family_idx], \
                                            "Subfamily": row[subfamily_idx], \
                                            "Genus": row[genus_idx],\
                                            "ID": row[id_idx]}
        
    def get_language_info(self, language_id: str = None, language_name: str = None):
        '''For a given language, get information about that language: language name and ISO-code,
        place spoken, phylogenetic family.
        Args:
            - language_id (str): language ID 
            - language_name (str): language name (either one will work)
        Returns: 
            - lang2desc (dict): mapping from language id to language name, iso-code, place, family
            - None, if language not found
        '''
        if language_id:
            return self.lang2desc[language_id] if language_id in self.lang2desc else None
        if language_name:
            for _, lang_desc in self.lang2desc.items():
                # print(lang_desc["Name"])
                if lang_desc["Name"].strip().casefold() == language_name.strip().casefold():
                    return lang_desc
            return None
        raise ValueError("Provide either language ID or language name.")
    
    def get_predefined_feature_sets(self, feature_set_type: str = None) -> List : 
        '''Return sets of features of interest, e.g. syntactic features
        Args:
            - feature_set_type (str): type of feature set to return
        Returns:
            - features (list): list of features of interest
            - num_values_per_feature (list): number of values per feature (relevant for binary features)
        '''
        
        if feature_set_type == "phonological":
            raise NotImplementedError
        elif feature_set_type == "morphological":
            features = ['20A',
 '21A',
 '21B',
 '26A',
 '27A',
 '28A',
 '29A',
 '30A',
 '31A',
 '32A',
 '33A',
 '34A',
 '35A',
 '37A',
 '38A',
 '39A',
 '39B',
 '40A',
 '44A',
 '45A',
 '65A',
 '66A',
 '67A',
 '68A',
 '69A',
 '70A']
        elif feature_set_type == "syntactic":
            features = ['81A',
'81B',
'82A',
'83A',
'84A',
'85A',
'86A',
'87A',
'88A',
'89A',
'90A',
'90B',
'90C',
'90D',
'90E',
'90F',
'90G',
'91A',
'92A',
'93A',
'94A',
'95A',
'96A',
'97A',
'98A',
'99A',
'100A',
'101A',
'112A',
'115A',
'116A',
'143C',
'143D',
'143E',
'143F',
'144A',
'144C',
'144D',]
        else:
            raise ValueError("Invalid feature set type")
        
        return features

    def _binarize_feature_set(self, feature_set):
        '''Given a feature vector set, binarize it by converting each multi-value feature 
        to a set of binary features, one for each value.
        This function is called internally by get_feature_vector() if self.binary is True.
        Args:
            - feature_set (list): feature vector
        Returns:
            - feature_set (list): binarized feature vector, with cell for each binary feature
        '''
        binarized_feature_set = []
        for feature in feature_set:
            if feature in self.feature2desc:
                for i in range(1, self.feature2desc[feature]["max_value"]+1):
                    binarized_feature_set.append(feature + "-" + str(i)) # e.g. 81A-1, we 
                    # just reconstruct the feature ID from the param_id and the value
                    # These are just the keys of self.feature2desc[feature]
                    # so we can do this more neatly, but this way is more explicit
            else:
                raise ValueError("Invalid feature ID in binarize_feature_set()")
        return binarized_feature_set

    def get_feature_vector(self, feature_set_type: str = None, feature_set: List = None):
        '''Given either a feature_set_type or feature set, return 
        feature2idx (dict): mapping from feature id to index in language vector
        idx2feature (dict): mapping from index in language vector to feature id
        '''

        if feature_set_type:
            feature_set = self.get_predefined_feature_sets(feature_set_type)
        elif not feature_set:
            # If no feature set is specified, use all features
            feature_set = list(self.feature2desc.keys())
        
        if self.binary:
            feature_set = self._binarize_feature_set(feature_set)
        
        feature2idx = {}
        idx2feature = {}
        for feature in feature_set:
            feature2idx[feature] = len(feature2idx)
            idx2feature[len(idx2feature)] = feature

        return feature2idx, idx2feature
        

    def get_language_vector(self, language_id: str, feature2idx: dict = None):
        '''For a given language, get the language vector given some set of features: 
        values of above features ordered by feature ID (all features by default)'''

        if not feature2idx:
            # If no feature2idx is specified, use all features
            feature2idx, _ = self.get_feature_vector()

        lang_vector = [0] * len(feature2idx)
        with open(self.wals_values_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            id_idx = header.index("Language_ID")
            feature_idx = header.index("Parameter_ID")
            value_idx = header.index("Value")

            if self.binary:
                # reconstruct feature ID from param_id and value
                # This is the same as Code-ID in the codes.csv file
                for row in reader:
                    feature = row[feature_idx] + "-" + row[value_idx] 
                    if row[id_idx] == language_id and feature in feature2idx:
                        lang_vector[feature2idx[feature]] = 1

            else:
                for row in reader:
                    if row[id_idx] == language_id and row[feature_idx] in feature2idx:
                        lang_vector[feature2idx[row[feature_idx]]] = int(row[value_idx])

        return lang_vector


# wals_obj = wals()
# language_info = wals_obj.get_language_info("deu")
# print(language_info)
# # print(wals_obj.feature2desc)
# # print(wals_obj.get_language_info("hin"))
# feature2idx, idx2feature = wals_obj.get_feature_vector(feature_set_type="syntactic")
# vector = wals_obj.get_language_vector("deu", feature2idx)
# for i in range(len(vector)):
#     print(idx2feature[i], vector[i], wals_obj.feature2desc[idx2feature[i]])



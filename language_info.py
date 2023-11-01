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
    def __init__(self, wals_datapath = None):
        self.datapath = wals_datapath if wals_datapath else WALS_DIR
        # print(self.datapath, wals_datapath)
        self.feature2idx = {}
        self.idx2feature = {}
        self.feature2desc = {}
        self.wals_values_path = os.path.join(self.datapath, "values.csv")
        self.wals_codes_path = os.path.join(self.datapath, "codes.csv")
        self.wals_languages_path = os.path.join(self.datapath, "languages.csv")
        # print(self.wals_codes_path)

    def get_feature_list(self):
        '''Get the list of features in the database, ordered by feature ID'''
        # Extract columns named "ID" and "Description from self.wals_codes_path"
        # and store them in self.feature2idx and self.feature2desc

        with open(self.wals_codes_path, 'r') as f:

            reader = csv.reader(f)
            header = next(reader)
            id_idx = header.index("Parameter_ID")
            desc_idx = header.index("Description")

            for row in reader:
                self.feature2desc[row[id_idx]] = row[desc_idx]

    def get_language_info(self, language_id: str):
        '''For a given language, get information about that language: language name and ISO-code,
        place spoken, phylogenetic family.
        Returns: lang2desc (dict): mapping from language id to language name, iso-code, place, family'''

        lang2desc = {}
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
                lang2desc[row[id_idx]] = {"Name": row[name_idx], \
                                            "ISO639P3code": row[iso639_code], \
                                            "Macroarea": row[place_idx], \
                                            "Family": row[family_idx], \
                                            "Subfamily": row[subfamily_idx], \
                                            "Genus": row[genus_idx]}
        return lang2desc[language_id]

    def get_predefined_feature_sets(self, feature_set_type: str = None) -> List : 
        '''Return sets of features of interest, e.g. syntactic features'''
        
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

    def get_feature_vector(self, feature_set_type: str = None, feature_set: List = None):
        '''Given either a feature_set_type or feature set, return 
        feature2idx (dict): mapping from feature id to index in language vector
        idx2feature (dict): mapping from index in language vector to feature id
        '''

        if feature_set_type:
            feature_set = self.get_predefined_feature_sets(feature_set_type)
        if not feature_set:
            # If no feature set is specified, use all features
            feature_set = list(self.feature2desc.keys())
        
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

            for row in reader:
                if row[id_idx] == language_id and row[feature_idx] in feature2idx:
                    lang_vector[feature2idx[row[feature_idx]]] = int(row[value_idx])

        return lang_vector




# wals_obj = wals()
# wals_obj.get_feature_list()
# print(wals_obj.feature2desc)
# print(wals_obj.get_language_info("eng"))
# feature2idx, idx2feature = wals_obj.get_feature_vector(feature_set_type="syntactic")
# print(wals_obj.get_language_vector("eng", feature2idx))

# Use stanza to get dependency parse of a sentence
# import stanza
# # stanza.download('en')
# nlp = stanza.Pipeline('en')
# doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
# print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')


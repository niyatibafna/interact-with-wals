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
        self.feature2idx = {}
        self.idx2feature = {}
        self.feature2desc = {}
        self.wals_values_path = os.path.join(self.datapath, "values.csv")
        self.wals_codes_path = os.path.join(self.datapath, "codes.csv")
        self.wals_languages_path = os.path.join(self.datapath, "languages.csv")


    def get_feature_list(self):
        '''Get the list of features in the database, ordered by feature ID'''
        # Extract columns named "ID" and "Description from self.wals_codes_path"
        # and store them in self.feature2idx and self.feature2desc

        with open(self.wals_codes_path, 'r') as f:

            reader = csv.reader(f)
            header = next(reader)
            id_idx = header.index("ID")
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

        if feature_set_type == "syntactic":
            features = ['81A-1',
 '81A-2',
 '81A-3',
 '81A-4',
 '81A-5',
 '81A-6',
 '81A-7',
 '81B-1',
 '81B-2',
 '81B-3',
 '81B-4',
 '81B-5',
 '82A-1',
 '82A-2',
 '82A-3',
 '83A-1',
 '83A-2',
 '83A-3',
 '84A-1',
 '84A-2',
 '84A-3',
 '84A-4',
 '84A-5',
 '84A-6',
 '85A-1',
 '85A-2',
 '85A-3',
 '85A-4',
 '85A-5',
 '86A-1',
 '86A-2',
 '86A-3',
 '87A-1',
 '87A-2',
 '87A-3',
 '87A-4',
 '88A-1',
 '88A-2',
 '88A-3',
 '88A-4',
 '88A-5',
 '88A-6',
 '89A-1',
 '89A-2',
 '89A-3',
 '89A-4',
 '90A-1',
 '90A-2',
 '90A-3',
 '90A-4',
 '90A-5',
 '90A-6',
 '90A-7',
 '90B-1',
 '90B-2',
 '90B-3',
 '90B-4',
 '90B-5',
 '90C-1',
 '90C-2',
 '90C-3',
 '90C-4',
 '90D-1',
 '90D-2',
 '90D-3',
 '90D-4',
 '90D-5',
 '90D-6',
 '90D-7',
 '9E+00',
 '9E-01',
 '9E-02',
 '9E-03',
 '9E-04',
 '9E-05',
 '9E-06',
 '90F-1',
 '90F-2',
 '90G-1',
 '90G-2',
 '90G-3',
 '90G-4',
 '91A-1',
 '91A-2',
 '91A-3',
 '92A-1',
 '92A-2',
 '92A-3',
 '92A-4',
 '92A-5',
 '92A-6',
 '93A-1',
 '93A-2',
 '93A-3',
 '94A-1',
 '94A-2',
 '94A-3',
 '94A-4',
 '94A-5',
 '95A-1',
 '95A-2',
 '95A-3',
 '95A-4',
 '95A-5',
 '96A-1',
 '96A-2',
 '96A-3',
 '96A-4',
 '96A-5',
 '97A-1',
 '97A-2',
 '97A-3',
 '97A-4',
 '97A-5',
 '98A-1',
 '98A-2',
 '98A-3',
 '98A-4',
 '98A-5',
 '98A-6',
 '99A-1',
 '99A-2',
 '99A-3',
 '99A-4',
 '99A-5',
 '99A-6',
 '99A-7',
 '100A-1',
 '100A-2',
 '100A-3',
 '100A-4',
 '100A-5',
 '100A-6',
 '101A-1',
 '101A-2',
 '101A-3',
 '101A-4',
 '101A-5',
 '101A-6',
 '112A-1',
 '112A-2',
 '112A-3',
 '112A-4',
 '112A-5',
 '112A-6',
 '115A-4',
 '116A-1',
 '116A-2',
 '116A-3',
 '116A-4',
 '116A-5',
 '143C-1',
 '143C-2',
 '143C-3',
 '143C-4',
 '143C-5',
 '143C-6',
 '143C-7',
 '143C-8',
 '143C-9',
 '143C-10',
 '143C-11',
 '143C-12',
 '143C-13',
 '143C-14',
 '143C-15',
 '143C-16',
 '143C-17',
 '143C-18',
 '143C-19',
 '143C-20',
 '143C-21',
 '143C-22',
 '143C-23',
 '143D-1',
 '143D-2',
 '143D-3',
 '143D-4',
 '143D-5',
 '143D-6',
 '1.43E+01',
 '1.43E+00',
 '1.43E-01',
 '1.43E-02',
 '143F-1',
 '143F-2',
 '143F-3',
 '144A-1',
 '144A-2',
 '144A-3',
 '144A-4',
 '144A-5',
 '144A-6',
 '144A-7',
 '144A-8',
 '144A-9',
 '144A-10',
 '144A-11',
 '144A-12',
 '144A-13',
 '144A-14',
 '144A-15',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144C',
 '144D',
 '144D',
 '144D',
 '144D',
 '144D',
 '144D',
 '144D',
 '144D',
 '144D',
 '144D',
 '144D',
 '144D']
        elif feature_set_type == "phonological":
            return 
        elif feature_set_type == "morphological":
            return 
        else:
            raise ValueError("Invalid feature set type")



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
            feature2idx, _ = self.get_feature_vector()

        lang_vector = [0] * len(feature2idx)
        with open(self.wals_values_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            id_idx = header.index("ID")
            feature_idx = header.index("Code_ID")
            value_idx = header.index("Value")

            for row in reader:
                if row[id_idx] == language_id:
                    lang_vector[feature2idx[row[feature_idx]]] = row[value_idx]

        return lang_vector




wals_obj = wals()
wals_obj.get_feature_list()
print(wals_obj.feature2desc)
print(wals_obj.get_language_info("eng"))

# Use stanza to get dependency parse of a sentence
import stanza
# stanza.download('en')
nlp = stanza.Pipeline('en')
doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')


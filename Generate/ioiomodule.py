"""
----------------------------------------------------------------------------------------
Copyright (c) 2020 - see AUTHORS file

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
----------------------------------------------------------------------------------------
"""

import json
import os

import numpy as np
from tqdm import tqdm

from Generate import constants as C, preprocessing


#from generateHighlight import *
#from argument_parser import args

def readLabels(game_folder, sequence_length_first_half, framerate=2, num_classes=3):

	json_data = json.load(open(game_folder + C.LABEL_NAME))
	return preprocessing.labelToCategorical(json_data, sequence_length_first_half, framerate, num_classes)

def readFeatures(game_folder, feature_type):

	feature_1 = None

	if os.path.exists(game_folder + feature_type) :
		feature_1 = np.load(game_folder + feature_type)

	else:
		print("Warning... missing at least one half of the game: ", game_folder)
	return feature_1


class Dataset:

	"""
	Dataset class

	This class deals with the loading of the dataset to be able to access the different elements.
	The code loads the features extracted from args.featurestype and returns it.
	It then creates the labels from the json files based on the number of frames where the features were extracted.

	If the preprocessed features are passed as argument, then it will simply load them. Otherwise, it loads everything
	from the original SoccerNet dataset.

	"""

	def __init__(self, dataset_path, set_type, feature_type, framerate, num_class):

		# Get the list of folders to read
		self.dataset_path = dataset_path
		self.datatype = set_type
		

		self.num_classes = num_class
		self.input_shape=None
		self.framerate = 2

		self.set_path = None
		#self.game_list = None
		self.max_index = None

		self.next_index = 0
		self.max_index = 0

		self.features = list()
		self.labels = list()

		self.feature_type = feature_type

	def nextFeatures(self):

		# Get the features
		feature_1= readFeatures(self.dataset_path + self.datatype, self.feature_type)

		# Get the labels if the feature for this game exist
		label_1 = (None)
		if feature_1 is not None :
			label1 = readLabels(self.dataset_path + self.datatype, feature_1.shape[0], self.framerate, self.num_classes)
			
			# Transform the labels to the Time Shift Encodings
			label_1 = preprocessing.oneHotToShifts(label1, C.K_MATRIX)
		
		# Reading order management
		self.next_index += 1
		if self.next_index >= self.max_index:
			#self.randomize()
			return feature_1, label_1, False

		return feature_1, label_1, True

	def storeFeatures(self):

		# Loading from the preprocessed .npy files if available (faster)
		ft='C3D.npy'
		file_path_features = self.dataset_path + self.datatype[0:-4] + "_" + ft[0:-4] + "_features.npy"
		file_path_labels = self.dataset_path + self.datatype[0:-4] + "_" + ft[0:-4] + "_labels.npy"
		#print(file_path_features,"__",file_path_labels)
		if os.path.exists(file_path_features) and os.path.exists(file_path_labels):
			self.features = np.load(file_path_features, allow_pickle=True)
			self.labels = np.load(file_path_labels, allow_pickle=True)
			self.input_shape = (120*2, self.features[0].shape[1],1)
			return 

		self.set_path =self.dataset_path + self.datatype
		#self.game_list = np.load(self.set_path)
		self.max_index = 1
		print("set_path",self.set_path)
		# Otherwise, load the dataset from the original SoccerNet
		ret = True
		pbar = tqdm(total=1)
		while ret:
			feature_1, label_1, ret = self.nextFeatures()
			if feature_1 is not None:
				print(feature_1)
				self.features.append(feature_1)
				self.labels.append(label_1)

			pbar.update(1)
		pbar.close()

		self.input_shape = (120*2, self.features[0].shape[1],1)
		self.features = np.array(self.features)
		self.labels = np.array(self.labels)

		# Save the preregistered features for faster loading next time
		# Check if the folder exist, otherwise create it
		#if not os.path.isdir(self.dataset_path + "/preregistered/"):
		#	os.mkdir(self.dataset_path + "/preregistered/")
		#np.save(file_path_features, self.features)
		#np.save(file_path_labels, self.labels)


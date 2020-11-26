from Generate.FeatureExtractorC3D import FeatureExtractorC3D
#from ui_make import *

def ex1(file_dir, videoname):
    s1=file_dir
    s2=videoname
    FeatureExtractor = FeatureExtractorC3D()
    FeatureExtractor.intervalStrideTime = 0.5
    FeatureExtractor.overwrite = False
    # FeatureExtractor.elaborateDataset(args.dataset)
    #FeatureExtractor.elaborateGame(file_dir + videoname)
    FeatureExtractor.elaborateGame(s1+s2)

if __name__ == "__main__":
    print("+++++++++++")
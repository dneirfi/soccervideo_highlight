# import argument_parser
from Generate import ioiomodule, evaluation, model

#from ui_make import *



def generate(file_dir,videoname, num_class,save_dir,weights):

    # ------------------
    # Load the arguments
    # ------------------
    print("IN")
    #args = argument_parser.args
    NMS_on = 1

    # ----------------
    # Load the testset
    # ----------------
    #num_class = goal+ card+substitution+cornerkick
    print("numclass: ",num_class)
    framerate=2
    feature_type = "C3D.npy"
    #testset = io_module.Dataset(args.datasetpath, C.LIST_TEST, args.featuretype, framerate=args.framerate,
    #                           num_classes = num_class)
   # testset = GenerateHighlightPKG.ioiomodule.Dataset()
    testset = ioiomodule.Dataset(file_dir, videoname, feature_type, framerate, num_class)
    #testset = io_module.Dataseeet(file_dir, videoname, "C3D.npy", framerate, num_class)
    testset.storeFeatures()

    # ----------------
    # Testing settings
    # ----------------

    # Load the network and its weights

    network =model.baseline(testset.input_shape, 16, num_class, 40 * 2, 5)
    network.load_weights(weights)

    # Evaluate and display the average-mAP
    average_mAP = evaluation.average_mAP(testset, network, save_dir + "/Test_Average_mAP.log", NMS_on=NMS_on)
    print("Average-mAP: ", average_mAP)

    #end =True
'''
    # For the all videos of the testset, get the graphs and numpy arrays of the results
    counter = 0
    for data, label in tqdm(zip(testset.features, testset.labels)):
        evaluation.graphVideo(data, label, network, args.savepath + "/Test_" + str(counter) + ".png", NMS_on=NMS_on)
'''
if __name__ == "__main__":
    print("+++++++++++")
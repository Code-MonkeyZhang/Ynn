import time
from typing import List
from .Layer_class import *
from .util import *

"""
======================================================================
Model Class
======================================================================
"""


class Model:
    def __init__(self, dense_array: List[Layer], cost, name='model') -> None:
        self.dense_array = dense_array
        self.layers_output = []
        self.name = name
        self.cost = cost

    # Iterate through each layer, and puts its output to the next layer
    def predict(self, x: np.ndarray) -> np.ndarray:
        prev_layer_output = x
        for dense_layer in self.dense_array:
            self.layers_output.append((dense_layer, prev_layer_output))
            layer_output = dense_layer.compute_layer(prev_layer_output)
            prev_layer_output = layer_output
        return prev_layer_output

    def fit(self, X_train, y_train, learning_rate, epochs, batch_size=32, b1=0.9, b2=0.999, epsilon=1e-8):
        # perform backward prop
        epoch_lost_list = []

        print("Start Training")
        for epoch in range(epochs):
            tic = time.time()

            epoch_lost = 0
            print("Epoch {}/{}  ".format(epoch + 1, epochs))
            # Divide X_train into pieces, each piece is the size of batch size
            X_batch_list, y_batch_list = slice2batches(X_train, y_train, batch_size)

            batch_num = len(X_batch_list)

            # In each epoch, iterate through each batch
            for i in range(batch_num):

                print_progress_bar(i, batch_num)

                # Extract training example and label
                train_example = X_batch_list[i]
                label = y_batch_list[i]

                # Convert label to one-hot
                label_one_hot = np.zeros((label.shape[0], 10))
                label_one_hot[np.arange(
                    label.shape[0]), label] = 1  # use np advanced indexing to allocate the corresponding element to 1

                # Perform forward prop to compute the lost
                self.layers_output.clear()  # Clear the layers_output before Start
                prediction = self.predict(train_example)

                error = compute_cross_entropy_loss(prediction, label_one_hot)
                epoch_lost += error

                ###### START TRAINING #####

                # init backprop_gradient as all ones
                backprop_gradient = np.ones(self.dense_array[-1].get_weights().shape)

                # reverse iterate the layers
                for layer, prev_layer_output in reversed(self.layers_output):
                    if layer.activation == "Flatten":
                        break  # ignore Flatten layer
                    backprop_gradient = layer.train_layer(prev_layer_output,
                                                          prediction,
                                                          label_one_hot,
                                                          learning_rate,
                                                          b1, b2, epsilon,
                                                          backprop_gradient)

            tok = time.time()
            epoch_lost = epoch_lost / batch_num
            epoch_lost_list.append(epoch_lost)
            print(" - Cost {:.6f} / Time {:.4f} ms".format(epoch_lost, (1000 * (tok - tic))))

        plot_loss(epoch_lost_list)

    def set_rand_weight(self):
        for layer in self.dense_array:
            layer.set_random_weights()

    def save(self, path=""):
        for layer in self.dense_array:
            if layer.layer_name == "Flatten":
                continue
            np.save(path + layer.layer_name + "_w" + ".npy", layer.get_weights())
            np.save(path + layer.layer_name + "_b" + ".npy", layer.get_bias())

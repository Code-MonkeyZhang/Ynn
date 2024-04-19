from typing import List
from .Layer_class import *
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

    def fit(self, X_train, y_train, learningRate, epochs):
        # perform backward prop
        print("Start Training")
        for epoch in range(epochs):
            epoch_lost = 0
            # In each epoch we iterate through each training example
            for i in range(X_train.shape[0]):
                # print("Training Image {}".format(i + 1))
                # Make sure to clear the layers_output at the start of processing each sample
                self.layers_output.clear()

                train_example = X_train[i][
                    np.newaxis, ...]  # extract one training example, and turn its shape into (1,28,28)
                label = y_train[i]

                # Manual convert it to one-hot
                label_one_hot = np.zeros((1, 10))
                label_one_hot[0, label] = 1

                # do forward prop to compute lost
                # and save output of each layer
                prediction = self.predict(train_example)

                epoch_lost += self.compute_loss(prediction, label_one_hot)
                # print(epoch_lost)

                ###### START TRAINING #####

                # init backprop_gradient as all ones, when training from the last layer(output layer)
                backprop_gradient = np.ones(self.dense_array[-1].get_weights().shape)

                # reverse iterate the layers
                for layer, prev_layer_output in reversed(self.layers_output):
                    if layer.activation == "Flatten":
                        break  # ignore Flatten layer
                    backprop_gradient = layer.train_layer(prev_layer_output, prediction, label_one_hot, learningRate,
                                                          backprop_gradient)
                    # print("Training Layer {}, weights {:.6f}".format(layer.activation, np.mean(layer.Weights)))

            print("===============================================================================")
            print("Epoch {}/{}     Lost {}".format(epoch + 1, epochs, epoch_lost / X_train.shape[0]))
            # print("Softmax Weights: Avg:{:.6f} Max {:.6f} Min{:.6f}".format(
            #     np.mean(self.dense_array[-1].get_weights()),
            #     np.max(self.dense_array[-1].get_weights()),
            #     np.min(self.dense_array[-1].get_weights())
            # ))
            #
            # print("ReLU Weights: Avg:{:.6f} Max {:.6f} Min{:.6f}".format(
            #     np.mean(self.dense_array[-2].get_weights()),
            #     np.max(self.dense_array[-2].get_weights()),
            #     np.min(self.dense_array[-2].get_weights())
            # ))

    def compute_loss(self, prediction, target):
        # 使用交叉熵损失计算损失
        # 避免对数函数中的数值不稳定，可以添加一个很小的值epsilon到对数函数中
        epsilon = 1e-12
        prediction = np.clip(prediction, epsilon, 1. - epsilon)
        # 计算交叉熵损失
        loss = -np.sum(target * np.log(prediction)) / prediction.shape[0]
        return loss

    def set_rand_weight(self):
        for layer in self.dense_array:
            layer.set_random_weights()

# def evaluate(self):
#     pass
# def get_weights(self):
#     pass
# use forward prop to get prediction

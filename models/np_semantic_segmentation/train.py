# ******************************************************************************
# Copyright 2017-2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

from __future__ import unicode_literals, print_function, division, \
    absolute_import

import os

from neon import logger as neon_logger
from neon.backends import gen_backend
from neon.util.argparser import NeonArgparser

from models.np_semantic_segmentation.data import NpSemanticSegData
from models.np_semantic_segmentation.model import NpSemanticSegClassifier


def train_mlp_classifier(dataset, model_file_path, num_epochs, callback_args):
    """

    Args:
        model_file_path (str): model path
        num_epochs (int): number of epochs
        callback_args (dict): callback_arg
        dataset: NpSemanticSegData object containing the dataset
    Returns:
        print error_rate, test_accuracy_rate and precision_recall_rate evaluation from the model

    """
    model = NpSemanticSegClassifier(num_epochs, callback_args)
    model.build()
    # run fit
    model.fit(dataset.test_set, dataset.train_set)
    # save model params
    model.save(model_file_path)
    # set evaluation error rates
    error_rate, test_accuracy_rate, precision_recall_rate = model.eval(dataset.test_set)
    neon_logger.display('Misclassification error = %.1f%%' %
                        (error_rate * 100))
    neon_logger.display('Test accuracy rate = %.1f%%' %
                        (test_accuracy_rate * 100))
    neon_logger.display('precision rate = %s!!' %
                        (str(precision_recall_rate[0])))
    neon_logger.display('recall rate = %s!!' %
                        (str(precision_recall_rate[1])))


if __name__ == "__main__":
    # parse the command line arguments
    parser = NeonArgparser()
    parser.set_defaults(epochs=200)
    parser.add_argument('--data', default='datasets/prepared_data.csv', type=str,
                        help='Path the CSV file where the '
                             'prepared dataset is saved')
    parser.add_argument('--model_path', default='datasets/np_semantic_segmentation', type=str,
                        help='Path the save the model')
    args = parser.parse_args()
    data_path = args.data
    if not os.path.exists(data_path):
        raise Exception('Not valid model settings file')
    model_path = args.model_path
    if not os.path.exists(data_path):
        raise Exception('Not valid model settings file')
    # generate backend
    be = gen_backend(batch_size=64)
    # load data sets from file
    data_set = NpSemanticSegData(data_path, train_to_test_ratio=0.8)
    # train the mlp classifier
    train_mlp_classifier(data_set, model_path, args.num_epochs, **args.callback_args)

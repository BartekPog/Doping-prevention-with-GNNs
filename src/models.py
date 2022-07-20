from git import Object
import numpy as np
import torch
from pygod.models import *

class PyGod(Object):
    '''
    Wrapper class for PyGod Models
    '''
    def __init__(self, model_name=None, contamination=0.01, supervised=False):

        self.contamination = contamination
        self.supervised = supervised

        if model_name == 'mlpae':
            '''
            Vanila Multilayer Perceptron Autoencoder.
            '''
            self.model = MLPAE(num_layers=4, epoch=100, contamination=self.contamination) 

        elif model_name == 'gcnae':
            '''
            Vanila Graph Convolutional Networks Autoencoder.
            '''
            self.model = GCNAE(num_layers=4, epoch=100, contamination=self.contamination)

        elif model_name == 'dominant':
            '''
            DOMINANT (Deep Anomaly Detection on Attributed Networks) is an
            anomaly detector consisting of a shared graph convolutional
            encoder, a structure reconstruction decoder, and an attribute
            reconstruction decoder. The reconstruction mean square error of the
            decoders are defined as structure anomaly score and attribute
            anomaly score, respectively.
            '''
            self.model = DOMINANT(num_layers=4, epoch=100, contamination=self.contamination)

        elif model_name == 'scan':
            '''
            SCAN (Structural Clustering Algorithm for Networks) is a clustering
            algorithm, which only takes the graph structure without the node
            features as the input. Note: This model will output detected
            clusters instead of "outliers" descibed in the original paper.
            '''
            self.model = SCAN(eps=0.1, mu=10, contamination=self.contamination)

        elif model_name == 'radar':
            '''
            Radar (Residual Analysis for Anomaly Detection in Attributed
            Networks) is an anomaly detector with residual analysis. This
            model is transductive only.
            '''
            self.model = Radar(contamination=self.contamination, epoch=100)

        elif model_name == 'anomalous': 
            '''
            ANOMALOUS (A Joint Modeling Approach for Anomaly Detection on
            Attributed Networks) is an anomaly detector with CUR decomposition
            and residual analysis. This model is transductive only.
            '''
            self.model = ANOMALOUS(contamination=self.contamination, epoch=100)

        elif model_name == 'one':
            '''
            Outlier Aware Network Embedding for Attributed Networks.
            '''
            self.model = ONE(contamination=self.contamination, iter=5)

        elif model_name == 'done':
            '''
            DONE (Deep Outlier Aware Attributed Network Embedding) consists of
            an attribute autoencoder and a structure autoencoder. It estimates
            five losses to optimize the model, including an attribute proximity
            loss, an attribute homophily loss, a structure proximity loss, a
            structure homophily loss, and a combination loss. It calculates
            three outlier scores, and averages them as an overall scores.
            '''
            self.model = DONE(contamination=self.contamination, epoch=5)

        elif model_name == 'adone':
            '''
            AdONE (Adversarial Outlier Aware Attributed Network
            Embedding) consists of an attribute autoencoder and a structure
            autoencoder. It estimates five loss to optimize the model,
            including an attribute proximity loss, an attribute homophily loss,
            a structure proximity loss, a structure homophily loss, and an
            alignment loss. It calculates three outlier scores, and averages
            them as an overall score.
            '''
            self.model = AdONE(contamination=self.contamination, epoch=5)

        elif model_name == 'gaan':
            '''
            GAAN (Generative Adversarial Attributed Network Anomaly
            Detection) is a generative adversarial attribute network anomaly
            detection framework, including a generator module, an encoder
            module, a discriminator module, and uses anomaly evaluation
            measures that consider sample reconstruction error and real sample
            recognition confidence to make predictions. This model is
            transductive only.
            '''
            self.model = GAAN(contamination=self.contamination, epoch=5)

        elif model_name == 'ocgnn':
            '''
            OCGNN (One-Class Graph Neural Networks for Anomaly Detection in
            Attributed Networks) is an anomaly detector that measures the
            distance of anomaly to the centroid, in a similar fashion to the
            support vector machine, but in the embedding space after feeding
            towards several layers of GCN.
            '''
            self.model = OCGNN(contamination=self.contamination, epoch=20)
        else: 
            print("Invalid model")
            self.model = None

    def train(self, train_graph):
        if self.supervised:
            self.model.fit(train_graph, np.asarray(train_graph.y))    
        self.model.fit(train_graph)

    def get_train_scores(self):
        return self.model.decision_scores_

    def predict(self, test_graph):
        scores = self.model.decision_function(test_graph)
        return scores
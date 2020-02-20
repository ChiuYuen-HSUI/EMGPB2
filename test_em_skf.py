# -*- coding: utf-8 -*-
import numpy as np

from bayou.datastructures import Gaussian, GMM, GMMSequence
from bayou.models import LinearModel, ConstantVelocity
from bayou.expmax.skf import SKF


def get_Q(Q_sig, dt=1):
    Q = (Q_sig ** 2) * np.asarray([
        [(1/3)*np.power(dt, 3), 0, (1/2)*np.power(dt, 2), 0],
        [0, (1/3)*np.power(dt, 3), 0, (1/2)*np.power(dt, 2)],
        [(1/2) * np.power(dt, 2), 0, dt, 0],
        [0, (1/2) * np.power(dt, 2), 0, dt]
    ])
    return Q

def get_Q_RW(Q_sig):
    Q = (Q_sig ** 2) * np.diag([1, 1])
    return Q

def get_R(R_sig):
    R = (R_sig ** 2) * np.eye(2)
    return R


def test_em_skf_cv():
    F = np.asarray([
        [1.0, 0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])
    H = np.asanyarray([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0]
    ])
    """ 
        
    """
    g1 = Gaussian(np.zeros([4, 1]), 10.0 * np.eye(4))
    g2 = Gaussian(np.zeros([4, 1]), 10.0 * np.eye(4))
    initial_gmm_state = GMM([g1, g2])

    # measurements = 5 * np.random.randn(200, 2, 1) + 1

    measurements = np.loadtxt('data/measurement2.csv', delimiter=',')
    measurements = np.expand_dims(measurements, axis=-1)

    gmmsequence = GMMSequence(measurements, initial_gmm_state)

    m1 = LinearModel(F, get_Q(2.0), H, (1.0 ** 2) * np.eye(2))
    m2 = LinearModel(F, get_Q(10.0), H, (1.0 ** 2) * np.eye(2))
    initial_models = [m1, m2]

    Z = np.ones((2, 2)) / 2
    '''
    Z = np.array([[0.7, 0.15, 0.15],
                  [0.15, 0.7, 0.15],
                  [0.15, 0.15, 0.7]])
    '''
    dataset = [gmmsequence]

    models_all, Z_all, dataset, LL = SKF.EM(dataset, initial_models, Z,
                                        max_iters=1000, threshold=1e-7, learn_H=True, learn_R=True,
                                        learn_A=True, learn_Q=True, learn_init_state=False, learn_Z=True,
                                        diagonal_Q=False, wishart_prior=False)

    return models_all, Z_all


def test_em_skf_rw():
    F = np.eye(4)
    H = np.asanyarray([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0]
    ])

    g1 = Gaussian(np.zeros([4, 1]), 10 * np.eye(4))
    g2 = Gaussian(np.zeros([4, 1]), 10 * np.eye(4))
    initial_gmm_state = GMM([g1, g2])

    # measurements = 5 * np.random.randn(200, 2, 1) + 1

    measurements = np.loadtxt(r'data/measurement3.csv', delimiter=',')
    measurements = np.expand_dims(measurements, axis=-1)

    gmmsequence = GMMSequence(measurements, initial_gmm_state)

    m1 = LinearModel(F, (1.0 ** 2) * np.eye(4), H, (2.0 ** 2) * np.eye(2))
    m2 = LinearModel(F, (20.0 ** 2) * np.eye(4), H, (2.0 ** 2) * np.eye(2))
    initial_models = [m1, m2]

    Z = np.ones([2, 2]) / 2

    dataset = [gmmsequence]

    models_all, Z_all, dataset, LL = SKF.EM(dataset, initial_models, Z,
                                        max_iters=100, threshold=0.000001, learn_H=True, learn_R=True,
                                        learn_A=True, learn_Q=True, learn_init_state=False, learn_Z=True,
                                        diagonal_Q=False, wishart_prior=False)


    return models_all, Z_all


def test_em_skf_3():
    g1 = Gaussian(np.ones([4, 1]), np.eye(4))
    g2 = Gaussian(np.ones([2, 1]), np.eye(2))
    initial_gmm_state = GMM([g1, g2])

    # measurements = 5 * np.random.randn(200, 2, 1) + 1

    measurements = np.loadtxt('data/measurements.csv', delimiter=',')
    measurements = np.expand_dims(measurements, axis=-1)

    gmmsequence = GMMSequence(measurements, initial_gmm_state)

    m1 = LinearModel(np.eye(4), np.eye(4), np.eye(4)[:2], np.eye(2))
    m2 = LinearModel(np.eye(2), np.eye(2), np.eye(2), np.eye(2))
    initial_models = [m1, m2]

    Z = np.ones([2, 2]) / 2

    dataset = [gmmsequence]

    new_models, Z, dataset, LL = SKF.EM(dataset, initial_models, Z,
                                        max_iters=100, threshold=0.0001, learn_H=False, learn_R=True,
                                        learn_A=True, learn_Q=True, learn_init_state=True, learn_Z=True,
                                        diagonal_Q=False, wishart_prior=False)

    print(LL)
    print(Z)
    print(new_models[0].R)

    return new_models


def test_em_skf_cvrw():
    F_CV = np.asarray([
        [1.0, 0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])
    F_RW = np.eye(2)
    H_CV = np.asanyarray([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0]
    ])
    H_RW = np.eye(2)
    """ 

    """
    g1 = Gaussian(np.zeros([4, 1]), 25.0 * np.eye(4))
    g2 = Gaussian(np.zeros([2, 1]), 25.0 * np.eye(2))
    initial_gmm_state = GMM([g1, g2])

    # measurements = 5 * np.random.randn(200, 2, 1) + 1

    measurements = np.loadtxt('data/measurement4.csv', delimiter=',')
    measurements = np.expand_dims(measurements, axis=-1)

    gmmsequence = GMMSequence(measurements, initial_gmm_state)

    m1 = LinearModel(F_CV, get_Q(1.0), H_CV, (0.5 ** 2) * np.eye(2))
    m2 = LinearModel(F_RW, get_Q_RW(3.0), H_RW, (0.5 ** 2) * np.eye(2))
    initial_models = [m1, m2]

    Z = np.ones((2, 2)) / 2
    '''
    Z = np.array([[0.7, 0.15, 0.15],
                  [0.15, 0.7, 0.15],
                  [0.15, 0.15, 0.7]])
    '''
    dataset = [gmmsequence]

    models_all, Z_all, dataset, LL = SKF.EM(dataset, initial_models, Z,
                                            max_iters=100, threshold=0.00001, learn_H=True, learn_R=True,
                                            learn_A=True, learn_Q=True, learn_init_state=False, learn_Z=True,
                                            diagonal_Q=False, wishart_prior=False)

    return models_all, Z_all


models_all, Z_all = test_em_skf_rw()


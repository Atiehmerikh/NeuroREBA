import REBA.body_part_reba_calculator.Degree_to_REBA.neck_reba_score as REBA_neck
import REBA.body_part_reba_calculator.Degree_to_REBA.trunk_reba_score as REBA_trunk
import REBA.body_part_reba_calculator.Degree_to_REBA.leg_reba_score as REBA_leg
import REBA.body_part_reba_calculator.Degree_to_REBA.upperarm_reba_score as REBA_UA
import REBA.body_part_reba_calculator.Degree_to_REBA.lowerarm_reba_score as REBA_LA
import REBA.body_part_reba_calculator.Degree_to_REBA.wrist_reba_score as REBA_wrist
import REBA.body_part_reba_calculator.partial_REBA_to_total_REBA as REBA

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam, RMSprop, Nadam, Adamax, Adadelta, Adagrad, SGD
from tensorflow.keras.regularizers import l1, l2
from tensorflow.keras import initializers
from tensorflow.keras.layers import Activation
from tensorflow.keras import backend as K
from tqdm import tqdm
import math

# Neck
def neck_ranges():
    neck_flexion_extension_samples = list(range(-60, 31))
    neck_side_flexion_samples = list(range(-54, 55))
    neck_rotation_samples = list(range(-60, 61))

    return neck_flexion_extension_samples, neck_side_flexion_samples, neck_rotation_samples

def neck_learning_model():

    activation = 'tanh'
    model = Sequential()
    model.add(Dense(3, input_dim=3, activation=activation))
    model.add(Dense(3, activation=activation))
    model.add(Dense(3, activation=activation))
    model.add(Dense(3, activation=activation))
    model.add(Dense(3, activation=activation))
    model.add(Dense(3, activation=activation))
    model.add(Dense(3, activation=activation))
    model.add(Dense(1))
    model.compile(optimizer=SGD(lr=0.01), loss='mse')

    neck_flexion_extension_samples, neck_side_flexion_samples, neck_rotation_samples = neck_ranges()
    for e in tqdm(range(20)):
        for i in neck_flexion_extension_samples:
            num_of_data = len(neck_side_flexion_samples) * len(neck_rotation_samples)
            X_train = np.zeros(shape=(num_of_data, 3))
            y_train = np.zeros(shape=(num_of_data,))
            counter = 0
            for j in neck_side_flexion_samples:
                for k in neck_rotation_samples:
                    m_neck =REBA_neck.NeckREBA([i,j,k])
                    m_neck_reba_score = m_neck.neck_reba_score()
                    X_train[counter, :] = [i,j,k]
                    y_train[counter] = m_neck_reba_score
            model.fit(X_train, y_train, verbose=0)

    model.save('./data/neck_DNN.model')

def neck_model_test():
    neck_flexion_extension_samples, neck_side_flexion_samples, neck_rotation_samples = neck_ranges()
    model = load_model('./data/neck_DNN.model')

    abs_sum = 0
    for i in tqdm(neck_flexion_extension_samples):
        num_of_data = len(neck_side_flexion_samples) * len(neck_rotation_samples)
        X_train = np.zeros(shape=(num_of_data, 3))
        y_train = np.zeros(shape=(num_of_data,))
        counter = 0
        for j in neck_side_flexion_samples:
            for k in neck_rotation_samples:
                m_neck =REBA_neck.NeckREBA([i,j,k])
                m_neck_reba_score = m_neck.neck_reba_score()
                X_train[counter, :] = [i,j,k]
                y_train[counter] = m_neck_reba_score

        pred = model.predict(X_train)
        for y_true, y_pred in zip(y_train, pred):
            abs_sum += math.fabs(y_true - y_pred)

    return (abs_sum, len(neck_flexion_extension_samples) * len(neck_side_flexion_samples) * len(neck_rotation_samples))

# neck_flexion_extension_samples = [-55,-15, -3, 1, 3, 18, 23, 29]
# neck_side_flexion_samples = [-52,-13, -7, 3, 19, 46, 50]
# neck_rotation_samples = [-57,-32, -13, -1, 2, 5, 11, 30, 58]
# neck_sample_test = []
# for i in neck_flexion_extension_samples:
#     for j in neck_side_flexion_samples:
#         for k in neck_rotation_samples:
#             m_neck =REBA_neck.NeckREBA([i,j,k])
#             neck_sample_test.append([i,j,k,m_neck.neck_reba_score()])

# trunk
trunk_flexion_extension_samples = [-30,0,20,60, 70]
trunk_side_flexion_samples = [-40,0, 40]
trunk_rotation_samples = [-35,0, 35]
trunk_sample = []
for i in trunk_flexion_extension_samples:
    for j in trunk_side_flexion_samples:
        for k in trunk_rotation_samples:
            m_trunk =REBA_trunk.TrunkREBA([i,j,k])
            trunk_sample.append([i,j,k,m_trunk.trunk_reba_score()])

# Legs
legs_flexion_samples = [0,30,60,150]
leg_sample = []
for i in legs_flexion_samples:
    m_leg = REBA_leg.LegREBA([i,i])
    leg_sample.append([i, m_leg.leg_reba_score()])

# Upper Arm
right_upper_arm_flexion_extension_samples = [-47,-20,0,20,45,90, 170]
left_upper_arm_flexion_extension_samples = [-47, -20, 0, 20, 45, 90, 170]
right_upper_arm_adduction_abduction_samples = [-2,0, 200]
left_upper_arm_adduction_abduction_samples = [-2,0, 200]
right_shoulder_raise_samples = [0, 30]
left_shoulder_raise_samples = [0, 30]
UA_sample = []
for i in right_upper_arm_flexion_extension_samples:
    for j in left_upper_arm_flexion_extension_samples:
        for k in right_upper_arm_adduction_abduction_samples:
            for l in left_upper_arm_adduction_abduction_samples:
                for m in right_shoulder_raise_samples:
                    for n in left_shoulder_raise_samples:
                        m_UA = REBA_UA.UAREBA([i, j,k,l,m,n])
                        UA_sample.append([i, j, k,l,m,n,m_UA.upper_arm_reba_score()])

# Lower Arm
right_lower_arm_flexion_samples = [0,60,100, 150]
left_lower_arm_flexion_samples = [0,60,100, 150]
LA_sample =[]
for i in right_lower_arm_flexion_samples:
    for j in left_lower_arm_flexion_samples:
        m_LA = REBA_LA.LAREBA([i,j])
        LA_sample.append([i,j,m_LA.lower_arm_score()])

# Wrist
right_wrist_flexion_extension_samples = [-53,-15,15, 47]
left_wrist_flexion_extension_samples = [-53,-15,15, 47]
right_wrist_side_adduction_abduction_samples = [-40,0, 30]
left_wrist_side_adduction_abduction_samples = [-40,0, 30]
right_wrist_rotation_samples = [-90,0, 90]
left_wrist_rotation_samples = [-90,0, 90]
wrist_sample = []
for i in right_wrist_flexion_extension_samples:
    for j in left_wrist_flexion_extension_samples:
        for k in right_wrist_side_adduction_abduction_samples:
            for l in left_wrist_side_adduction_abduction_samples:
                for m in right_wrist_rotation_samples:
                    for n in left_wrist_rotation_samples:
                        m_wrist = REBA_wrist.WristREBA([i, j,k,l,m,n])
                        wrist_sample.append([i, j,k,l,m,n, m_wrist.wrist_reba_score()])

# m_REBA = REBA.partial_to_total_REBA([neck_sample[0][len(neck_sample[0])-1],
#                                      trunk_sample[0][len(trunk_sample[0])-1],
#                                      leg_sample[0][len(leg_sample[0])-1],
#                                      UA_sample[0][len(UA_sample[0])-1],
#                                      LA_sample[0][len(LA_sample[0])-1],
#                                      wrist_sample[0][len(wrist_sample[0])-1]])
# print(m_REBA.find_total_REBA())




np.random.seed(42)
#neck_learning_model()
print(neck_model_test())



    
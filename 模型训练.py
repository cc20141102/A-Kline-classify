import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.utils import shuffle
import time
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dropout
from tensorflow.keras import regularizers

def load_data_from_folder(folder, label, data_list, labels_list):
    for file in os.listdir(folder):
        if file.endswith(".xlsx"):
            
            file_path = os.path.join(folder, file)
            data = pd.read_excel(file_path).loc[:, ["open", "high", "low", "close","percent", "turnoverrate", "active_buy_volume", "active_sell_volume", "un_active_buy_Volume", "un_active_sell_volume"]]
            data = data.apply(lambda x: x / x.max(), axis=0)
            array = data.values
            data_list.append(array)
            labels_list.append(label)
            del data

folders = ["1", "-1", "0"]
labels_mapping = {"1": 2, "-1": 0, "0": 1}
data_list = []
labels_list = []
time1 = time.time()
print(time1)
for folder in folders:
    label = labels_mapping[folder]
    load_data_from_folder(folder, label, data_list, labels_list)
print(time.time()-time1)

data = np.array(data_list)
labels = np.array(labels_list)

print(data.shape)
print(labels.shape)


# 将标签转换为one-hot编码形式
labels = tf.keras.utils.to_categorical(labels, num_classes=3)

# 将数据集划分为训练集和测试集
train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.3, random_state=42)

# 对训练集进行随机打乱
train_data, train_labels = shuffle(train_data, train_labels)


model = Sequential()
model.add(LSTM(32, input_shape=(10, 10)))
model.add(Dense(16, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(3, activation='softmax'))


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 每隔10个 epoch 就保存模型
checkpoint = ModelCheckpoint('lstm_model.h5', monitor='val_accuracy', save_best_only=True, period=10)

# 训练模型
epochs = 200
batch_size = 16
history = model.fit(train_data, train_labels, epochs=epochs, batch_size=batch_size, validation_data=(test_data, test_labels), callbacks=[checkpoint])

# 评估模型
loss, accuracy = model.evaluate(test_data, test_labels)
print('Loss: ', loss)
print('Accuracy: ', accuracy)

# 如果测试集准确率达到要求，则保存模型
if accuracy >= 0.9:
    model.save('lstm_model.h5')
    print("模型保存成功！")
else:
    print("测试集准确率未达到要求，模型未保存。")
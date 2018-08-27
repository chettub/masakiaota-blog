import os
import keras
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.callbacks import TensorBoard
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np


def lenet(input_shape, num_classes):
    """
    http://tecmemo.wpblog.jp/wp-content/uploads/2017/03/dl_lenet-01.png この表を参考に一部活性化関数を変更してLenetを定義
    """
    model = Sequential()

    # フィルターを6枚用意, 小窓のサイズ5×5, paddingによって入力と出力の画像サイズは同じ
    model.add(Conv2D(
        6, kernel_size=5, padding="same",
        input_shape=input_shape, activation="relu",
        init="he_uniform"
    ))
    # 2, 2でマックスプーリング
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 再度畳み込み、深い層ほどフィルターを増やすのはテクニック
    model.add(Conv2D(16, kernel_size=5, padding="same",
                     activation="relu", init="he_uniform"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # Flatten()はマトリックスを1次元ベクトルに変換する層
    # FCにつなぐために必要
    model.add(Flatten())
    model.add(Dense(120, activation="relu", init="he_normal"))
    model.add(Dense(64, activation="relu", init="he_normal"))
    model.add(Dense(num_classes, init="he_normal"))
    model.add(Activation("softmax"))
    model.summary()
    return model


# acquire the .csv name
TRAINS = list(Path("./data/train/").glob("*.csv"))
y = pd.read_csv("./data/target.csv", header=None).iloc[:, 1].values
# split test
X_train, X_test, y_train, y_test = train_test_split(
    TRAINS, y, test_size=0.1, random_state=42)
# onehot
Y_train, Y_test = keras.utils.to_categorical(
    y_train, 10), keras.utils.to_categorical(y_test, 10)


def get_batch(batch_size):
    """
    batchを取得する関数
    """
    global X_train, Y_train
    SIZE = len(X_train)
    # n_batchs
    n_batchs = SIZE//batch_size
    # for でyield
    i = 0
    while (i < n_batchs):
        print("doing", i, "/", n_batchs)
        Y_batch = Y_train[(i * n_batchs):(i * n_batchs + batch_size)]
        X_batch_name = X_train[(i * n_batchs):(i * n_batchs + batch_size)]
        X_batch = np.array([np.loadtxt(file)
                            for file in X_batch_name]).reshape(batch_size, 28, 28, 1)
        # これで(batch_size, 28, 28, 1)のtrainのテンソルが作られる
        i += 1
        yield X_batch, Y_batch


# またtestに関してはデータが十分少ない(メモリに乗る)と仮定して、取得しておく
print("loading X_test...")
X_test = np.array([np.loadtxt(file)
                   for file in X_test]).reshape(-1, 28, 28, 1)

model = lenet((28, 28, 1), 10)
model.compile(loss="categorical_crossentropy",
              optimizer=Adam(),
              metrics=["accuracy"])
N_EPOCHS = 5
for epoch in range(N_EPOCHS):
    print("=" * 50)
    print(epoch, "/", N_EPOCHS)
    acc = []
    for X_batch, Y_batch in get_batch(1000):
        model.train_on_batch(X_batch, Y_batch)
        score = model.evaluate(X_batch, Y_batch)
        print("batch accuracy:", score[1])
        acc.append(score[1])
    print("Train accuracy", np.mean(acc))
    score = model.evaluate(X_test, Y_test)
    print("Test loss:", score[0])
    print("Test accuracy:", score[1])


"""
引数の名前がinitからkernel_initializerに変わってるみたいで、怒られてる


Using TensorFlow backend.
loading X_test...
train_on_batch.py:27: UserWarning: Update your `Conv2D` call to the Keras 2 API: `Conv2D(6, kernel_size=5, padding="same", input_shape=(28, 28, 1..., activation="relu", kernel_initializer="he_uniform")`
  init="he_uniform"
train_on_batch.py:33: UserWarning: Update your `Conv2D` call to the Keras 2 API: `Conv2D(16, kernel_size=5, padding="same", activation="relu", kernel_initializer="he_uniform")`
  activation="relu", init="he_uniform"))
train_on_batch.py:38: UserWarning: Update your `Dense` call to the Keras 2 API: `Dense(120, activation="relu", kernel_initializer="he_normal")`
  model.add(Dense(120, activation="relu", init="he_normal"))
train_on_batch.py:39: UserWarning: Update your `Dense` call to the Keras 2 API: `Dense(64, activation="relu", kernel_initializer="he_normal")`
  model.add(Dense(64, activation="relu", init="he_normal"))
train_on_batch.py:40: UserWarning: Update your `Dense` call to the Keras 2 API: `Dense(10, kernel_initializer="he_normal")`
  model.add(Dense(num_classes, init="he_normal"))
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
conv2d_1 (Conv2D)            (None, 28, 28, 6)         156
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 14, 14, 6)         0
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 14, 14, 16)        2416
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 7, 7, 16)          0
_________________________________________________________________
flatten_1 (Flatten)          (None, 784)               0
_________________________________________________________________
dense_1 (Dense)              (None, 120)               94200
_________________________________________________________________
dense_2 (Dense)              (None, 64)                7744
_________________________________________________________________
dense_3 (Dense)              (None, 10)                650
_________________________________________________________________
activation_1 (Activation)    (None, 10)                0
=================================================================
Total params: 105,166
Trainable params: 105,166
Non-trainable params: 0
_________________________________________________________________
==================================================
0 / 5
doing 0 / 37
1000/1000 [==============================] - 0s 381us/step
batch accuracy: 0.07
doing 1 / 37
1000/1000 [==============================] - 0s 263us/step
batch accuracy: 0.156
doing 2 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.18
doing 3 / 37
1000/1000 [==============================] - 0s 280us/step
batch accuracy: 0.228
doing 4 / 37
1000/1000 [==============================] - 0s 294us/step
batch accuracy: 0.321
doing 5 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.436
doing 6 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 0.534
doing 7 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.594
doing 8 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.622
doing 9 / 37
1000/1000 [==============================] - 0s 286us/step
batch accuracy: 0.642
doing 10 / 37
1000/1000 [==============================] - 0s 263us/step
batch accuracy: 0.667
doing 11 / 37
1000/1000 [==============================] - 0s 267us/step
batch accuracy: 0.685
doing 12 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 0.709
doing 13 / 37
1000/1000 [==============================] - 0s 291us/step
batch accuracy: 0.733
doing 14 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.757
doing 15 / 37
1000/1000 [==============================] - 0s 276us/step
batch accuracy: 0.786
doing 16 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.802
doing 17 / 37
1000/1000 [==============================] - 0s 268us/step
batch accuracy: 0.819
doing 18 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.828
doing 19 / 37
1000/1000 [==============================] - 0s 257us/step
batch accuracy: 0.83
doing 20 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.847
doing 21 / 37
1000/1000 [==============================] - 0s 286us/step
batch accuracy: 0.857
doing 22 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.86
doing 23 / 37
1000/1000 [==============================] - 0s 277us/step
batch accuracy: 0.869
doing 24 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.876
doing 25 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.889
doing 26 / 37
1000/1000 [==============================] - 0s 362us/step
batch accuracy: 0.897
doing 27 / 37
1000/1000 [==============================] - 0s 270us/step
batch accuracy: 0.903
doing 28 / 37
1000/1000 [==============================] - 0s 263us/step
batch accuracy: 0.911
doing 29 / 37
1000/1000 [==============================] - 0s 263us/step
batch accuracy: 0.903
doing 30 / 37
1000/1000 [==============================] - 0s 290us/step
batch accuracy: 0.896
doing 31 / 37
1000/1000 [==============================] - 0s 263us/step
batch accuracy: 0.903
doing 32 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.913
doing 33 / 37
1000/1000 [==============================] - 0s 267us/step
batch accuracy: 0.918
doing 34 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.919
doing 35 / 37
1000/1000 [==============================] - 0s 278us/step
batch accuracy: 0.924
doing 36 / 37
1000/1000 [==============================] - 0s 298us/step
batch accuracy: 0.927
Train accuracy 0.7192162162162162
4200/4200 [==============================] - 1s 275us/step
Test loss: 0.3723116356134415
Test accuracy: 0.8942857142857142
==================================================
1 / 5
doing 0 / 37
1000/1000 [==============================] - 0s 285us/step
batch accuracy: 0.905
doing 1 / 37
1000/1000 [==============================] - 0s 282us/step
batch accuracy: 0.905
doing 2 / 37
1000/1000 [==============================] - 0s 307us/step
batch accuracy: 0.912
doing 3 / 37
1000/1000 [==============================] - 0s 279us/step
batch accuracy: 0.919
doing 4 / 37
1000/1000 [==============================] - 0s 263us/step
batch accuracy: 0.922
doing 5 / 37
1000/1000 [==============================] - 0s 267us/step
batch accuracy: 0.921
doing 6 / 37
1000/1000 [==============================] - 0s 267us/step
batch accuracy: 0.937
doing 7 / 37
1000/1000 [==============================] - 0s 260us/step
batch accuracy: 0.932
doing 8 / 37
1000/1000 [==============================] - 0s 279us/step
batch accuracy: 0.937
doing 9 / 37
1000/1000 [==============================] - 0s 272us/step
batch accuracy: 0.941
doing 10 / 37
1000/1000 [==============================] - 0s 287us/step
batch accuracy: 0.948
doing 11 / 37
1000/1000 [==============================] - 0s 303us/step
batch accuracy: 0.954
doing 12 / 37
1000/1000 [==============================] - 0s 285us/step
batch accuracy: 0.959
doing 13 / 37
1000/1000 [==============================] - 0s 271us/step
batch accuracy: 0.961
doing 14 / 37
1000/1000 [==============================] - 0s 287us/step
batch accuracy: 0.962
doing 15 / 37
1000/1000 [==============================] - 0s 273us/step
batch accuracy: 0.968
doing 16 / 37
1000/1000 [==============================] - 0s 257us/step
batch accuracy: 0.971
doing 17 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.977
doing 18 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.976
doing 19 / 37
1000/1000 [==============================] - 0s 258us/step
batch accuracy: 0.97
doing 20 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.972
doing 21 / 37
1000/1000 [==============================] - 0s 279us/step
batch accuracy: 0.972
doing 22 / 37
1000/1000 [==============================] - 0s 300us/step
batch accuracy: 0.972
doing 23 / 37
1000/1000 [==============================] - 0s 299us/step
batch accuracy: 0.976
doing 24 / 37
1000/1000 [==============================] - 0s 275us/step
batch accuracy: 0.977
doing 25 / 37
1000/1000 [==============================] - 0s 257us/step
batch accuracy: 0.976
doing 26 / 37
1000/1000 [==============================] - 0s 255us/step
batch accuracy: 0.977
doing 27 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 0.979
doing 28 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.978
doing 29 / 37
1000/1000 [==============================] - 0s 273us/step
batch accuracy: 0.982
doing 30 / 37
1000/1000 [==============================] - 0s 295us/step
batch accuracy: 0.979
doing 31 / 37
1000/1000 [==============================] - 0s 299us/step
batch accuracy: 0.982
doing 32 / 37
1000/1000 [==============================] - 0s 298us/step
batch accuracy: 0.979
doing 33 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.979
doing 34 / 37
1000/1000 [==============================] - 0s 257us/step
batch accuracy: 0.976
doing 35 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.976
doing 36 / 37
1000/1000 [==============================] - 0s 263us/step
batch accuracy: 0.98
Train accuracy 0.9591621621621621
4200/4200 [==============================] - 1s 268us/step
Test loss: 0.23688280346315532
Test accuracy: 0.9276190476190476
==================================================
2 / 5
doing 0 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 0.97
doing 1 / 37
1000/1000 [==============================] - 0s 328us/step
batch accuracy: 0.968
doing 2 / 37
1000/1000 [==============================] - 0s 312us/step
batch accuracy: 0.973
doing 3 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.974
doing 4 / 37
1000/1000 [==============================] - 0s 280us/step
batch accuracy: 0.972
doing 5 / 37
1000/1000 [==============================] - 0s 291us/step
batch accuracy: 0.975
doing 6 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.98
doing 7 / 37
1000/1000 [==============================] - 0s 267us/step
batch accuracy: 0.985
doing 8 / 37
1000/1000 [==============================] - 0s 268us/step
batch accuracy: 0.988
doing 9 / 37
1000/1000 [==============================] - 0s 277us/step
batch accuracy: 0.99
doing 10 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.99
doing 11 / 37
1000/1000 [==============================] - 0s 270us/step
batch accuracy: 0.992
doing 12 / 37
1000/1000 [==============================] - 0s 270us/step
batch accuracy: 0.998
doing 13 / 37
1000/1000 [==============================] - 0s 263us/step
batch accuracy: 0.997
doing 14 / 37
1000/1000 [==============================] - 0s 267us/step
batch accuracy: 0.997
doing 15 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.997
doing 16 / 37
1000/1000 [==============================] - 0s 273us/step
batch accuracy: 0.998
doing 17 / 37
1000/1000 [==============================] - 0s 270us/step
batch accuracy: 0.998
doing 18 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.997
doing 19 / 37
1000/1000 [==============================] - 0s 268us/step
batch accuracy: 0.997
doing 20 / 37
1000/1000 [==============================] - 0s 271us/step
batch accuracy: 0.997
doing 21 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.998
doing 22 / 37
1000/1000 [==============================] - 0s 259us/step
batch accuracy: 0.999
doing 23 / 37
1000/1000 [==============================] - 0s 258us/step
batch accuracy: 0.999
doing 24 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.998
doing 25 / 37
1000/1000 [==============================] - 0s 349us/step
batch accuracy: 0.997
doing 26 / 37
1000/1000 [==============================] - 0s 407us/step
batch accuracy: 0.997
doing 27 / 37
1000/1000 [==============================] - 0s 277us/step
batch accuracy: 0.997
doing 28 / 37
1000/1000 [==============================] - 0s 328us/step
batch accuracy: 0.997
doing 29 / 37
1000/1000 [==============================] - 0s 425us/step
batch accuracy: 0.997
doing 30 / 37
1000/1000 [==============================] - 0s 350us/step
batch accuracy: 0.995
doing 31 / 37
1000/1000 [==============================] - 0s 299us/step
batch accuracy: 0.995
doing 32 / 37
1000/1000 [==============================] - 0s 316us/step
batch accuracy: 0.996
doing 33 / 37
1000/1000 [==============================] - 0s 335us/step
batch accuracy: 0.992
doing 34 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.992
doing 35 / 37
1000/1000 [==============================] - 0s 319us/step
batch accuracy: 0.99
doing 36 / 37
1000/1000 [==============================] - 0s 294us/step
batch accuracy: 0.989
Train accuracy 0.9908378378378376
4200/4200 [==============================] - 1s 290us/step
Test loss: 0.21162862170487642
Test accuracy: 0.939047619047619
==================================================
3 / 5
doing 0 / 37
1000/1000 [==============================] - 0s 272us/step
batch accuracy: 0.99
doing 1 / 37
1000/1000 [==============================] - 0s 271us/step
batch accuracy: 0.986
doing 2 / 37
1000/1000 [==============================] - 0s 272us/step
batch accuracy: 0.989
doing 3 / 37
1000/1000 [==============================] - 0s 262us/step
batch accuracy: 0.993
doing 4 / 37
1000/1000 [==============================] - 0s 268us/step
batch accuracy: 0.997
doing 5 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.999
doing 6 / 37
1000/1000 [==============================] - 0s 269us/step
batch accuracy: 0.999
doing 7 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 0.999
doing 8 / 37
1000/1000 [==============================] - 0s 308us/step
batch accuracy: 0.999
doing 9 / 37
1000/1000 [==============================] - 0s 267us/step
batch accuracy: 0.999
doing 10 / 37
1000/1000 [==============================] - 0s 279us/step
batch accuracy: 0.999
doing 11 / 37
1000/1000 [==============================] - 0s 266us/step
batch accuracy: 0.999
doing 12 / 37
1000/1000 [==============================] - 0s 296us/step
batch accuracy: 0.999
doing 13 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 0.999
doing 14 / 37
1000/1000 [==============================] - 0s 297us/step
batch accuracy: 0.999
doing 15 / 37
1000/1000 [==============================] - 0s 290us/step
batch accuracy: 0.999
doing 16 / 37
1000/1000 [==============================] - 0s 294us/step
batch accuracy: 1.0
doing 17 / 37
1000/1000 [==============================] - 0s 299us/step
batch accuracy: 1.0
doing 18 / 37
1000/1000 [==============================] - 0s 305us/step
batch accuracy: 1.0
doing 19 / 37
1000/1000 [==============================] - 0s 312us/step
batch accuracy: 1.0
doing 20 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 1.0
doing 21 / 37
1000/1000 [==============================] - 0s 351us/step
batch accuracy: 1.0
doing 22 / 37
1000/1000 [==============================] - 0s 288us/step
batch accuracy: 1.0
doing 23 / 37
1000/1000 [==============================] - 0s 278us/step
batch accuracy: 1.0
doing 24 / 37
1000/1000 [==============================] - 0s 346us/step
batch accuracy: 1.0
doing 25 / 37
1000/1000 [==============================] - 0s 338us/step
batch accuracy: 1.0
doing 26 / 37
1000/1000 [==============================] - 0s 351us/step
batch accuracy: 1.0
doing 27 / 37
1000/1000 [==============================] - 0s 270us/step
batch accuracy: 1.0
doing 28 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 1.0
doing 29 / 37
1000/1000 [==============================] - 0s 346us/step
batch accuracy: 1.0
doing 30 / 37
1000/1000 [==============================] - 0s 328us/step
batch accuracy: 0.998
doing 31 / 37
1000/1000 [==============================] - 0s 357us/step
batch accuracy: 0.999
doing 32 / 37
1000/1000 [==============================] - 0s 273us/step
batch accuracy: 0.999
doing 33 / 37
1000/1000 [==============================] - 0s 270us/step
batch accuracy: 0.996
doing 34 / 37
1000/1000 [==============================] - 0s 275us/step
batch accuracy: 0.995
doing 35 / 37
1000/1000 [==============================] - 0s 267us/step
batch accuracy: 0.995
doing 36 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.994
Train accuracy 0.9978378378378379
4200/4200 [==============================] - 1s 262us/step
Test loss: 0.21339615402255385
Test accuracy: 0.9414285714285714
==================================================
4 / 5
doing 0 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.994
doing 1 / 37
1000/1000 [==============================] - 0s 273us/step
batch accuracy: 0.996
doing 2 / 37
1000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.998
doing 3 / 37
1000/1000 [==============================] - 0s 265us/step
batch accuracy: 0.999
doing 4 / 37
1000/1000 [==============================] - 0s 299us/step
batch accuracy: 1.0
doing 5 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 281us/step
batch accuracy: 1.0
doing 6 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 288us/step
batch accuracy: 1.0
doing 7 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 01000/1000 [==============================] - 0s 273us/step
batch accuracy: 1.0
doing 8 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 272us/step
batch accuracy: 1.0
doing 9 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 640/1000 [==================>...........] - ETA: 0 832/1000 [=======================>......] - ETA: 01000/1000 [==============================] - 0s 265us/step
batch accuracy: 1.0
doing 10 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 01000/1000 [==============================] - 0s 266us/step
batch accuracy: 1.0
doing 11 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 284us/step
batch accuracy: 1.0
doing 12 / 37
  32/1000 [..............................] - ETA: 0 256/1000 [======>.......................] - ETA: 0 448/1000 [============>.................] - ETA: 0 672/1000 [===================>..........] - ETA: 0 896/1000 [=========================>....] - ETA: 01000/1000 [==============================] - 0s 263us/step
batch accuracy: 1.0
doing 13 / 37
  32/1000 [..............................] - ETA: 0 256/1000 [======>.......................] - ETA: 0 480/1000 [=============>................] - ETA: 0 704/1000 [====================>.........] - ETA: 0 896/1000 [=========================>....] - ETA: 01000/1000 [==============================] - 0s 264us/step
batch accuracy: 0.999
doing 14 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 286us/step
batch accuracy: 1.0
doing 15 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 672/1000 [===================>..........] - ETA: 0 896/1000 [=========================>....] - ETA: 01000/1000 [==============================] - 0s 263us/step
batch accuracy: 1.0
doing 16 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 290us/step
batch accuracy: 1.0
doing 17 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 268us/step
batch accuracy: 1.0
doing 18 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 269us/step
batch accuracy: 1.0
doing 19 / 37
  32/1000 [..............................] - ETA: 0 256/1000 [======>.......................] - ETA: 0 480/1000 [=============>................] - ETA: 0 704/1000 [====================>.........] - ETA: 0 928/1000 [==========================>...] - ETA: 01000/1000 [==============================] - 0s 262us/step
batch accuracy: 1.0
doing 20 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 672/1000 [===================>..........] - ETA: 0 864/1000 [========================>.....] - ETA: 01000/1000 [==============================] - 0s 280us/step
batch accuracy: 1.0
doing 21 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 640/1000 [==================>...........] - ETA: 0 832/1000 [=======================>......] - ETA: 01000/1000 [==============================] - 0s 266us/step
batch accuracy: 1.0
doing 22 / 37
  32/1000 [..............................] - ETA: 0 256/1000 [======>.......................] - ETA: 0 480/1000 [=============>................] - ETA: 0 704/1000 [====================>.........] - ETA: 0 928/1000 [==========================>...] - ETA: 01000/1000 [==============================] - 0s 256us/step
batch accuracy: 1.0
doing 23 / 37
  32/1000 [..............................] - ETA: 0 256/1000 [======>.......................] - ETA: 0 480/1000 [=============>................] - ETA: 0 704/1000 [====================>.........] - ETA: 0 928/1000 [==========================>...] - ETA: 01000/1000 [==============================] - 0s 261us/step
batch accuracy: 1.0
doing 24 / 37
  32/1000 [..............................] - ETA: 0 256/1000 [======>.......................] - ETA: 0 448/1000 [============>.................] - ETA: 0 640/1000 [==================>...........] - ETA: 0 864/1000 [========================>.....] - ETA: 01000/1000 [==============================] - 0s 264us/step
batch accuracy: 1.0
doing 25 / 37
  32/1000 [..............................] - ETA: 0 256/1000 [======>.......................] - ETA: 0 480/1000 [=============>................] - ETA: 0 704/1000 [====================>.........] - ETA: 0 928/1000 [==========================>...] - ETA: 01000/1000 [==============================] - 0s 256us/step
batch accuracy: 1.0
doing 26 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 960/1000 [===========================>..] - ETA: 01000/1000 [==============================] - 0s 293us/step
batch accuracy: 1.0
doing 27 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 672/1000 [===================>..........] - ETA: 0 864/1000 [========================>.....] - ETA: 01000/1000 [==============================] - 0s 263us/step
batch accuracy: 1.0
doing 28 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 672/1000 [===================>..........] - ETA: 0 864/1000 [========================>.....] - ETA: 01000/1000 [==============================] - 0s 263us/step
batch accuracy: 1.0
doing 29 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 672/1000 [===================>..........] - ETA: 0 896/1000 [=========================>....] - ETA: 01000/1000 [==============================] - 0s 262us/step
batch accuracy: 1.0
doing 30 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 384/1000 [==========>...................] - ETA: 0 576/1000 [================>.............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 281us/step
batch accuracy: 1.0
doing 31 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 640/1000 [==================>...........] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 281us/step
batch accuracy: 1.0
doing 32 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 384/1000 [==========>...................] - ETA: 0 544/1000 [===============>..............] - ETA: 0 736/1000 [=====================>........] - ETA: 0 928/1000 [==========================>...] - ETA: 01000/1000 [==============================] - 0s 305us/step
batch accuracy: 1.0
doing 33 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 608/1000 [=================>............] - ETA: 0 800/1000 [=======================>......] - ETA: 0 992/1000 [============================>.] - ETA: 01000/1000 [==============================] - 0s 285us/step
batch accuracy: 0.997
doing 34 / 37
  32/1000 [..............................] - ETA: 0 256/1000 [======>.......................] - ETA: 0 448/1000 [============>.................] - ETA: 0 640/1000 [==================>...........] - ETA: 0 832/1000 [=======================>......] - ETA: 01000/1000 [==============================] - 0s 284us/step
batch accuracy: 0.998
doing 35 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 416/1000 [===========>..................] - ETA: 0 576/1000 [================>.............] - ETA: 0 768/1000 [======================>.......] - ETA: 0 960/1000 [===========================>..] - ETA: 01000/1000 [==============================] - 0s 298us/step
batch accuracy: 0.999
doing 36 / 37
  32/1000 [..............................] - ETA: 0 224/1000 [=====>........................] - ETA: 0 448/1000 [============>.................] - ETA: 0 640/1000 [==================>...........] - ETA: 0 864/1000 [========================>.....] - ETA: 01000/1000 [==============================] - 0s 265us/step
batch accuracy: 0.997
Train accuracy 0.9993783783783785
  32/4200 [..............................] - ETA: 1 224/4200 [>.............................] - ETA: 1 448/4200 [==>...........................] - ETA: 0 672/4200 [===>..........................] - ETA: 0 864/4200 [=====>........................] - ETA: 01056/4200 [======>.......................] - ETA: 01248/4200 [=======>......................] - ETA: 01440/4200 [=========>....................] - ETA: 01632/4200 [==========>...................] - ETA: 01824/4200 [============>.................] - ETA: 01984/4200 [=============>................] - ETA: 02176/4200 [==============>...............] - ETA: 02336/4200 [===============>..............] - ETA: 02496/4200 [================>.............] - ETA: 02688/4200 [==================>...........] - ETA: 02880/4200 [===================>..........] - ETA: 03072/4200 [====================>.........] - ETA: 03296/4200 [======================>.......] - ETA: 03520/4200 [========================>.....] - ETA: 03712/4200 [=========================>....] - ETA: 03904/4200 [==========================>...] - ETA: 04096/4200 [============================>.] - ETA: 04200/4200 [==============================] - 1s 279us/step
Test loss: 0.21080376681339527
Test accuracy: 0.9454761904761905
"""

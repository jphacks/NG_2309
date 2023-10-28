from tensorflow.keras.layers import LSTM, Dense
import tensorflow as tf
import numpy as np
from tqdm import tqdm

class AnomalousDetector(tf.keras.Model):

    def __init__(self):
        super(AnomalousDetector, self).__init__()
        self.output_node = 10
        self.hidden_1 = 15
        self.dense = Dense(self.hidden_1, activation="relu")
        self.lstm_1 = LSTM(self.output_node, return_sequences=True)
        self.lstm_2 = LSTM(self.output_node, return_sequences=True)
        self.lstm_3 = LSTM(self.output_node, return_sequences=True)


    def call(self,x):
        output = self.dense(x)
        output = tf.reshape(output, (-1,1,15))
        output_1 = self.lstm_1(output)
        output_2 = self.lstm_1(output)
        output_3 = self.lstm_1(output)

        return output_1, output_2, output_3
    
def loss_func(y, pred_y):
    ls = []
    for _ in range(len(pred_y)):
        ls.append(tf.subtract(y,pred_y)**2)
    loss_tensor = ls[0]
    for i in range(len(pred_y)):
        loss_tensor = tf.math.maximum(loss_tensor,ls[i])
    loss = tf.reduce_mean(loss_tensor)

    return loss
    
@tf.function
def train_step(x, y, model:AnomalousDetector, optimizer:tf.keras.optimizers.Adam):

    loss = 0
    
    with tf.GradientTape() as tape:

        output_1, output_2, output_3 = model(x, training=True)
        vae_loss = loss_func(y, (output_1, output_2, output_3))
        loss += vae_loss
        
    batch_loss = loss / len(x)
    variables = model.trainable_variables
    gradients = tape.gradient(loss, variables)
    optimizer.apply_gradients(zip(gradients, variables))

    return batch_loss


    
def model_create(X,Y):

    optimizer = tf.keras.optimizers.Adam(beta_1=0.9, beta_2=0.98, 
                                        epsilon=1e-9)
    
    BATCH_SIZE= 3

    train_X, train_Y = X[:-1], Y[:-1]
    test_X, test_Y = X[-1:], Y[-1:]

    model = AnomalousDetector()

    train_dataset = tf.data.Dataset.from_tensor_slices((train_X, train_Y))
    train_dataset = train_dataset.batch(BATCH_SIZE, drop_remainder=True)

    EPOCHS = 10
    for epoch in tqdm(range(EPOCHS)):

        for x_train, y_train in train_dataset:
            
            batch_loss = train_step(x_train, y_train, model, optimizer)

        print('Epoch {} Loss {}'.format(epoch + 1, batch_loss.numpy()))

    return model.predict(test_X), test_Y


if __name__ == "__main__":
    X = np.random.uniform(0,1,size=(12,20))
    Y = np.random.uniform(0,1,size=(12,10))
    pred, ans = model_create(X,Y)
    print(pred, ans)
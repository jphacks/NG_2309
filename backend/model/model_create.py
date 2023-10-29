from tensorflow.keras.layers import LSTM, Dense
import tensorflow as tf
import numpy as np
from tqdm import tqdm
import scipy.stats as stats

class AnomalousDetector(tf.keras.Model):

    def __init__(self):
        super(AnomalousDetector, self).__init__()
        self.output_node = 10
        self.hidden_1 = 20
        self.hidden_2 = 15
        self.dense_1 = Dense(self.hidden_1, activation="relu", kernel_initializer=tf.keras.initializers.RandomNormal())
        self.dense_2 = Dense(self.hidden_2, activation="relu", kernel_initializer=tf.keras.initializers.RandomNormal())
        self.lstm_1 = LSTM(self.output_node, return_sequences=True, kernel_initializer=tf.keras.initializers.RandomNormal())
        self.lstm_2 = LSTM(self.output_node, return_sequences=True, kernel_initializer=tf.keras.initializers.RandomNormal())
        self.lstm_3 = LSTM(self.output_node, return_sequences=True, kernel_initializer=tf.keras.initializers.RandomNormal())


    def call(self,x):
        output = self.dense_1(x)
        output = self.dense_2(output)
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
    test_dataset = tf.data.Dataset.from_tensor_slices((test_X, test_Y))
    train_dataset = train_dataset.batch(BATCH_SIZE, drop_remainder=True)

    EPOCHS = 100
    for epoch in tqdm(range(EPOCHS)):

        for x_train, y_train in train_dataset:
            
            batch_loss = train_step(x_train, y_train, model, optimizer)

        print('Epoch {} Loss {}'.format(epoch + 1, batch_loss.numpy()))

    return model


def create_s_t(y, pred_y):

    ls = []

    for i in range(len(y)):
        max_array = (np.array(y[i]) - np.array(pred_y[0][i]))**2
        for j in range(len(pred_y)):
            max_array = np.maximum((np.array(y[i]) - np.array(pred_y[j][i]))**2, max_array)
        ls.append(np.median(max_array))

    return np.array(ls)


def anomalous_percent(model:AnomalousDetector, data):
    
    in_window = 20
    out_window = 10
    end = 360

    X = tf.constant([data[i:i+in_window] for i in range(end - in_window - out_window)])
    Y = tf.constant([data[i:i+out_window] for i in range(in_window, end - out_window)])

    output_1, output_2, output_3 = model.predict(X)
    s_t = create_s_t(Y, (output_1, output_2, output_3))

    sigma = s_t.std()

    mean = s_t.mean()

    r_t = (s_t - mean) / sigma

    result = max(r_t[-10:])

    percentage = stats.norm.cdf(result, loc=mean, scale=1) * 100

    return percentage

def calculate_anmalous_percent(X, Y, data):
    X_array = np.array(X, dtype=np.float64)
    Y_array = np.array(Y, dtype=np.float64)
    model_instance = model_create(X_array,Y_array)
    return anomalous_percent(model_instance, np.array(data))


if __name__ == "__main__":
    data = np.random.uniform(0,1,360)
    X = np.zeros((12,20))
    Y = np.zeros((12,10))
    model_instance = model_create(X,Y)
    print(anomalous_percent(model_instance, data))

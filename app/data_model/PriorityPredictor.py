import pandas as pd
import numpy as np

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

class DataSourceAdapter:
    def __init__(self, source_type, source_path):
        self.source_type = source_type
        self.source_path = source_path
    
    def load_data(self):
        if self.source_type == 'json':
            return pd.read_json(self.source_path)
        elif self.source_type == 'csv':
            return pd.read_csv(self.source_path)
        elif self.source_type == 'request':
            return pd.read_csv(self.source_path)
        elif self.source_type == 'database':
            # Assuming source_path is a SQLite database file
           # conn = sqlite3.connect(self.source_path)
           # query = "SELECT * FROM your_table_name"  # Modify as needed
            # df = pd.read_sql(query, conn)
            # conn.close()
            # return df
            pass
        else:
            raise ValueError("Unsupported source type. Choose from 'json', 'csv', or 'database'.")

class DataClasifier:
    def __init__(self, data_adapter, clasifier = None):
        self.data_adapter = data_adapter
        self.clasifier = clasifier
    
    #expected List os dicts: [{atribute1, condition1},{atribute2, condition2}...]
    def filter_data(self, atribute = None, isin = []):  
        df = self.data_adapter.load_data() 
        if not atribute:
            return df
        return df[df[atribute].isin(isin)]
    
    def get_frequency(self, atribute = None):
        if not atribute:
            return ("there is not atribute selected")
        df = self.data_adapter.load_data()
        frequency = df[atribute].value_counts().to_dict()
        return frequency
    
    def get_ratio(self, atribute = None):
        if not atribute:
            return ("there is not atribute selected")
        df = self.data_adapter.load_data()
        frequency = df[atribute].value_counts()
        ratio = frequency / frequency.sum()
        ratio_dict = ratio.to_dict()
        return ratio_dict


class PriorityPredictor:
    def __init__(self, data_adapter, model = None):
        self.data_adapter = data_adapter
        self.model = model
        self.scaler = StandardScaler()

    def load_data(self):
        df = self.data_adapter.load_data()
        df['expiresAt'] = pd.to_datetime(df['expiresAt'])
        df['days_to_expire'] = (df['expiresAt'] - datetime.now()).dt.days
        df['depletion_rate'] = df['available'] / np.where(df['SalesRateDay'] > 0, df['SalesRateDay'], 0.1)
        
        X = df[['days_to_expire', 'available', 'price', 'SalesRateDay', 'depletion_rate']]
        y = df['priority']
        y = to_categorical(y, num_classes=5)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Standardize features
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def build_model(self):
        #static variables for now
        self.model = Sequential([
            Dense(200, input_dim=self.X_train.shape[1], activation='linear'),
            Dense(32, activation='relu'),
            Dense(5, activation='softmax')  # 5 output classes
        ])
        
        # Compile the model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def train_model(self, epochs=100, batch_size=32):
        if self.model is None:
            raise ValueError("Model is not built yet. Call 'build_model()' before training.")
        
        self.history = self.model.fit(self.X_train, self.y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=1)
        self.save_model()
    def evaluate_model(self):
        if self.model is None:
            raise ValueError("Model is not built yet. Call 'build_model()' before evaluation.")
        
        loss, accuracy = self.model.evaluate(self.X_test, self.y_test)
        print(f'Loss: {loss:.4f}')
        print(f'Accuracy: {accuracy*100:.2f}%')
        return loss, accuracy

    def make_predictions(self, data):
        if self.model is None:
            raise ValueError("Model is not built yet. Call 'build_model()' before making predictions.")
        df = pd.DataFrame(data)
        df['expiresAt'] = pd.to_datetime(df['expiresAt'])
        df['days_to_expire'] = (df['expiresAt'] - datetime.now()).dt.days
        df['depletion_rate'] = df['available'] / np.where(df['SalesRateDay'] > 0, df['SalesRateDay'], 0.1)
        
        X = df[['days_to_expire', 'available', 'price', 'SalesRateDay', 'depletion_rate']]
        X_scaled = self.scaler.transform(X)

        predictions = self.model.predict(X_scaled)
        predicted_classes = np.argmax(predictions, axis=1)
        
        print(predictions)
        print(predicted_classes)
        return predictions, predicted_classes
    
    def save_model(self,name = 'predictor_model'):
        self.model.save(f'.\\SerializedModels\\{name}.h5')
# import library
import models.data as dataset
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
    
def split_data():
    from sklearn.preprocessing import StandardScaler
    data = dataset.read_data()
    
    X = data[['open_price', 'high', 'low', 'close', 'volume']]
    y = data['signal']
    
    # scaler = StandardScaler()
    # X = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    
    return ( X_train, X_test, y_train, y_test )

def data_uji():
    # X_train, X_test, y_train, y_test = split_data()
    data = dataset.read_data()
    data = data[['open_price', 'high', 'low', 'close', 'volume']]
    
    return data
    
def svm():
    X_train, X_test, y_train, y_test = split_data()
    
    # Inisialisasi model SVM (gunakan kernel dan parameter yang sesuai)
    svm_model = SVR(kernel='poly')

    # Melatih model SVM pada data latih
    svm_model.fit(X_train, y_train)

    # Melakukan prediksi pada data uji
    y_pred = svm_model.predict(X_test)

    # Evaluasi kinerja model
    mse = mean_squared_error(y_test, y_pred)
    
    return {
        "mse": mse,
        # "confussion_matrix": confusion_matrix(y_test, y_pred),
        "svm_model": svm_model
    }

def prediksi(input):
    from sklearn.preprocessing import StandardScaler
    import numpy as np
    
    model = svm()
    model = model['svm_model']
    
    # scaler = StandardScaler()
    # X = scaler.fit_transform(input)
    
    svm_pred = model.predict(input)
    
    # svm_pred = scaler.inverse_transform(pred)
    
    return svm_pred
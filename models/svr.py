# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVR
from datetime import date, timedelta
from sklearn.metrics import mean_absolute_error

def predict_stock_and_signal(n_days, stock_data):
    # Creating a DataFrame from the provided stock data
    df = pd.DataFrame(stock_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    df['Days'] = range(len(df))  # adding a new column in the dataset

    days = [[i] for i in range(len(df))]

    # Splitting the dataset
    X = days
    y = df.close

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

    # We are going to use GridSearchCV method
    # for getting the best parameters for our model
    # first we will provide some parameters as Dict here
    parameters = {
        'C': [0.001, 0.01, 0.1, 1, 100, 1000],
        'epsilon': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10,
                    50, 100, 150, 1000],
        'gamma': [0.0001, 0.001, 0.005, 0.1, 1, 3, 5, 8, 40, 100, 1000]
    }

    # we will use Support Vector Regressor and kernel as Radial Basis Function
    gsc = GridSearchCV(
        estimator=SVR(kernel='rbf'),
        param_grid=parameters,
        cv=10,
        scoring='neg_mean_absolute_error'
    )

    grid_result = gsc.fit(X_train, y_train)

    # storing and using the best parameters
    # best parameters = min error
    best_params = grid_result.best_params_
    svr_model = SVR(kernel='rbf', C=best_params['C'], epsilon=best_params['epsilon'], gamma=best_params['gamma'])
    svr_model.fit(X_train, y_train)

    output_days = []
    for i in range(1, n_days + 1):  # adding n days provided by the user to our dataset
        output_days.append([i + X_test[-1][0]])

    # Making predictions for the next n_days
    predictions = svr_model.predict(output_days)
    
    # Extracting last n_days actual values from y_test
    y_test_last_n_days = y_test.tail(n_days)

    # Calculating MAPE
    mape = mean_absolute_error(y_test_last_n_days, predictions)

    # Calculating the difference between predicted and actual closing prices
    price_difference = predictions[-1] - y_test.tail(1).values[0]

    # Generating Buy/Sell signal based on the price difference
    if price_difference > 0:
        signal = "Beli"
    elif price_difference < 0:
        signal = "Jual"
    else:
        signal = "Tahan"

    # Visualizing the prediction and Buy/Sell signal using pyplot
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, y, label='Actual', marker='o')
    plt.plot(df.index[-1] + timedelta(days=1), predictions[-1], marker='o', color='green', label='Predicted')
    plt.title("Actual and Predicted Close Prices")
    plt.xlabel("Date")
    plt.ylabel("Closed Price")
    plt.legend()
    plt.savefig('./static/assets/plot/pred.png')

    # print(f"Prediction for the next {n_days} days: ${round(predictions[-1], 2)}")
    # print(f"Signal: {signal}")
    
    return {
        "hari": n_days,
        "prediksi": round(predictions[-1], 2),
        "sinyal": signal,
        "mape": mape
    }

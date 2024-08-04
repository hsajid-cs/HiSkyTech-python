from sklearn import linear_model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


Housing = pd.read_csv("Housing.csv")


'''
Housing Columns = ['price', 'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad',
       'guestroom', 'basement', 'hotwaterheating', 'airconditioning',
        'parking', 'prefarea', 'furnishingstatus']

'''

'''
The features of importance are area, bedrooms, bathrooms
The target is price
'''

X = Housing[['area', 'bedrooms', 'bathrooms']]
Y = Housing['price']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.5)

model = linear_model.LinearRegression()
model.fit(x_train, y_train)

y_predict = model.predict(x_test)


print("The model score is: ", model.score(x_test, y_test))

plt.scatter(y_test, y_predict)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4, color='red')
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title('House Price Prediction')
plt.show()


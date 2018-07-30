###############################################################################
# Curso: ANÁLISIS INTELIGENTE DE DATOS EN ENTORNOS DE BIG DATA
# Profesor: Dr. José Ángel Olivas Varela
# Alumno: Lic. Ariel Maiorano
# Mayo de 2018
###############################################################################
# Experimento - entrenamiento y validación con diferentes modelos
###############################################################################
#
# Entrena diferentes modelos con el mismo dataset e imprime los resultados.
#


import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

from keras.models import Sequential
from keras.layers import Dense, TimeDistributed
from keras.layers import LSTM
from keras.wrappers.scikit_learn import KerasClassifier


# archivo de datos
ARCHIVO_CSV = 'dataset.csv'

# nombres de los clasificadores
nombres = [
		"Vecinos más próximos (Nearest Neighbors)",
		"Bayesiano ingenuo (Naive Bayes)",
		"SVM Lineal (Linear SVM)",
		"Árbol de decisión (Decision Tree)",
		"Bosques aleatorios (Random Forest)",
		"Red Neuronal (Neural Network, NN)",
		"NN Recurrente con LSTM (RNN with LSTM)"
	]

# clasificadores
clasificadores = [
		KNeighborsClassifier(3),
		GaussianNB(),
		SVC(kernel="linear", C=0.025),
		DecisionTreeClassifier(max_depth=5),
		RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
	]


# recuperar datos
data = pd.read_csv(ARCHIVO_CSV, sep=',', header=0)

# extraer columen de grupo o clase
y = data.peridodo_maximo
X = data.drop('peridodo_maximo', axis=1)
# normalizar (?)
X = StandardScaler().fit_transform(X)
# separar training set y validation set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
# para lstm...
X_train_lstm = X_train.reshape((-1, 1, 8)) # 8 variables (n, tipo, a, b, ..., h), -1 auto para total
X_test_lstm = X_test.reshape((-1, 1, 8))

# funciones (básicas) para crear modelos de redes para keras, requerida por KerasClassifier
def crear_modelo_nn():
	model = Sequential()
	model.add(Dense(12, input_dim=8, activation='relu'))
	model.add(Dense(8, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
clasificadores.append(KerasClassifier(build_fn=crear_modelo_nn, epochs=500, batch_size=10, verbose=0))
def crear_modelo_rnn_lstm():
	model = Sequential()
	model.add(LSTM(100, input_shape=(1, 8)))
	model.add(Dense(1, activation='sigmoid'))
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
clasificadores.append(KerasClassifier(build_fn=crear_modelo_rnn_lstm, epochs=500, batch_size=10, verbose=0))


# proceso principal
for nombre, clasificador in zip(nombres, clasificadores):
	if 'RNN' in nombre:
		clasificador.fit(X_train_lstm, y_train)
		prediccion = clasificador.predict(X_test_lstm)
	else:
		clasificador.fit(X_train, y_train)
		prediccion = clasificador.predict(X_test)
	score = accuracy_score(y_test, prediccion)
	matriz_confusion = confusion_matrix(y_test, prediccion)	
	reporte = classification_report(y_test, prediccion, target_names=['De período NO máximo', 'De período máximo'])
	print(nombre + ' - score general: ' + str(score))
	print("Matríz de confusión:")	
	print(matriz_confusion)
	print("Reporte de resultados:")
	print(reporte)
	print('###############################################################################')

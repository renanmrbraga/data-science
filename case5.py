# Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from autosklearn

# Carregando o conjunto de dados California Housing
california_housing = fetch_california_housing()

# Criando um DataFrame do pandas com os dados e nomeando as colunas
X = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
# Armazenando a variável target (valor médio das casas)
y = california_housing.target

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=2)


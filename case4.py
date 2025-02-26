# Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from xgboost import XGBRegressor

# Carregando o conjunto de dados California Housing
california_housing = fetch_california_housing()

# Criando um DataFrame do pandas com os dados e nomeando as colunas
X = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
# Armazenando a variável target (valor médio das casas)
y = california_housing.target

# Exibindo as primeiras 5 linhas do DataFrame
print('Dataset Head:')
print(X.head())
print()  # Linha em branco para melhor legibilidade

# Características da casa
print('Dataset Keys:')
print(california_housing.keys())
print()  # Linha em branco para melhor legibilidade

# Descrição detalhada do conjunto de dados
print('Dataset Descrição:')
print(california_housing.DESCR)
print()  # Linha em branco para melhor legibilidade

# Exibindo os valores alvo (valor médio das casas)
print('Exibir target:')
print(y)
print()  # Linha em branco para melhor legibilidade

## Técnicas de Modelagem

# Links para a documentação de três técnicas de regressão diferentes

# 1. Regressão Linear do scikit-learn
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression

# 2. Support Vector Regression do scikit-learn
# https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html#sklearn.svm.SVR

# 3. Decision Tree Regression do XGBoost
# https://xgboost.readthedocs.io/en/stable/python/python_api.html

## Assumptions de Modelagem

## Apenas variáveis numéricas

## Design do Teste

# Divisão do Dataset:
# Separação do dataset em Train/Test com 20% dos dados para teste usando o método train_test_split do scikit-learn.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Métrica de Avaliação do Modelo:
# Validação das métricas MSE e RMSE para penalizar grandes erros de previsão.
# Utilizando a função mean_squared_error do scikit-learn.
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html#sklearn.metrics.mean_squared_error

## Técnica 1. Regressão Linear
regLinear = LinearRegression().fit(X_train, y_train)
yLinear = regLinear.predict(X_test)
MSELinear = mean_squared_error(y_test, yLinear)

print('MSE Linear:')
print(MSELinear)
print()

print('RMSE Linear:')
print(np.sqrt(MSELinear))
print()

## Técnica 2. Support Vector Regression (SVR)
regSVR = SVR().fit(X_train, y_train)
ySVR = regSVR.predict(X_test)
MSESVR = mean_squared_error(y_test, ySVR)

print('MSE SVR:')
print(MSESVR)
print()

print('RMSE SVR:')
print(np.sqrt(MSESVR))
print()

## Técnica 3. Decision Tree Regression (XGBoost)
regXGB = XGBRegressor().fit(X_train, y_train)
yXGB = regXGB.predict(X_test)
MSEXGB = mean_squared_error(y_test, yXGB)

print('MSE XGB:')
print(MSEXGB)
print()

print('RMSE XGB:')
print(np.sqrt(MSEXGB))
print()

# Calculando a média do target
media_target = np.mean(y)
print('Média do target:')
print(media_target)
print()

# Calculando a porcentagem de erro para Regressão Linear
porcentagem_erro_linear = (np.sqrt(MSELinear) / media_target) * 100
print('Porcentagem de Erro Linear:')
print(porcentagem_erro_linear)
print()

# Calculando a porcentagem de erro para SVR
porcentagem_erro_svr = (np.sqrt(MSESVR) / media_target) * 100
print('Porcentagem de Erro SVR:')
print(porcentagem_erro_svr)
print()

# Calculando a porcentagem de erro para XGB
porcentagem_erro_xgb = (np.sqrt(MSEXGB) / media_target) * 100
print('Porcentagem de Erro XGB:')
print(porcentagem_erro_xgb)
print()

# Otimização de hiperparâmetros

# Utilizando o método GridSearchCV do SKLearn
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV

print(regXGB.get_params().keys())
print()

parameters = {
    "max_depth": [5, 6, 7],
    "learning_rate": [0.1, 0.2, 0.3],
    "objective": ['reg:squarederror'],
    "booster": ['gbtree'],
    "n_jobs": [-1],  # Utilizando todos os núcleos disponíveis
    "gamma": [0, 1],
    "min_child_weight": [1, 3],
    "max_delta_step": [0, 1],
    "subsample": [0.5, 1]
}

# GridSearchCV para encontrar os melhores hiperparâmetros
xgbGrid = GridSearchCV(XGBRegressor(), parameters, refit='neg_mean_squared_error', verbose=True)

# Ajustar o modelo usando os melhores hiperparâmetros
xgbGridModel = xgbGrid.fit(X_train, y_train)

# Imprimir os melhores parâmetros encontrados
print('Melhores parâmetros:', xgbGridModel.best_params_)
print()

# Fazer previsões com o modelo ajustado
yGrid = xgbGridModel.predict(X_test)

# Calcular MSE para o modelo ajustado
MSEGrid = mean_squared_error(y_test, yGrid)

print('MSE XGB Grid:', MSEGrid)
print('RMSE XGB Grid:', np.sqrt(MSEGrid))

# Calcular a porcentagem de erro para o modelo ajustado
porcentagem_erro_xgb_grid = (np.sqrt(MSEGrid) / media_target) * 100
print('Porcentagem de Erro XGB Grid:')
print(porcentagem_erro_xgb_grid)
print()

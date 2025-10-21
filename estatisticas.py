import pandas as pd

def calcula_estatisticas(df):

    resultados = {}

    # funcoes sao de primeira ordem em python!!! da pra guardar em estruturas!!
    operacoes = {
        "media": lambda s: round(float(s.mean()), 2),
        "mediana": lambda s: round(float(s.median()), 2),
        "desvio_padrao": lambda s: round(float(s.std()), 2)
    }

    for metrica, func in operacoes.items():
        resultados[metrica] = {}
        
        for especie in ["setosa", "versicolor", "virginica"]:
            subset = df[df["species"] == especie]
            resultados[metrica][especie] = {
                "petal_length": func(subset["petal length (cm)"]),
                "petal_width": func(subset["petal width (cm)"]),
                "sepal_length": func(subset["sepal length (cm)"]),
                "sepal_width": func(subset["sepal width (cm)"])
            }
        
        resultados[metrica]["geral"] = {
            "petal_length": func(df["petal length (cm)"]),
            "petal_width": func(df["petal width (cm)"]),
            "sepal_length": func(df["sepal length (cm)"]),
            "sepal_width": func(df["sepal width (cm)"])
        }

    return resultados
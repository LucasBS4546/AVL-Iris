from avl_tree_iris import AvlTreeIris
from gui import visualize_species_trees
from estatisticas import calcula_estatisticas
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np
from scipy.stats import norm

# Carregar o conjunto Iris
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['species'] = iris.target_names[iris.target]

# Criar arvores AVL para cada especie
avl_setosa = AvlTreeIris()
avl_versicolor = AvlTreeIris()
avl_virginica = AvlTreeIris()

# Dicionario para mapear especies as arvores
species_trees = {
    'setosa': avl_setosa,
    'versicolor': avl_versicolor,
    'virginica': avl_virginica
}

# Inserir dados nas arvores AVL de determinada especie,
# usando determinada metrica (petal_length, sepal_width..)
def inserir_dados(species, metric):
    media_metrica = df[metric].mean()
    valor_mais_proximo, indice_mais_proximo = procura_valor_proximo(media_metrica, df)

    species_trees[species].insert(valor_mais_proximo, indice_mais_proximo)

    for index, row in df.iterrows():
        metric_value = row[metrica]
        species_trees[species].insert(metric_value, index)

# Calcular intervalos de confianca (95%)
def calculate_confidence_interval(data):
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    ci_lower, ci_upper = norm.interval(0.95, loc=mean, scale=std/np.sqrt(len(data)))
    return mean, ci_lower, ci_upper

def testar_intervalo_confianca(campo):
    for species in df['species'].unique():
        species_data = df[df['species'] == species][campo]
        mean, ci_lower, ci_upper = calculate_confidence_interval(species_data)
        print(f"{species}: Media = {mean:.2f}, Intervalo de Confianca (95%) = [{ci_lower:.2f}, {ci_upper:.2f}]")

# Funcao de classificacao
def classify_sample(sample):
    composite_index = calculate_composite_index(sample)
    min_diff = float('inf')
    predicted_species = None
    for species, tree in species_trees.items():
        closest_key, closest_node = tree.find_closest(composite_index)
        if closest_node and abs(closest_key - composite_index) < min_diff:
            min_diff = abs(closest_key - composite_index)
            predicted_species = species
    return predicted_species

def classifica_amostra(dados):
    sample = pd.Series(dados, index=iris.feature_names)
    predicted = classify_sample(sample)
    print(f"Amostra classificada como: {predicted}")

def relatorio():
    # Printa alguns dados no terminal
    for species, tree in species_trees.items():
        print(f"Arvore para {species}: Altura = {tree.height()}, Nos = {tree.size()}")

    # Coleta calculos estatisticos
    dados_estatisticos = calcula_estatisticas(df)

    # Parte de interface visual para visualizar arvores e resultados estatísticos
    visualize_species_trees(species_trees, df, dados_estatisticos)

if __name__ == "__main__":

    # Constroi arvores
    inserir_dados()

    # Intervalo de confianca para comprimento da petala
    testar_intervalo_confianca('petal length (cm)')

    # Classificao de amostra
    classifica_amostra([5.1, 3.5, 1.4, 0.2])

    # Relatorio da estrutura da arvore + dados estatisticos
    relatorio()

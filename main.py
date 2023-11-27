import matplotlib.pyplot as plt
import numpy as np
from kmodes.kmodes import KModes
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA


class DataSet:
    def __init__(self, name: str, categories: dict[str, list[bool]]):
        self.name = name
        self.categories = categories

    def __str__(self):
        return f'{self.name}: {self.categories}'

    def __repr__(self):
        return f'{self.name}: {self.categories}'

    def name_pretty(self) -> str:
        return self.name.replace('_', ' ')


def contains_name_in_data_sets(data_sets: list[DataSet], name: str) -> bool:
    for data_set_ in data_sets:
        if data_set_.name == name:
            return True
    return False


def create_pie_chart(data_set: DataSet):
    # plt.style.use('_mpl-gallery-nogrid')

    # make data
    if len(data_set.categories) != 1:
        x = [sum(data_set.categories[category]) for category in data_set.categories]
        labels = data_set.categories.keys()
    else:
        yes = sum(data_set.categories[list(data_set.categories.keys())[0]])
        no = len(data_set.categories[list(data_set.categories.keys())[0]]) - yes
        x = [yes, no]
        labels = ['Ja', 'Nein']
    colors = plt.get_cmap('Spectral')(np.linspace(0.2, 0.7, len(x)))

    # plot
    fig, ax = plt.subplots()
    ax.bar(labels, x, color=colors)
    ax.set_ylabel('Anzahl Personen')

    plt.suptitle(data_set.name_pretty())
    plt.tight_layout()
    plt.savefig(f'diagrams\\{data_set.name}.png')


if __name__ == '__main__':
    data = open('Umfrage_Ergebnis.csv', 'r')
    lines = data.readlines()
    data.close()
    lines = [line.replace('\n', '') for line in lines]

    array = [line.split(',') for line in lines]

    for line in array[1:]:
        for value in line:
            assert value in ['0', '1']
    categories: dict[str, list[bool]] = {category: [] for category in array[0]}

    for line in array[1:]:
        for i, value in enumerate(line):
            categories[array[0][i]].append(value == '1')

    # for dict_key in categories:
    #    print(dict_key, categories[dict_key])

    set_list: list[DataSet] = []
    for dict_key in categories:
        split = dict_key.split('=')
        name = split[0]
        subcategory = split[1] if len(split) > 1 else name
        if not contains_name_in_data_sets(set_list, name):
            set_list.append(DataSet(name, {subcategory: categories[dict_key]}))

        else:
            for data_set in set_list:
                if data_set.name == name:
                    data_set.categories[subcategory] = categories[dict_key]

    print(set_list)

    dimensions = []
    for s in set_list:
        l = []
        values_list = list(s.categories.values())
        for i in range(len(values_list[0])):
            x = []
            for j in values_list:
                x.append(j[i])

            val = None
            for k in range(len(x)):
                if x[k]:
                    val = k
            if val is None:
                val = -1
            l.append(val)
        dimensions.append(l)

    data = list(d for d in dimensions)
    persons = []
    for i in range(len(data[0])):
        p = []
        for j in range(len(data)):
            p.append(data[j][i])
        persons.append(p)

    print(len(persons))
    print(len(persons[0]))

    persons = np.array([np.array(xi) for xi in persons])
    # np_array = np.array([[1,1,1,1], [5,2,1,1], [1,2,1,1], [10,2,1,1], [4,-1,1,1]]) #np.array([np.array(xi) for xi in data])

    km = KModes(n_clusters=2, init='Huang', n_init=5, verbose=1)

    clusters = km.fit_predict(persons)
    km.labels_ = [i for i in persons]

    # Print the cluster centroids
    print(km.cluster_centroids_)

    # from sklearn.manifold import TSNE

    # tsne = TSNE(n_components=2)  # Choose the number of components
    # reduced_data = tsne.fit_transform(data)

    linkage_data = linkage(persons, method='ward', metric='euclidean')

    print (linkage_data)
    dendrogram(linkage_data)
    plt.tight_layout()
    plt.savefig(f'diagrams\\dendrogram.png')

    hierarchical_cluster = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='ward')
    hierarchical_cluster.fit_predict(persons)
    print(hierarchical_cluster.labels_)

    # for data_set in set_list:
    #    create_pie_chart(data_set)
    # print(array)

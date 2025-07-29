import numpy

class DecisionTreeClassifier:
    def __init__(self, max_depth: int = ..., min_samples_split: int = ..., min_samples_leaf: int = ..., type_function: int = ...) -> None:
        """__init__(self: Tree.DecisionTreeClassifier, max_depth: int = 1000000000, min_samples_split: int = 2, min_samples_leaf: int = 1, type_function: int = 1) -> None
                Создать древовидный классификатор.
                    max_depth – максимальная глубина (∞ по умолчанию)  
                    min_samples_split – минимальное число объектов для деления узла  
                    min_samples_leaf – минимальное число объектов в листе  
                    type_function – тип функции
        """
    def fit(self, feature_data: numpy.ndarray[numpy.longdouble], label_data: numpy.ndarray[numpy.int32]) -> None:
        """fit(self: Tree.DecisionTreeClassifier, feature_data: numpy.ndarray[numpy.longdouble], label_data: numpy.ndarray[numpy.int32]) -> None
            Построить дерево по обучающей выборке.
            
            Parameters
            ----------
            feature_data : np.ndarray[float64], shape (n_samples, n_features)
                Матрица признаков. Допускается тип numpy.float64/longdouble.
            label_data   : np.ndarray[int32],  shape (n_samples,)
                Целевые метки классов.

            Returns
            -------
            None
        """
    def get_final_score(self) -> float:
        """get_final_score(self: Tree.DecisionTreeClassifier) -> float
            Вернуть межкластерный скор
        """
    def predict(self, feature_data: numpy.ndarray[numpy.longdouble]) -> list[int]:
        """predict(self: Tree.DecisionTreeClassifier, feature_data: numpy.ndarray[numpy.longdouble]) -> list[int]
        
            Предсказать класс для каждого объекта.

            Parameters
            ----------
            feature_data : np.ndarray[float64], shape (n_samples, n_features)

            Returns
            -------
            np.ndarray[int32], shape (n_samples,)
                Вектор предсказанных классов.
         
        """
    def print(self) -> None:
        """print(self: Tree.DecisionTreeClassifier) -> None"""

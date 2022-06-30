import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle

def main():
    degrees = []
    labels = []
    for i in range(12):
        try:
            with open(f"./hand_data/{i}.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    degrees.append(list(map(float, line.split(","))))
                    labels.append(i)
        except:
            print(f"not found {i}.txt")

    degrees = np.array(degrees)
    labels = np.array(labels)
    
    X_train, X_test, y_train, y_test = train_test_split(degrees, labels)
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    
    corect = 0
    poses = knn.predict(X_test)
    for i in range(len(poses)):
        if poses[i] == y_test[i]:
            corect += 1
    s = corect / len(y_test)
    print(f"正答率 : {s}%")
        

    with open('./models/hand_model.pickle', mode='wb') as fp:
        pickle.dump(knn, fp)

if __name__ == "__main__":
    main()

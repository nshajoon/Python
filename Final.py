from operator import index
from numpy import append, unique
from sklearn.neural_network import MLPClassifier
import mysql.connector
import numpy as np

cnx =  mysql.connector.connect(user='root', password='Friendly20*')
cursor = cnx.cursor()
DB_NAME = 'CarDB'
cursor.execute("USE {}".format(DB_NAME))
query = "SELECT * FROM info"
cursor.execute(query)
inputs = cursor.fetchall()

X=[]
Y=[]
names =[]
colors = []
for data in inputs:
    names.append(data[0])
    colors.append(data[3])

unique_names = np.unique(names)
unique_colors = np.unique(colors)

for data in inputs:
    X.append( [float((np.where(unique_names == data[0]))[0][0]), float(data[2]), float((np.where(unique_colors == data[3])[0][0])) ]  )
    Y.append(float(data[1]))



clf = MLPClassifier(alpha=1e-05, hidden_layer_sizes=(4, 3), random_state=1,
              solver='lbfgs')
clf.fit(X, Y)

inp0 =  (np.where(unique_names == 'Acadia'))[0][0]
if inp0.size==0:
    inp0 = len(unique_names) +1
inp1 = 60338
inp2 = (np.where(unique_colors == 'White'))[0][0]
if inp2.size==0:
    inp2 = len(unique_colors)+1
result=clf.predict([[inp0, inp1, inp2]])
print (result)
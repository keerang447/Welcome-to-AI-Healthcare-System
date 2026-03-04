import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

data = {
    "age": [25,45,35,50,23,40,60,30],
    "bp": [120,140,130,150,110,145,160,125],
    "sugar": [80,150,90,170,85,160,180,95],
    "disease": [0,1,0,1,0,1,1,0]
}

df = pd.DataFrame(data)

X = df[["age","bp","sugar"]]
y = df["disease"]

model = RandomForestClassifier()
model.fit(X,y)

pickle.dump(model, open("health_model.pkl","wb"))

print("Model Trained Successfully")
import pandas as pd
# Cargar el dataset
# data = pd.read_csv('spam.csv', sep=';', header=None, names=['label', 'message'])
data = pd.read_csv("spam.csv", sep=",", names=["label", "message"])

# Mostrar las primeras filas del dataset
print(data.head())
# Cuántos mensajes hay de cada tipo (spam y ham)
data['label'].value_counts()
# Convertir texto a características numéricas usando TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
# Crear el vectorizador TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(data["message"])
# Convertir las etiquetas a valores numéricos
y = data["label"].map({"ham": 0, "spam": 1})
# Dividir el dataset en entrenamiento y prueba
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Elegimos el algoritmo de clasificación
from sklearn.naive_bayes import MultinomialNB
# Crear el modelo
model = MultinomialNB()
model.fit(X_train, y_train)
# Evaluar el modelo(Predicciones)
y_pred = model.predict(X_test)
# Evaluar el rendimiento del modelo
from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)
# Interpretación:
# 0.90 → Muy bueno
# 0.80–0.90 → Aceptable
# < 0.80 → Mejorable
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

def detectar_spam(texto):
    vector = vectorizer.transform([texto])
    pred = model.predict(vector)

    if pred[0] == 1:
        return "🚫 SPAM"
    else:
        return "✅ NO SPAM"
# Ejemplo de uso
print(detectar_spam("oferta exclusiva solo por hoy"))


import streamlit as st
import pickle
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:] # clonig
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text  = y[:]
    y.clear()

    for i in text:
       y.append(ps.stem(i))
        
    return " ".join(y)

cv = pickle.load(open('vectorizer1.pkl','rb'))
model = pickle.load(open('model1.pkl', 'rb'))


st.title("Email/SMS Spam Classifier")
input_sms = st.text_area("Enter the Message: ")

if st.button('Predict'):

    # 1. preprocess
    transformed_sms = transform_text(input_sms)
    # 2. vectorize
    vector_input = cv.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. display
    if result == 1:
        st.header("SPAM")
    else:
        st.header("NOT SPAM")

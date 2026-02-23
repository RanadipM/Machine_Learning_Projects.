import streamlit as st
import nltk
import pandas as pd
import matplotlib.pyplot as plt
import os
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud

# ==========================
# SAFE NLTK DOWNLOAD
# ==========================
def download_nltk_resources():
    resources = ['punkt', 'vader_lexicon', 'stopwords']
    for resource in resources:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(resource)

download_nltk_resources()

sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words("english"))

# ==========================
# SESSION STATE
# ==========================
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="Speech Intelligence Dashboard", layout="wide")
st.title("🚀 Speech Intelligence & NLP Dashboard")

st.markdown("Analyze speeches using Sentiment Analysis, Topic Modeling, and Text Intelligence.")

# ==========================
# SIDEBAR INPUT
# ==========================
st.sidebar.header("Select Input Source")

option = st.sidebar.radio(
    "Choose Input Method:",
    ("Select Predefined Speech", "Upload Your Own File", "Enter Custom Text")
)

# ==========================
# PREDEFINED FILES
# ==========================
if option == "Select Predefined Speech":
    
  import os

  BASE_DIR = os.path.dirname(os.path.abspath(__file__))

  speeches = {
    "Bose Speech": os.path.join(BASE_DIR, "Sentiment_Analysis_Bose.txt"),
    "Gandhiji Speech": os.path.join(BASE_DIR, "Sentiment_Analysis_Gandhi.txt"),
    "Mandela Speech": os.path.join(BASE_DIR, "Sentiment_Analysis_Mandela.txt")
  }
    selected_speech = st.sidebar.selectbox("Select a speech:", list(speeches.keys()))
    
    if st.sidebar.button("Load Speech"):
        file_path = speeches[selected_speech]
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                st.session_state.text_input = f.read()
            st.success(f"{selected_speech} loaded successfully!")
        else:
            st.error("Speech file not found!")

elif option == "Upload Your Own File":
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file is not None:
        st.session_state.text_input = uploaded_file.read().decode("utf-8")
        st.success("File uploaded successfully!")

elif option == "Enter Custom Text":
    st.session_state.text_input = st.text_area(
        "Enter your text here:",
        value=st.session_state.text_input,
        height=200
    )

# ==========================
# FUNCTIONS
# ==========================
def analyze_sentiment(text):
    sentences = sent_tokenize(text)
    scores = []
    
    for sentence in sentences:
        score = sia.polarity_scores(sentence)
        scores.append(score["compound"])
    
    return sentences, scores


def extract_bigrams(text, top_n=10):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    bigram_list = list(ngrams(tokens, 2))
    bigram_freq = Counter(bigram_list)
    return bigram_freq.most_common(top_n)


def extract_topics(text, n_topics=3):
    documents = [doc.strip() for doc in text.split("\n\n") if doc.strip()]
    
    if len(documents) < 2:
        return ["Not enough text for meaningful topic modeling."]
    
    vectorizer = CountVectorizer(stop_words='english')
    dtm = vectorizer.fit_transform(documents)
    
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    
    words = vectorizer.get_feature_names_out()
    topics = []
    
    for idx, topic in enumerate(lda.components_):
        top_words = [words[i] for i in topic.argsort()[:-6:-1]]
        topics.append(f"Topic {idx+1}: " + ", ".join(top_words))
    
    return topics

# ==========================
# ANALYZE BUTTON
# ==========================
if st.button("Analyze"):

    text_data = st.session_state.text_input
    
    if text_data.strip() == "":
        st.warning("Please provide text first.")
    else:
        sentences, scores = analyze_sentiment(text_data)

        if len(scores) > 0:
            avg_score = sum(scores) / len(scores)
        else:
            avg_score = 0

        # ==========================
        # DASHBOARD METRICS
        # ==========================
        col1, col2, col3 = st.columns(3)

        col1.metric("Average Sentiment", f"{avg_score:.3f}")
        col2.metric("Total Sentences", len(sentences))
        col3.metric("Unique Words", len(set(word_tokenize(text_data))))

        # ==========================
        # SENTIMENT TABLE
        # ==========================
        st.subheader("🔍 Sentence-Level Sentiment")

        result_df = pd.DataFrame({
            "Sentence": sentences,
            "Compound Score": scores
        })

        def label_sentiment(score):
            if score >= 0.05:
                return "Positive"
            elif score <= -0.05:
                return "Negative"
            else:
                return "Neutral"

        result_df["Sentiment"] = result_df["Compound Score"].apply(label_sentiment)

        st.dataframe(result_df)

        # ==========================
        # SENTIMENT DISTRIBUTION
        # ==========================
        st.subheader("📊 Sentiment Distribution")
        sentiment_counts = result_df["Sentiment"].value_counts()
        st.bar_chart(sentiment_counts)

        # ==========================
        # SENTIMENT TREND LINE
        # ==========================
        st.subheader("📈 Sentiment Trend Over Speech")
        fig, ax = plt.subplots()
        ax.plot(scores)
        ax.set_xlabel("Sentence Index")
        ax.set_ylabel("Compound Score")
        st.pyplot(fig)

        # ==========================
        # WORD CLOUD
        # ==========================
        st.subheader("☁️ Word Cloud")

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="black"
        ).generate(text_data)

        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(wordcloud, interpolation='bilinear')
        ax_wc.axis("off")
        st.pyplot(fig_wc)

        # ==========================
        # BIGRAMS
        # ==========================
        st.subheader("🔗 Top 10 Bigrams")

        bigrams = extract_bigrams(text_data)
        bigram_df = pd.DataFrame(bigrams, columns=["Bigram", "Frequency"])
        bigram_df["Bigram"] = bigram_df["Bigram"].apply(lambda x: " ".join(x))

        st.dataframe(bigram_df)

        # ==========================
        # TOPICS
        # ==========================
        st.subheader("🧠 Extracted Topics (LDA)")

        topics = extract_topics(text_data)
        for topic in topics:
            st.write(topic)



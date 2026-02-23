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
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="Speech Intelligence Dashboard", layout="wide")

# ==========================
# SAFE NLTK DOWNLOAD
# ==========================
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("vader_lexicon", quiet=True)
nltk.download("stopwords", quiet=True)

sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words("english"))

# ==========================
# SESSION STATE
# ==========================
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================
# HEADER
# ==========================
st.title("Speech Intelligence & NLP Dashboard")
st.markdown("Interactive dashboard for sentiment analysis, topic modeling, and text intelligence.")

# ==========================
# SIDEBAR
# ==========================
st.sidebar.header("Select Input Source")

option = st.sidebar.radio(
    "Choose Input Method:",
    ("Select Predefined Speech", "Upload Your Own File", "Enter Custom Text")
)

if option == "Select Predefined Speech":
    speeches = {
        "Bose Speech": os.path.join(BASE_DIR, "Sentiment_Analysis_Bose.txt"),
        "Gandhiji Speech": os.path.join(BASE_DIR, "Sentiment_Analysis_Gandhi.txt"),
        "Mandela Speech": os.path.join(BASE_DIR, "Sentiment_Analysis_Mandela.txt")
    }

    selected = st.sidebar.selectbox("Select a speech:", list(speeches.keys()))

    if st.sidebar.button("Load Speech"):
        path = speeches[selected]
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                st.session_state.text_input = f.read()
            st.success(f"{selected} loaded successfully.")
        else:
            st.error("Speech file not found.")

elif option == "Upload Your Own File":
    file = st.file_uploader("Upload a .txt file", type=["txt"])
    if file:
        st.session_state.text_input = file.read().decode("utf-8")

elif option == "Enter Custom Text":
    st.session_state.text_input = st.text_area(
        "Enter text:",
        value=st.session_state.text_input,
        height=200
    )

# ==========================
# FUNCTIONS
# ==========================
def analyze_sentiment(text):
    sentences = sent_tokenize(text)
    scores = [sia.polarity_scores(s)["compound"] for s in sentences]
    return sentences, scores

def extract_bigrams(text, top_n=10):
    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w.isalpha() and w not in stop_words]
    bigrams = list(ngrams(tokens, 2))
    return Counter(bigrams).most_common(top_n)

def extract_topics(text, n_topics):
    docs = [doc.strip() for doc in text.split("\n\n") if doc.strip()]
    if len(docs) < 2:
        return ["Not enough text for topic modeling."]
    vectorizer = CountVectorizer(stop_words="english")
    dtm = vectorizer.fit_transform(docs)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    words = vectorizer.get_feature_names_out()
    topics = []
    for idx, topic in enumerate(lda.components_):
        top_words = [words[i] for i in topic.argsort()[:-6:-1]]
        topics.append(f"Topic {idx+1}: " + ", ".join(top_words))
    return topics

# ==========================
# ANALYSIS
# ==========================
if st.button("Analyze"):

    text = st.session_state.text_input

    if text.strip() == "":
        st.warning("Please provide text.")
    else:
        sentences, scores = analyze_sentiment(text)
        avg_score = sum(scores)/len(scores) if scores else 0

        result_df = pd.DataFrame({
            "Sentence": sentences,
            "Score": scores
        })

        def label(score):
            if score >= 0.05:
                return "Positive"
            elif score <= -0.05:
                return "Negative"
            return "Neutral"

        result_df["Sentiment"] = result_df["Score"].apply(label)

        # ==========================
        # OVERVIEW METRICS
        # ==========================
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average Sentiment", f"{avg_score:.3f}")
        col2.metric("Sentences", len(sentences))
        col3.metric("Word Count", len(word_tokenize(text)))
        col4.metric("Unique Words", len(set(word_tokenize(text))))

        # ==========================
        # SUMMARY INSIGHT
        # ==========================
        st.subheader("Summary Insight")
        if avg_score > 0.2:
            st.write("The speech has a strongly positive tone.")
        elif avg_score > 0:
            st.write("The speech has a moderately positive tone.")
        elif avg_score < -0.2:
            st.write("The speech has a strongly negative tone.")
        elif avg_score < 0:
            st.write("The speech has a moderately negative tone.")
        else:
            st.write("The speech is largely neutral.")

        # ==========================
        # TABS
        # ==========================
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Sentiment", "Topics", "Text Patterns", "Compare", "Download"]
        )

        # -------- Sentiment Tab --------
        with tab1:
            st.subheader("Sentiment Distribution")
            st.bar_chart(result_df["Sentiment"].value_counts())

            st.subheader("Sentiment Trend")
            fig, ax = plt.subplots()
            ax.plot(scores)
            st.pyplot(fig)

            filter_option = st.selectbox(
                "Filter Sentences",
                ["All", "Positive", "Negative", "Neutral"]
            )

            if filter_option != "All":
                st.dataframe(result_df[result_df["Sentiment"] == filter_option])
            else:
                st.dataframe(result_df)

        # -------- Topics Tab --------
        with tab2:
            n_topics = st.slider("Number of Topics", 2, 6, 3)
            topics = extract_topics(text, n_topics)
            for t in topics:
                st.write(t)

        # -------- Text Patterns Tab --------
        with tab3:
            st.subheader("Word Cloud")
            wc = WordCloud(width=800, height=400, background_color="white").generate(text)
            fig_wc, ax_wc = plt.subplots()
            ax_wc.imshow(wc)
            ax_wc.axis("off")
            st.pyplot(fig_wc)

            st.subheader("Top Bigrams")
            st.write(extract_bigrams(text))

            st.subheader("Top Keywords (TF-IDF)")
            tfidf = TfidfVectorizer(stop_words="english")
            matrix = tfidf.fit_transform([text])
            features = tfidf.get_feature_names_out()
            scores_tfidf = matrix.toarray()[0]
            top_idx = scores_tfidf.argsort()[-10:][::-1]
            keywords = [features[i] for i in top_idx]
            st.write(keywords)

        # -------- Compare Tab --------
        with tab4:
            st.subheader("Compare Two Speeches")
            file1 = st.file_uploader("Upload First Speech", type=["txt"], key="f1")
            file2 = st.file_uploader("Upload Second Speech", type=["txt"], key="f2")

            if file1 and file2:
                text1 = file1.read().decode("utf-8")
                text2 = file2.read().decode("utf-8")

                _, scores1 = analyze_sentiment(text1)
                _, scores2 = analyze_sentiment(text2)

                avg1 = sum(scores1)/len(scores1)
                avg2 = sum(scores2)/len(scores2)

                c1, c2 = st.columns(2)
                c1.metric("Speech 1 Avg Sentiment", f"{avg1:.3f}")
                c2.metric("Speech 2 Avg Sentiment", f"{avg2:.3f}")

        # -------- Download Tab --------
        with tab5:
            csv = result_df.to_csv(index=False)
            st.download_button(
                "Download Sentiment Results",
                csv,
                "sentiment_results.csv",
                "text/csv"
            )

        # -------- Explanation Section --------
        with st.expander("How This Dashboard Works"):
            st.write("""
            Sentiment Analysis: VADER lexicon-based scoring.
            Topic Modeling: Latent Dirichlet Allocation (LDA).
            Text Patterns: N-gram frequency and TF-IDF keyword extraction.
            """)

import streamlit as st
import re
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK tokenizer data
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


# =====================================================
# SLANG AND ABBREVIATION DICTIONARY
# =====================================================

slang_dictionary = {
    "u": "you",
    "ur": "your",
    "r": "are",
    "pls": "please",
    "plz": "please",
    "tmrw": "tomorrow",
    "asap": "as soon as possible",
    "msg": "message",
    "btw": "by the way",
    "idk": "I don't know",
    "omg": "oh my god",
    "thx": "thanks",
    "tnx": "thanks",
    "gr8": "great",
    "b4": "before",
    "cuz": "because",
    "coz": "because",
    "w8": "wait",
    "l8r": "later",
    "gonna": "going to",
    "wanna": "want to",
    "gotta": "got to",
    "lemme": "let me",
    "dunno": "do not know",
    "c": "see",
    "cu": "see you",
    "np": "no problem",
    "yw": "you're welcome",
    "cmg": "coming"
}


# =====================================================
# TEXT NORMALIZATION FUNCTION
# =====================================================

def normalize_text(text):

    # Tokenize the input text using NLTK
    tokens = word_tokenize(text)

    normalized_tokens = []
    changes = []

    for token in tokens:

        # Process words and numbers
        if re.match(r"^[A-Za-z0-9]+$", token):

            word = token.lower()

            # Check whether the word exists in dictionary
            if word in slang_dictionary:

                replacement = slang_dictionary[word]

                # Preserve first-letter capitalization
                if token[0].isupper():
                    replacement = replacement.capitalize()

                normalized_tokens.append(replacement)

                changes.append((token, replacement))

            else:
                normalized_tokens.append(token)

        else:
            # Keep punctuation
            normalized_tokens.append(token)

    # Reconstruct the sentence
    result = ""

    for token in normalized_tokens:

        if token in [".", ",", "!", "?", ";", ":", "'s"]:
            result += token

        else:

            if result:
                result += " "

            result += token

    return result, changes, tokens


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Smart Text Normalizer",
    page_icon="✨",
    layout="wide"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: gray;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# TITLE
# =====================================================

st.markdown(
    '<div class="main-title">✨ Smart Text Normalizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Convert slang and abbreviations into standard English'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

st.divider()


# =====================================================
# INPUT SECTION
# =====================================================

st.subheader("📝 Enter Your Text")

text = st.text_area(
    "Type or paste informal text below:",
    placeholder="Example: Thx for ur help",
    height=180
)


# =====================================================
# BUTTONS
# =====================================================

col1, col2 = st.columns(2)

with col1:

    normalize_button = st.button(
        "✨ Normalize Text",
        use_container_width=True
    )

with col2:

    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


# =====================================================
# CLEAR BUTTON
# =====================================================

if clear_button:
    st.rerun()


# =====================================================
# NORMALIZE BUTTON
# =====================================================

if normalize_button:

    if text.strip() == "":

        st.warning("⚠️ Please enter some text first.")

    else:

        result, changes, tokens = normalize_text(text)

        # =================================================
        # NORMALIZED TEXT
        # =================================================

        st.divider()

        st.subheader("📄 Normalized Text")

        st.text_area(
            "Standardized version:",
            result,
            height=180
        )


        # =================================================
        # TEXT STATISTICS
        # =================================================

        total_words = len(
            [
                t for t in tokens
                if re.match(r"^[A-Za-z0-9]+$", t)
            ]
        )

        normalized_words = len(changes)

        if total_words > 0:

            percentage = (
                normalized_words / total_words
            ) * 100

        else:

            percentage = 0


        st.subheader("📊 Text Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Words",
                total_words
            )

        with col2:

            st.metric(
                "Words Normalized",
                normalized_words
            )

        with col3:

            st.metric(
                "Normalization",
                f"{percentage:.1f}%"
            )


        # =================================================
        # CHANGES MADE
        # =================================================

        st.subheader("🔍 Changes Made")

        if changes:

            for old_word, new_word in changes:

                st.write(
                    f"**{old_word}** → **{new_word}**"
                )

            st.success(
                f"✅ Successfully normalized "
                f"{normalized_words} word(s)."
            )

        else:

            st.info(
                "ℹ️ No slang or abbreviations were detected."
            )


        # =================================================
        # NLP TOKENIZATION
        # =================================================

        st.subheader("🔤 NLP Tokenization")

        st.write(
            "The sentence was divided into individual tokens:"
        )

        st.code(
            " | ".join(tokens)
        )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "NLP AAT Project • Smart Text Normalization Tool"
)
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm.auto import tqdm
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# download required NLTK data
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

class DataCleaningPipeline:

    def __init__(self, text_col='text', similarity_threshold=0.9, min_length=10, max_length=1000,perplexity_model_name='gpt2'):
        self.text_col = text_col
        self.similarity_threshold = similarity_threshold
        self.min_length = min_length
        self.max_length = max_length
        self.vectorizer = TfidfVectorizer(stop_words='english')

         # load model/tokenizer for perplexity
        self.perplexity_model = AutoModelForCausalLM.from_pretrained(perplexity_model_name)
        self.perplexity_tokenizer = AutoTokenizer.from_pretrained(perplexity_model_name)
        self.perplexity_model.eval()


    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = [w for w in text.split() if w not in stop_words]
        return ' '.join(tokens)

    def filter_by_length(self, df):
        mask = (
            df['text'].str.len() >= self.min_length
        ) & (
            df['text'].str.len() <= self.max_length
        )
        filtered = df[mask].reset_index(drop=True)
        print(f"Filtered by length: {len(df)} → {len(filtered)} rows")
        return filtered

    def deduplicate(self, df):
        print(f"Building TF-IDF matrix for {len(df)} documents...")
        tfidf = self.vectorizer.fit_transform(df['text'])
        sim_matrix = cosine_similarity(tfidf)

        print("Scanning for duplicates...")
        to_drop = set()
        n = sim_matrix.shape[0]
        for i in tqdm(range(n), desc="Rows", unit="row"):
            for j in range(i + 1, n):
                if sim_matrix[i, j] > self.similarity_threshold:
                    to_drop.add(j)

        result = df.drop(index=list(to_drop)).reset_index(drop=True)
        print(f"Dropped {len(to_drop)} duplicates → {len(result)} remaining")
        return result
    def calculate_perplexity(self, text):
        inputs = self.perplexity_tokenizer(
            text, return_tensors='pt', truncation=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.perplexity_model(
                **inputs, labels=inputs['input_ids']
            )
        return torch.exp(outputs.loss).item()

    def clean(self, input_file, output_file):
        print(f"Loading data from {input_file}…")
        df = pd.read_csv(input_file)

        # Determine source column for text
        col_candidates = [self.text_col.lower(), 'sentence', 'document']
        # Normalize column names to lower-case mapping
        col_map = {col.lower(): col for col in df.columns}
        source_col = None
        for cand in col_candidates:
            if cand in col_map:
                source_col = col_map[cand]
                break
        if not source_col:
            raise KeyError(
                f"None of the columns {col_candidates} found in CSV. Available: {list(df.columns)}"
            )

        # Rename selected column to 'text'
        df = df.rename(columns={source_col: 'text'})

        # Preprocessing
        print("Preprocessing text…")
        tqdm.pandas(desc="Preprocessing")
        df['text'] = df['text'].astype(str).progress_apply(self.preprocess)

        # Filter by length
        df = self.filter_by_length(df)

        # Deduplicate
        # df = self.deduplicate(df)

        # Save cleaned data
        df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")

        # Validate
        self.validate_cleaned_data(output_file)

    def validate_cleaned_data(self, file_path):
        df = pd.read_csv(file_path)
        print(f"\nValidation Report for {file_path}:")
        print(f"  • Total samples: {len(df)}")
        avg_len = df['text'].str.len().mean()
        print(f"  • Average text length: {avg_len:.2f}")

        short_texts = df[df['text'].str.len() < self.min_length]
        print(f"  • Texts shorter than {self.min_length} chars: {len(short_texts)}")
        print(f"  • Unique samples: {df['text'].nunique()}")

        sample_df = df.sample(n=min(100, len(df)))
        print("\nSample for manual review:")
        print(sample_df['text'].head().to_string(index=False))

        common_issues = {
            'special_chars': df['text'].str.contains(r'[^a-zA-Z0-9\s]'),
            'numbers': df['text'].str.contains(r'\d'),
            'all_caps': df['text'].str.isupper()
        }
        for issue, mask in common_issues.items():
            print(f"  • Samples with {issue}: {mask.sum()}")

        perplexities = sample_df['text'].apply(self.calculate_perplexity)
        print(
            f"\nAverage perplexity on sample: {perplexities.mean():.2f}"
            )

# def validate_cleaned_data(file_path, sample_size=100):
#     df = pd.read_csv(file_path)
#     # Basic statistics
#     print(f"\nValidation Report for {file_path}:")
#     print(f"  • Total samples: {len(df)}")
#     avg_len = df['text'].str.len().mean()
#     print(f"  • Average text length: {avg_len:.2f}")
#     short_texts = df[df['text'].str.len() < 10]
#     print(f"  • Texts shorter than 10 chars: {len(short_texts)}")
#     print(f"  • Unique samples: {df['text'].nunique()}")

# if __name__ == '__main__':
#     pipeline = DataCleaningPipeline(text_col='sentence')
#     pipeline.clean(
#         'rawdata/student_scores.csv',
#         'cleandata/studentscores.csv'
#     )

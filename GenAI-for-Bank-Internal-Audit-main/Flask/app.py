from flask import Flask, render_template, request
from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from summa.summarizer import summarize
from summarizer import Summarizer
import nltk
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

app = Flask(__name__)

# Load pre-trained Sentence BERT model
model = SentenceTransformer('bert-base-nli-mean-tokens')

# Load the Gemini API key and Model
gemini_model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key="AIzaSyC2DRYHQGqwXVB6I1BUYtCnNkW5ADQgD8s")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    action = request.form['action']
    rationale = request.form['rationale']
    document = request.files['documents']
    output_messages = [] 

    # Process the inputs here
    # For now, just print them
    output_messages.append("<h4>Input Provided:</h4>")
    output_messages.append("\n")
    output_messages.append("<b>Action</b>: "+ action)
    output_messages.append("<b>Completion Rationale</b>: "+ rationale)
    output_messages.append("<b>Evidence Document</b>: "+ document.filename)
    output_messages.append("\n")

    if document.filename.endswith('.docx') or document.filename.endswith('.pdf'):
        if document.filename.endswith('.docx') :
            doc_content = extract_text_from_docx(document)
        else :
            doc_content = extract_text_from_pdf(document)
            doc_content = remove_junk_characters(doc_content)
            
        evidence = rationale + doc_content
        
        # Set the parameters for summarization
        summary_ratio = 0.3  # Summarize the document to 30% of its original length
        split_text = True  # Split the text into sentences
        return_scores = False  # Do not return sentence scores
        language = "english"  # Set the language to English

        summary = summarize(evidence, ratio=summary_ratio, split=split_text, scores=return_scores, language=language)
        summarised_evidence = " ".join(summary)
        
        # Encode action item and closure statement
        action_item_embedding = model.encode([action])
        closure_embedding = model.encode([summarised_evidence])

        # Calculate cosine similarity
        similarity_score = calculate_cosine_similarity(action_item_embedding, closure_embedding)
        output_messages.append("<h4>Part 1 : Similarity Score with Summarised Evidence</h4>")
        output_messages.append("\n")
        output_messages.append("<b>Summarised Evidence</b>: "+ summarised_evidence)
        output_messages.append("\n")
        output_messages.append("<b>Similarity Score for Action and Summarised Evidence</b>: "+ str(similarity_score))
        output_messages.append("\n")

        output_messages.append("<h4>Gemini generated Audit Review for Summarised Evidence:</h4>")
        output_messages.append("\n")
        output_messages.append("<b>Output</b>: " + gemini_review_summarised(action, summarised_evidence, similarity_score))
        output_messages.append("\n")

        # Evidence sentences
        evidence_sentences = sentences_break(evidence)
        cosine_scores = {}
        
        for evidence_sentence in evidence_sentences:
            evidence_embedding = model.encode([evidence_sentence])
            cosine_score = calculate_cosine_similarity(action_item_embedding, evidence_embedding)
            cosine_scores[evidence_sentence] = cosine_score
            
        top_5_sentences = sorted(cosine_scores.items(), key=lambda x: x[1], reverse=True)[:5]

        output_messages.append("<h4>Part 2 : Key sentences in the Evidence which align closely with the Action item:</h4>")
        output_messages.append("\n")
        evidence = ""
        i = 1
        for sentence, score in top_5_sentences:
            output_messages.append("<b>Evidence"+str(i)+"</b>: " + sentence)
            output_messages.append("<b>Similarity Score</b>: " + str(score))
            evidence += " Evidence " + str(i) + ": " + sentence + ", Cosine Score: " + str(score) + ";"
            i += 1

        output_messages.append("\n")
        output_messages.append("<h4>Gemini generated Audit Review for key sentences in the Evidence:</h4>")
        output_messages.append("\n")
        output_messages.append("<b>Output</b>: " + gemini_review_sentences(action, evidence))
        output_messages.append("\n")
    else:
        output_messages.append("Unsupported file format. Only .docx files are supported.")

    # Here you can process the inputs further, like saving files, etc.
    
    return render_template('output.html', messages=output_messages)


def extract_text_from_docx(docx_file):
    text = []
    document = Document(docx_file)
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text)


def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


def remove_junk_characters(text):
    # Define regular expression pattern to match alphanumeric and punctuation characters
    pattern = r'[^\w\s.,!?]'
    # Use regex to filter out non-standard characters
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def sentences_break(evidence):
    # Use nltk's sentence tokenizer to split evidence into sentences
    sentences = nltk.sent_tokenize(evidence)
    return sentences


# Function to calculate cosine similarity
def calculate_cosine_similarity(embedding1, embedding2):
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity[0][0]

def gemini_review_summarised(action_item, evidence, similarity_score):
    response = gemini_model.generate_content(
        "; Action:" + action_item + 
        "; Evidence: "+ evidence + 
        "; Similarity Score: "+ str(similarity_score) + 
        "; Based on the action and summarised evidence statements along with **cosine similarity score**, can you provide rationale on whether the action is closed or failed?​"
        )
    gemini_output = ""
    for chunk in response:
      gemini_output += chunk.text
    return gemini_output

def gemini_review_sentences(action_item, evidence):
    response = gemini_model.generate_content(
        "; Action:" + action_item + 
        "; Evidence: "+ evidence + 
        "; Based on the action and key sentences in the evidence statements along with **cosine similarity scores**, can you provide rationale on whether the action is closed or failed?​"
        )
    gemini_output = ""
    for chunk in response:
      gemini_output += chunk.text
    return gemini_output

if __name__ == '__main__':
    app.run(debug=True)

# GenAI-integration-in-Bank-Internal-Audit
 
**Overview**

This project leverages Generative AI (GenAI) to transform traditional audit processes in the banking sector, aiming to enhance both efficiency and accuracy. Manual auditing is often prone to errors and time-consuming. Our solution uses advanced Natural Language Processing (NLP) techniques, including cosine similarity and Sentence-BERT, to evaluate audit action items against provided evidence and help auditors identify potential risks more quickly.

**Key Features**
* Cosine Similarity: A similarity score is calculated between audit action items and their supporting evidence, helping auditors assess how closely the evidence addresses the audit issue.
* Top 5 Evidence Sentences: The tool extracts the five most relevant sentences from the evidence, narrowing down the information for auditors to focus on.
Google Gemini Integration: This Large Language Model (LLM) provides interpretative insights into the cosine scores, helping auditors make more informed decisions.

**Project Aim**
* Enhance Audit Efficiency: Reduce the time auditors spend reviewing evidence manually by automating the comparison process.
* Improve Accuracy: Provide auditors with an accurate similarity score and relevant sentence highlights to ensure that no critical information is missed.
* Streamline Audit Review Process: Offer a clear, easy-to-understand interface that reduces the need for auditors to manually sift through lengthy documentation.

**Methodology**
* Data Preprocessing: Clean and prepare the audit action items and evidence.
* Sentence Embedding: Use Sentence-BERT to embed both the action items and evidence into a high-dimensional space.
* Cosine Similarity Calculation: Compute the similarity between the action and evidence, providing a single score to help auditors assess the match.
* Top 5 Sentence Extraction: Identify the five most relevant sentences in the evidence to further assist in the decision-making process.
* Google Gemini Integration: Use the Gemini model to generate insights and explain how the cosine similarity score relates to the audit issue.

**Technology Stack**
* Python Flask: Web framework for building and hosting the application.
* Sentence-BERT: Pre-trained model for embedding action items and evidence.
* Google Gemini: Large Language Model for interpreting cosine similarity scores.

**Audit Review sample input page:**
![image](https://github.com/user-attachments/assets/d633a362-c0ed-454e-9271-42fb78c95b91)



**Audit Review sample output page (Action Closed):**
![image](https://github.com/user-attachments/assets/c7d8bcae-8b79-4762-8419-4002e16bd21f)
![image](https://github.com/user-attachments/assets/ccdab7a0-bab9-42ed-97bb-80485e2f0d54)


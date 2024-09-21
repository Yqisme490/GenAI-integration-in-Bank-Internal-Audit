Introduction

In the banking and finance sector, audit and compliance are crucial for maintaining regulatory standards and mitigating risks. Traditional manual auditing processes are often time-consuming and susceptible to human error. Our project aims to transform these processes by leveraging Generative AI (GenAI) to enhance efficiency and accuracy. This project, in collaboration with a leading multinational financial services company, focuses on developing a GenAI tool to streamline audit reviews. The tool evaluates audit action items against supporting evidence by analysing textual similarities using advanced machine learning techniques.
Our solution employs a pre-trained Sentence-BERT embedding model to compute cosine similarity scores between audit actions and corresponding evidence. By summarising extensive evidence data and pinpointing the most relevant sentences, our tool assists auditors in quickly identifying whether audit issues have been addressed effectively. The system also integrates Google Gemini for providing interpretative insights, aiding auditors in making informed decisions based on the AI-generated results.
The project's primary deliverables include a GenAI system that produces a general similarity score and highlights the top five evidence sentences with the highest contextual relevance to the action items. This approach not only accelerates the review process but also reduces the likelihood of oversight, ultimately contributing to improved audit efficiency and compliance in the banking sector.


Execution of Code :

Run Flask/app.py - python app.py

Sample Cases :

TEST 1

Action : "Ensure that all customer transactions exceeding $10,000 are accompanied by proper documentation and flagged for review, as per anti-money laundering regulations. Review current procedures and implement necessary controls to mitigate the risk of non-compliance and financial penalties."

Closure rationale : "Implemented enhanced monitoring systems to automatically flag and review transactions exceeding $10,000, ensuring compliance with anti-money laundering regulations. All necessary documentation and controls are now in place to mitigate potential risks."

Evidence doc : Evidence1.docx

Result expectation : Action is closed so high similarity score.



TEST 2
Action : "Ensure that all customer transactions exceeding $10,000 are accompanied by proper documentation and flagged for review, as per anti-money laundering regulations. Review current procedures and implement necessary controls to mitigate the risk of non-compliance and financial penalties."

Closure rationale : "Despite concerted efforts, the action item pertaining to the enhancement of monitoring systems for transactions exceeding $10,000 has not been fully completed. While progress has been made in reviewing procedures and exploring technological solutions, challenges remain in the implementation phase. Further coordination and resource allocation are necessary to ensure the effective deployment of enhanced monitoring capabilities and the establishment of robust controls. The issue will continue to be actively monitored and addressed until full compliance is achieved."


Evidence doc : Evidence1.1.docx

Result expectation : Action is not closed so low similarity score.

------------------------------------------------------------------

thank you 

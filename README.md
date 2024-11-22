## **Description**

This project implements **Retrieval-Augmented Generation (RAG)** using a large language model (**LLM**) and documents stored on **Google Drive**. It allows comparing the model's performance with and without contextual information retrieval from documents. The application also supports customizing model parameters, such as temperature, to observe their effects on the generated responses.

---

## **Features**

- **Retrieval-Augmented Generation (RAG)**:
  - Retrieve relevant context from documents to enhance model responses.
  - Compare responses with and without additional context.
- **LLM Parameter Customization**:
  - Adjust temperature to control response creativity.
- **File Management**:
  - Download PDF files from Google Drive.
  - Convert PDFs to text and use them as additional context.
- **Graphical User Interface (Tkinter)**:
  - Interface for managing files and launching operations.

---

## **Installation**
  - git clone https://github.com/Anne-Flower/LLM.git

  - cd LLM-Project

  - pip3 install -r requirements.txt


## **Run**
  - Local : python3 localrag.py
  - Drive :  python3 upload.py



**Question example**
What is a supernova?

**Temperature**
- Precision level of response : Adjust the temperature parameter to control the nature of responses

**Rags**
- With RAG: Retrieves context from stored documents for enhanced accuracy.
- Without RAG: Pure LLM-generated response based solely on the model's training.
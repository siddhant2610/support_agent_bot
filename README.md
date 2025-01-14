# Support-Agent-Chatbot-for-CDP-How-to-Questions

## Project Explanation

This project is a Support Agent Chatbot designed to answer "How-to" questions related to Customer Data Platforms (CDPs). The chatbot leverages natural language processing (NLP) to interpret user queries and provides concise, accurate responses based on predefined datasets. It aims to simplify understanding of CDP-related concepts, troubleshooting, and implementation guidance, making it particularly useful for businesses and developers working with platforms like Segment, mParticle, and others.

### Key Features
- **Dynamic Q&A Generation**: Provides tailored answers to user queries from a curated dataset.
- **Dataset Customization**: Built with the flexibility to fine-tune responses using additional data.
- **Scalable Design**: Supports the addition of more datasets and platforms for expanded coverage.

---

![chat ui image](https://github.com/user-attachments/assets/e5018d74-8314-4b39-97bc-b2ed09bc32ea)


## Tech Stack Used

### 1. **Programming Language**
- **Python**: The core language used for building the chatbot due to its rich ecosystem of libraries for machine learning and NLP.
- **html,css**: used this to give a basic design to the chat bot UI.

### 2. **Frameworks and Libraries**
QLoRA (Quantized LoRA)
QLoRA is an optimization technique that combines quantization and Low-Rank Adaptation (LoRA).

Purpose: Reduces the memory usage of large language models by quantizing weights (e.g., nf16 format) while still adapting a smaller set of weights for fine-tuning.
Usage in the Project: Ideal for fine-tuning large transformer models on resource-constrained systems like Google Colab.

LoRA (Low-Rank Adaptation)
LoRA focuses on fine-tuning by freezing the majority of the model's parameters and training only a few low-rank matrices.

Purpose: Minimizes computational requirements and memory usage.
Why Used: To make fine-tuning efficient without retraining the entire model.

nf16 (Normalized Float 16-bit Precision)
nf16 refers to a precision format used in deep learning to reduce memory consumption without significant loss of accuracy.

Purpose: Optimizes storage and computation during training and inference.
Why Used: Helps manage large datasets and models in limited environments like Colab.
Transformers
Transformers are a deep learning architecture that processes sequential data using attention mechanisms.

Purpose: Excels in NLP tasks like text generation, classification, and question-answering.
Why Used: Forms the backbone of modern language models, enabling complex natural language understanding and generation.
- **Pandas**: For data preprocessing and management.
- **Google Colab**: For executing the project in a cloud-based environment.

### 3. **Other Tools**
- **Jupyter Notebook**: For structuring the project into modular, executable cells.
- **GitHub**: For version control and project collaboration.

---

## Google Colab Link

### Public Access Link
https://colab.research.google.com/drive/10z8jQiQVV5yLg3-n73Z_es980pkcbHl4?usp=sharing 

---

## Getting Started

### Running the Chatbot
1. Open the Google Colab link provided above.
2. connect to T4 GPU, by clicking on manage Runtime
3. Import the required dataset that is attached in the GitHub repository.
4. Train the model by running each cell.
5. Follow the instructions in the notebook to initialize the environment and run the chatbot.
6. Use the input field at last after training, provided in the notebook to test queries.




---

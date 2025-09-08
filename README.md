# mini-rag-app
#This is a minimal implementation of the RAG model for question answering.


# mini-rag-app

## Requirements
- Python 3.10

## Install Dependencies
```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```

## Install Python using MiniConda
1. Download and install MiniConda from [here](https://docs.conda.io/en/latest/miniconda.html).
2. Create a new environment using the following command:
   ```bash
   conda create -n mini-rag python=3.10
   ```
3. Activate the environment:
   ```bash
   conda activate mini-rag
   ```

### (Optional) Setup your command line interface for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### (Optional) Run Ollama Local LLM Server using Colab + Ngrok
Check the notebook and video for instructions.

## Installation
1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Setup the environment variables:
   ```bash
   cp .env.example .env
   ```
   

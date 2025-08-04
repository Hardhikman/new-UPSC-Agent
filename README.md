# 🎓 UPSC GS Question Generator

An intelligent UPSC General Studies question generator that uses RAG (Retrieval-Augmented Generation) with Ollama, LangChain, and ChromaDB to create high-quality Mains-style questions based on previous year question patterns.

## 🌟 Features

- **PDF Processing**: Automatically extracts questions from UPSC previous year question papers
- **Topic-wise Organization**: Categorizes questions by General Studies topics
- **RAG-based Generation**: Uses retrieval-augmented generation to create contextually relevant questions
- **Interactive Web UI**: Gradio-based interface for easy question generation
- **Local LLM Support**: Powered by Ollama for privacy and offline usage
- **Vector Database**: ChromaDB for efficient similarity search and retrieval

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Files     │───▶│  parse_pdfs.py   │───▶│   chunks.json   │
│  (pyq_data/)    │    │                  │    │   (data/)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gradio UI     │◀───│    app.py        │◀───│  indexing.py    │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                         │
                                ▼                         ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Ollama LLM    │    │   ChromaDB      │
                       │                 │    │  (chroma_db/)   │
                       └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Phi3 model downloaded in Ollama (`ollama pull phi3`)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hardhikman/new-UPSC-Agent.git
   cd new-UPSC-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file if needed:
   ```env
   # Ollama Configuration
   EMBEDDING_MODEL="phi3"
   LLM_MODEL="phi3"
   
   # ChromaDB Configuration
   PERSIST_DIR="chroma_db"
   ```

4. **Ensure Ollama is running**
   ```bash
   ollama serve
   ```

5. **Download required models**
   ```bash
   ollama pull phi3
   ```

## 📚 Usage

### Step 1: Prepare Your Data

Place your UPSC previous year question PDF files in the `pyq_data/` directory. The project comes with sample files:
- `GS1.pdf` - General Studies Paper 1
- `GS2.pdf` - General Studies Paper 2  
- `GS3.pdf` - General Studies Paper 3

### Step 2: Extract Questions from PDFs

```bash
python parse_pdfs.py
```

This script will:
- Process all PDF files in `pyq_data/`
- Extract questions organized by topics
- Save structured data to `data/chunks.json`

### Step 3: Index Questions into Vector Database

```bash
python indexing.py
```

This script will:
- Load questions from `data/chunks.json`
- Create embeddings using Ollama
- Store in ChromaDB for efficient retrieval

### Step 4: Launch the Question Generator

```bash
python app.py
```

The Gradio interface will be available at `http://localhost:7860`

## 🎯 How It Works

1. **PDF Processing**: The `parse_pdfs.py` script uses PyPDF2 to extract text from PDF files and applies regex patterns to identify topics and questions.

2. **Data Indexing**: The `indexing.py` script converts questions into vector embeddings using Ollama's phi3 model and stores them in ChromaDB.

3. **Question Generation**: The main application (`app.py`) uses a RAG approach:
   - Retrieves similar questions from the vector database based on the selected topic
   - Uses these as examples in a prompt template
   - Generates new questions using the Ollama LLM

## 📁 Project Structure

```
new-UPSC-Agent/
├── app.py                 # Main Gradio application
├── parse_pdfs.py         # PDF processing and question extraction
├── indexing.py           # Vector database indexing
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── data/
│   └── chunks.json      # Extracted questions data
├── pyq_data/            # PDF files directory
│   ├── GS1.pdf
│   ├── GS2.pdf
│   └── GS3.pdf
└── chroma_db/           # ChromaDB vector database
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMBEDDING_MODEL` | Ollama model for embeddings | `phi3` |
| `LLM_MODEL` | Ollama model for text generation | `phi3` |
| `PERSIST_DIR` | ChromaDB storage directory | `chroma_db` |

### Supported Models

The application supports any Ollama model. Popular choices:
- `phi3` (recommended for balanced performance)
- `llama2`
- `mistral`
- `codellama`

## 🎨 Features in Detail

### PDF Processing
- Automatically detects and processes all PDF files in `pyq_data/`
- Extracts questions using intelligent regex patterns
- Handles various PDF formats and layouts
- Cleans and normalizes question text

### Vector Database
- Uses ChromaDB for efficient similarity search
- Supports incremental updates (avoids duplicates)
- Persistent storage for embeddings
- Topic-based filtering for targeted retrieval

### Question Generation
- RAG-based approach for contextually relevant questions
- Configurable number of questions (1-10)
- Topic-wise question generation
- High-quality output based on previous year patterns

## 🚨 Troubleshooting

### Common Issues

1. **Ollama not running**
   ```bash
   ollama serve
   ```

2. **Model not found**
   ```bash
   ollama pull phi3
   ```

3. **Empty chunks.json**
   - Ensure PDF files are in `pyq_data/`
   - Run `python parse_pdfs.py` first

4. **ChromaDB errors**
   - Delete `chroma_db/` directory and re-run `python indexing.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM support
- [LangChain](https://langchain.com/) for RAG framework
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Gradio](https://gradio.app/) for the web interface

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section
2. Search existing [GitHub Issues](https://github.com/Hardhikman/new-UPSC-Agent/issues)
3. Create a new issue with detailed information

---

**Happy Learning! 🎓**

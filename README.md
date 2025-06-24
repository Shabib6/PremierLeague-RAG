# ⚽️ Premier League RAG Bot

A Retrieval-Augmented Generation (RAG) based chatbot that answers user questions about the Premier League 2024/25 season using data crawled from FBref.com. Built with LangChain, OpenAI GPT-4o, and Qdrant.

---

## 📌 Features

- 🧠 GPT-4o-powered question understanding  
- 🔍 Semantic sub-query generation for deeper search  
- 📄 Context-aware responses using embedded documents  
- 📊 Data sourced from FBref.com (live stats, articles)  
- 💾 Stores and retrieves data from Qdrant Vector DB  

---

## 🚀 Tech Stack

| Layer              | Tech Used                  |
|-------------------|----------------------------|
| LLM               | OpenAI GPT-4o              |
| Embedding Model   | text-embedding-3-large     |
| Vector DB         | Qdrant                     |
| Framework         | LangChain (Python)         |
| Crawler           | WebBaseLoader / Firecrawl  |

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pl-rag-bot.git
cd pl-rag-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your-openai-api-key
FIRECRAWL_API_KEY=your-firecrawl-api-key  # Optional if using Firecrawl
```

### 4. Run Qdrant (if not running already)

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

---

## 🔁 How It Works

1. **Web Crawling:** Pulls live Premier League data from FBref.com  
2. **Chunking & Embedding:** Splits content into chunks and embeds using OpenAI  
3. **Storage:** Embeddings stored in Qdrant for fast retrieval  
4. **Querying:**
   - User inputs a question
   - GPT-4o generates 3 diverse sub-queries
   - Top relevant chunks are retrieved  
5. **Answering:** GPT-4o answers using only the retrieved context  

---

## 💬 Sample Query

```
>> Who is the top scorer in the Premier League 2024/25?

Sub-queries generated:
- Premier League 2024/25 top goal scorer
- Leading goal scorer EPL this season
- Who has scored the most goals?

🔎 Result: [Name] with [X goals]
```

---

## 🧪 Known Issues

- Firecrawl may throw parameter-related errors — fallback to WebBaseLoader for stability.  
- Some newer data from FBref may not be formatted uniformly.  
- Crawling depth and token limits may restrict complete context in some answers.  

---

## 📚 To-Do

- [ ] Add support for uploading custom PDFs (press reports, scouting docs)  
- [ ] Improve UI using Streamlit or Gradio  
- [ ] Add caching layer for repeated queries  
- [ ] Fine-tune sub-query diversity generation  

---

## 👨‍💻 Author

Built by [Shabib Ahamed](https://github.com/Shabib6)

---

## 📄 License

This project is licensed under the MIT License.

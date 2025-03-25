# import wikipedia
# from duckduckgo_search import DDGS

# def search_web(query):
#     """Searches DuckDuckGo for relevant sources."""
#     results = DDGS().text(query)
#     return [{"title": r["title"], "url": r["href"]} for r in results[:3]]

# def get_wikipedia_summary(topic):
#     """Fetches Wikipedia summary if available."""
#     try:
#         return wikipedia.summary(topic, sentences=3)
#     except:
#         return "No Wikipedia summary available."
    

# def research_agent(brief):
#     """Fetch relevant sources from DuckDuckGo & Wikipedia."""
#     sources = search_web(brief)
#     summary = get_wikipedia_summary(brief)
#     return summary, sources


# #print(research_agent("Introduction to Cybersecurity"))


# import chromadb
# from sentence_transformers import SentenceTransformer
# from duckduckgo_search import DDGS
# import wikipedia
# import json 

# # Initialize ChromaDB and embedding model
# chroma_client = chromadb.PersistentClient(path="./chroma_db")
# collection = chroma_client.get_or_create_collection(name="research_cache")
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# def get_cached_research(query):
#     """Retrieve research from cache and convert it back from JSON string."""
#     query_embedding = embedding_model.encode(query).tolist()
#     results = collection.query(query_embeddings=[query_embedding], n_results=1)

#     if results["documents"]:
#         stored_data = results["documents"][0]  # Fetch stored data
        
#         # Check if the stored data is a string (which should be a JSON string)
#         if isinstance(stored_data, str):
#             try:
#                 data = json.loads(stored_data)  # Convert JSON string back to dictionary
#                 return data.get("data", stored_data)  # Extract list from dictionary
#             except json.JSONDecodeError:
#                 return stored_data  # If not valid JSON, return as-is
#         else:
#             return stored_data  # If it's already a list or other type, return it directly
            
#     return None

# def cache_research(query, content):
#     """Store new research results in ChromaDB as a string (JSON format)."""
#     query_embedding = embedding_model.encode(query).tolist()
    
#     if isinstance(content, list):  
#         content = json.dumps({"data": content})  # ✅ Convert list into JSON object

#     collection.add(ids=[query], documents=[content], embeddings=[query_embedding])
#     chroma_client.persist()

# def search_web(query):
#     """Search DuckDuckGo for relevant sources, with caching."""
#     cached_result = get_cached_research(query)
#     if cached_result:
#         return cached_result  # Return cached data

#     results = DDGS().text(query)
#     top_sources = [{"title": r["title"], "url": r["href"]} for r in results[:3]]
#     cache_research(query, top_sources)  # Store in cache
#     return top_sources

# def get_wikipedia_summary(topic):
#     """Fetch Wikipedia summary, with caching."""
#     cached_result = get_cached_research(topic)
#     if cached_result:
#         return cached_result  # Return cached data

#     try:
#         summary = wikipedia.summary(topic, sentences=3)
#     except:
#         summary = "No Wikipedia summary available."

#     cache_research(topic, summary)  # Store in cache
#     return summary


import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
from duckduckgo_search import DDGS
import wikipedia

#Ensure ChromaDB directory exists
DB_PATH = "./chroma_db"
os.makedirs(DB_PATH, exist_ok=True)

#Initialize ChromaDB PersistentClient
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="research_cache")

#Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_cached_research(query):
    """Retrieve research from cache and convert it back from JSON string."""
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=1)

    if results and "documents" in results and results["documents"]:
        #Extract first document
        stored_data = results["documents"][0][0]  

        #Ensure proper JSON decoding
        if isinstance(stored_data, str):
            try:
                data = json.loads(stored_data)
                #Extract list from dictionary
                return data.get("data", stored_data)  
            except json.JSONDecodeError:
                #If not valid JSON return
                return stored_data  
        else:
            return stored_data  
            
    return None  

def cache_research(query, content):
    """Store new research results in ChromaDB as a string (JSON format)."""
    query_embedding = embedding_model.encode(query).tolist()

    if isinstance(content, list):  
        content = json.dumps({"data": content}) 

    collection.add(ids=[query], documents=[content], embeddings=[query_embedding])
    chroma_client.persist()

def search_web(query):
    """Search DuckDuckGo for relevant sources, with caching."""
    cached_result = get_cached_research(query)
    if cached_result:
        return cached_result 

    results = DDGS().text(query)
    top_sources = [{"title": r["title"], "url": r["href"]} for r in results[:3]]
    cache_research(query, top_sources)  
    return top_sources

def get_wikipedia_summary(topic):
    """Fetch Wikipedia summary, with caching."""
    cached_result = get_cached_research(topic)
    if cached_result:
        return cached_result 

    try:
        summary = wikipedia.summary(topic, sentences=3)
    except:
        summary = "No Wikipedia summary available."

    cache_research(topic, summary) 
    return summary


print(f"🔹 Collection Count: {collection.count()}")
print(f"🔹 Collections Available: {chroma_client.list_collections()}")
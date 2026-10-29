import chromadb
from sentence_transformers import SentenceTransformer

print("Loading embedding model (this might take a few seconds)...")
#1. Load a free, local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

#2. Setup ChromaDB (In-Memory for now, we'll save it later)
client = chromadb.Client()
collection = client.create_collection(name="my_knowledge_base")

#3. Our "knowledge Base" (A list of random sentences)
documents = [
    "The New Tesla Model has an impressive battery range.",
    "I love eating pepperoni pizza on saturday nights.",
    "The Stock Market is on a down trend today dur to inflation fears.",
    "Renault is releasing a new hybrid SUV this year.",
    "The best pasta in Italy is made with fresh tomatoes.",
    "Interest Rates are expected to rise next quarter."
]

#Give each document an ID
ids = [f"doc_{i}" for i in range(len(documents))]

print("Embedding documents and saving to ChromaDB...")
#4. Convert the text to vectors and store them
embeddings = model.encode(documents).tolist()
collection.add(
    embeddings=embeddings,
    documents=documents,
    ids=ids
)

print("Database ready!\n")

#5. Let's Search!
queries = [
    "electric vehicles", #Should match Tesla
    "financial news", #Should match Stock Market/Inflation
    "food", #Should match pizza/pasta
]

for query in queries:
    print(f" Searching for: '{query}'")
    
    #Convert the search query into a vector
    query_embedding = model.encode([query])
    
    #Ask ChromaDB for the closest matches
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=1 # Return the top result
    )
    
    #Print the result
    best_match = results['documents'][0][0]
    print(f"Best Match: {best_match}\n")
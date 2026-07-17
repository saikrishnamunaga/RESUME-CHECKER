from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
sentences = ['This is a test sentence.', 'Another example.']
embeddings = model.encode(sentences)
print('Model loaded successfully!')
print('Embeddings shape:', embeddings.shape)
print(embeddings[0][:5])

# A PDF SEARCH ENGINE:
 A webapp that allows you to upload pdfs, and then ask queries similar to a search engine, and you get replies straight from the content uploaded    
 
 🔗[**Try the App**](https://pdf-search-engine-san-io.streamlit.app)
### How does it work?
- Extracts text from PDF
- Divides entire text to chunks of text
- The chunks are then given vector embedding
- Add the embeddings to FAISS index
- Get query embedding
- Search query embeddings in the FAISS index using euclidean distance
- Get results
## Work-In-Progress:
### Features to add:
- Basic RAG implementations
- Proper chunk segmentation
- Chat with PDF might be implemented
- Make it solely for medical field

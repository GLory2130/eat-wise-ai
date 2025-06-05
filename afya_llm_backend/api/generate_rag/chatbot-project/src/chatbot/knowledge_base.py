import os
import logging
import PyPDF2

class KnowledgeBase:
    def __init__(self, document_path):
        self.document_path = document_path
        self.documents = self.load_documents()
        logging.info(f"Loaded {len(self.documents)} documents from {document_path}")

    def load_documents(self):
        documents = []
        try:
            for filename in os.listdir(self.document_path):
                file_path = os.path.join(self.document_path, filename)
                if filename.lower().endswith('.pdf'):
                    # Handle PDF files
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() or ""
                        documents.append({'filename': filename, 'content': text})
                elif filename.lower().endswith('.txt'):
                    # Handle text files
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        documents.append({'filename': filename, 'content': text})
        except Exception as e:
            logging.error(f"Error loading documents: {str(e)}")
        return documents

    def get_response(self, query):
        if not query.strip():
            return None
        
        # Simple keyword search in document content
        for doc in self.documents:
            if query.lower() in doc['content'].lower():
                # Return a snippet with the match
                idx = doc['content'].lower().find(query.lower())
                start = max(0, idx-100)
                end = min(len(doc['content']), idx+200)
                snippet = doc['content'][start:end]
                return f"Found in {doc['filename']}:\n...{snippet}..."
        
        return "I'm sorry, I don't have specific information about that in my knowledge base. However, I can provide general nutrition advice based on my training."

    def add_document(self, document_path):
        """Add a new document to the knowledge base"""
        filename = os.path.basename(document_path)
        dest_path = os.path.join(self.document_path, filename)
        try:
            if not os.path.exists(dest_path):
                if filename.lower().endswith('.pdf'):
                    # Copy PDF file in binary mode
                    with open(document_path, 'rb') as src, open(dest_path, 'wb') as dst:
                        dst.write(src.read())
                else:
                    # Copy text file in text mode
                    with open(document_path, 'r', encoding='utf-8') as src, \
                         open(dest_path, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                # Reload documents
                self.documents = self.load_documents()
                return True
        except Exception as e:
            logging.error(f"Error adding document: {str(e)}")
        return False

    def update_document(self, document_id, new_content):
        """Update an existing document in the knowledge base"""
        file_path = os.path.join(self.document_path, document_id)
        try:
            if os.path.exists(file_path):
                if document_id.lower().endswith('.pdf'):
                    logging.warning("PDF files cannot be updated directly. Please replace the file instead.")
                    return False
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                # Reload documents
                self.documents = self.load_documents()
                return True
        except Exception as e:
            logging.error(f"Error updating document: {str(e)}")
        return False

    def delete_document(self, document_id):
        """Delete a document from the knowledge base"""
        file_path = os.path.join(self.document_path, document_id)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.documents = self.load_documents()
                return True
        except Exception as e:
            logging.error(f"Error deleting document: {str(e)}")
        return False
from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_documents():
    loader = DirectoryLoader(
        "knowledge_base",
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents = loader.load()
    return documents
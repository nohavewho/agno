from agno.knowledge.knowledge import Knowledge
from agno.document.local_document_store import LocalDocumentStore
# from agno.document.s3_document_store import S3DocumentStore
from agno.vectordb.pgvector import PgVector
from agno.agent import Agent
from agno.document.document_v2 import DocumentV2

# This is where we will store our documents
document_store = LocalDocumentStore(
    name="local_document_store",
    description="Local document store",
    storage_path="tmp/documents"
)

# This is a source of user documents
# document_seed_store = S3DocumentStore(
#     name="local_document_store_seed",
#     description="Instance of document store where existing documents are pulled from",
#     read_from_store=True,
#     copy_to_store=False
# )
document_seed_store = None

# Create Knowledge Instance
knowledge = Knowledge(
    name="My Knowledge Base", 
    description="Agno 2.0 Knowledge Implementation",
    document_store=document_store,
    vector_store=PgVector(
        table_name="vectors",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"
    )
)

# This will add a document to the document store

knowledge.load()
knowledge.add_documents(DocumentV2(
        name="CV1",
        paths=["tmp/cv_1.pdf"],
        metadata={"user_tag": "Engineering candidates"},
    )) 

# agent = Agent(
#     name="My Agent",
#     description="Agno 2.0 Agent Implementation",
#     knowledge=knowledge,
#     search_knowledge=True,
# )

# agent.print_response("Who is the best engineering candidate? Search the knowledge base for the answer.", markdown=True)




# Add a document
# knowledge.load()
# knowledge.load_documents({"paths": ["tmp/cv_2.pdf", "https://docs.agno.com/llms-full.txt"]}) #Need to figure out the DX for this
# knowledge.load_documents(documentStore=document_seed_store)


# # Remove documents
# knowledge.remove_document(document_id="123456", remove_from_store=True)
# knowledge.remove_all_documents(remove_from_store=True)

# # Get documents
# knowledge.get_document_by_id(document_id="123456")
# knowledge.get_all_documents()
# knowledge.get_documents_by_name(name="llms-full.txt")
# knowledge.get_documents_by_metadata(metadata={"key": "value"})
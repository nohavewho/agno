from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.db.postgres.postgres import PostgresDb
from agno.document.document_v2 import DocumentV2

# Create Knowledge Instance
documents_db = PostgresDb(
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    knowledge_table="knowledge_documents",
)

knowledge = Knowledge(
    name="Basic SDK Knowledge Base", 
    description="Agno 2.0 Knowledge Implementation",
    vector_store=PgVector(
        table_name="vectors",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"
    ),
    documents_db=documents_db
)

# ---  Sample 1: Add a single document from path ---
# knowledge.add_document("tmp/cv_1.pdf")

# --- Sample 2: Add a single document from DocumentV2 ---
# knowledge.add_document(DocumentV2(
#         name="CV2",
#         paths=["tmp/cv_2.pdf"],
#         metadata={"user_tag": "Engineering candidates"},
#     )) 

# --- Sample 3: Add multiple documents from paths ---
# knowledge.add_documents(["tmp/cv_1.pdf", "tmp/cv_2.pdf"])

# --- Sample 4: Add multiple documents from DocumentV2 ---
# knowledge.add_documents([
#     DocumentV2(
#         name="CV1",
#         paths=["tmp/cv_1.pdf"],
#         metadata={"user_tag": "Engineering candidates"},
#     ),
#     DocumentV2(
#         name="CV2",
#         paths=["tmp/cv_2.pdf"],
#         metadata={"user_tag": "Engineering candidates"},
#     )]
# )

# --- Sample 5: Add multiple documents from a mix of paths and DocumentV2 ---
knowledge.add_documents([
    "tmp/cv_1.pdf",
    DocumentV2(
        name="CV2",
        paths=["tmp/cv_2.pdf"],
        metadata={"user_tag": "Engineering candidates"},
    )
])

document = knowledge.get_document(document_id="dbf56958-507e-401e-a715-b703c82ae6c6")
print(document)

# knowledge_manager = KnowledgeManager(
#     knowledge=knowledge,
#     documents_db=documents_db
# )



# knowledge_manager.add_document(path="tmp/cv_1.pdf")
# knowledge_manager.get_document(id="cv_1")
# knowledge_manager.get_document(name="cv_1")
# knowledge_manager.get_documents(metadata={"user_tag": "Engineering candidates"})

# knowledge_manager.delete_document(id="cv_1")
# knowledge_manager.update_document(id="cv_1", content="Some altered content", metadata={"some_tag": "Updated tags"})
# knowledge.add_documents(paths=["tmp/cv_1.pdf", "tmp/cv_2.pdf"])
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.agent import Agent
from agno.document.document_v2 import DocumentV2



# Create Knowledge Instance
knowledge = Knowledge(
    name="Basic SDK Knowledge Base", 
    description="Agno 2.0 Knowledge Implementation",
    vector_store=PgVector(
        table_name="vectors",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"
    )
)

# Add files to the knowledge base
knowledge.add_documents(
    DocumentV2(
        name="CV1",
        paths=["tmp/cv_1.pdf", "tmp/cv_2.pdf"],
        metadata={"user_tag": "Engineering candidates"},
    )
) 


my_doc = DocumentV2(
    name="CV1",
    urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    metadata={"user_tag": "Recipes"},
)

# knowledge.add_document(my_doc)

agent = Agent(
    name="My Agent",
    description="Agno 2.0 Agent Implementation",
    knowledge=knowledge,
    search_knowledge=True,
    debug_mode=True,
)

agent.print_response("Who is the best engineering candidate? Search the knowledge base for the answer.", markdown=True)

# Remove documents

# TODO: Will need to update this. How will users know what id to use?
knowledge.remove_document(document_id="cv_1") 
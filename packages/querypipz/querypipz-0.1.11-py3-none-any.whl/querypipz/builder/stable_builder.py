
"""
docu = [Document(text = "我叫刘秀"),
 Document(text = "我爱吃大葱"),
]

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import TextNode

nodes = [
    TextNode(
        text="The Shawshank Redemption",
        metadata={
            "author": "Stephen King",
            "theme": "Friendship",
            "year": 1994,
        },
    ),
    TextNode(
        text="The Godfather",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafia",
            "year": 1972,
        },
    ),
    TextNode(
        text="Inception",
        metadata={
            "director": "Christopher Nolan",
            "theme": "Fiction",
            "year": 2010,
        },
    ),
    TextNode(
        text="To Kill a Mockingbird",
        metadata={
            "author": "Harper Lee",
            "theme": "Mafia",
            "year": 1960,
        },
    ),
    TextNode(
        text="1984",
        metadata={
            "author": "George Orwell",
            "theme": "Totalitarianism",
            "year": 1949,
        },
    ),
    TextNode(
        text="The Great Gatsby",
        metadata={
            "author": "F. Scott Fitzgerald",
            "theme": "The American Dream",
            "year": 1925,
        },
    ),
    TextNode(
        text="Harry Potter and the Sorcerer's Stone",
        metadata={
            "author": "J.K. Rowling",
            "theme": "Fiction",
            "year": 1997,
        },
    ),
]


"""


"""
        
from llama_index.core.graph_stores.types import EntityNode, ChunkNode, Relation

# Create a two entity nodes
entity1 = EntityNode(label="PERSON", name="Logan", properties={"age": 28})
entity2 = EntityNode(label="ORGANIZATION", name="LlamaIndex")

# Create a relation
relation = Relation(
    label="WORKS_FOR",
    source_id=entity1.id,
    target_id=entity2.id,
    properties={"since": 2023},
)
"""



# 具体生成器
class QueryBuilder3(QueryBuilder):
    '''

    '''

    def get_query(self):
        # 例如：
            # instance = AnotherClass(param1=value1, param2=value2)
        
        
        retriever = index.as_retriever(similarity_top_k=similarity_top_k)
        query_engine = PythonQueryEngine(
                retriever=retriever,
                response_synthesizer=get_response_synthesizer(response_mode="compact"),
                llm=Settings.llm,
                qa_prompt=qa_prompt,
                stream = True,
            )

        return query_engine
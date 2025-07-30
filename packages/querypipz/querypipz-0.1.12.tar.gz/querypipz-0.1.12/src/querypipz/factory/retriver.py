""" retriver """
from enum import Enum
from typing import Any
from llama_index.core.objects import ObjectIndex
from llama_index.core import VectorStoreIndex

from llama_index.core.indices.property_graph import (
    LLMSynonymRetriever,
    VectorContextRetriever,
)
class RetriverType(Enum):
    """Retriver

    Args:
        Enum (_type_): _description_
    """
    TOOLS_RETRIVER = 'ToolsRetriver'
    GRAPH_LLM_SYNONYM_RETRIEVER = "GraphLLMSynonymRetriever"
    GRAPH_VECTOR_CONTEXT_RETRIEVER = "GraphVectorContextRetriever"
    # 添加更多选项


class Retriver:
    """_summary_
    """
    def __new__(cls, retriver_type: RetriverType | str,tools = None,
                property_graph_store = None) -> Any:
        assert retriver_type.value in [i.value for i in RetriverType]

        if isinstance(retriver_type,RetriverType):
            assert retriver_type.value in [i.value for i in RetriverType]
            key_name = retriver_type.value
        else:
            assert retriver_type in [i.value for i in RetriverType]
            key_name = retriver_type
        instance = None

        if key_name == 'ToolsRetriver':
            # if we were using an external vector store,
            #   we could pass the stroage context and any other kwargs
            # storage_context=storage_context,
            # embed_model=embed_model,
            # ...
            obj_index = ObjectIndex.from_objects(tools,index_cls=VectorStoreIndex)
            instance=obj_index.as_retriever(similarity_top_k=2)

        elif key_name == "GraphLLMSynonymRetriever":
            instance = LLMSynonymRetriever(
                graph_store = property_graph_store,
                include_text=False,
            )
        elif key_name == "GraphVectorContextRetriever":
            instance = VectorContextRetriever(
                graph_store = property_graph_store,
                include_text=False,
            )

        else:
            raise TypeError('Unknown type')
        return instance

    @staticmethod
    def sub_retriver(index,retrievers:list):
        """ set sub retriver"""
        retriever = index.as_retriever(
            sub_retrievers=retrievers
                    )
        return retriever

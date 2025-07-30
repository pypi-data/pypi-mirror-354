""" graph_extractor """

from enum import Enum
from typing import Any
from typing import Literal
from llama_index.core.indices.property_graph.transformations import (
    ImplicitPathExtractor,
    SchemaLLMPathExtractor,
    SimpleLLMPathExtractor,
    DynamicLLMPathExtractor,
)
from llama_index.core import Settings
from llama_index.core.graph_stores.types import (
    EntityNode,
    Relation,
    KG_NODES_KEY,
    KG_RELATIONS_KEY,
)
from llama_index.core.schema import BaseNode, TransformComponent


class MyGraphExtractor(TransformComponent):
    """CUSTOM """

    def __call__(
        self, llama_nodes: list[BaseNode], **kwargs
    ) -> list[BaseNode]:
        for llama_node in llama_nodes:
            # be sure to not overwrite existing entities/relations

            existing_nodes = llama_node.metadata.pop(KG_NODES_KEY, [])
            existing_relations = llama_node.metadata.pop(KG_RELATIONS_KEY, [])

            existing_nodes.append(
                EntityNode(
                    name="llama", label="ANIMAL", properties={"key": "val"}
                )
            )
            existing_nodes.append(
                EntityNode(
                    name="index", label="THING", properties={"key": "val"}
                )
            )

            existing_relations.append(
                Relation(
                    label="HAS",
                    source_id="llama",
                    target_id="index",
                    properties={},
                )
            )

            # add back to the metadata

            llama_node.metadata[KG_NODES_KEY] = existing_nodes
            llama_node.metadata[KG_RELATIONS_KEY] = existing_relations

        return llama_nodes

    # optional async method
    # async def acall(self, llama_nodes: list[BaseNode], **kwargs) -> list[BaseNode]:
    #    ...



class GraphExtractorType(Enum):
    ''' enum '''
    MY_GRAPH_EXTRACTOR = 'MyGraphExtractor'
    DYNAMIC_LLM_PATH_EXTRACTOR = "DynamicLLMPathExtractor"
    DYNAMIC_LLM_PATH_EXTRACTOR2 = "DynamicLLMPathExtractor2"
    SCHEMA_LLM_PATH_EXTRACTOR = "SchemaLLMPathExtractor"
    SCHEMA_LLM_PATH_EXTRACTOR2 = "SchemaLLMPathExtractor2"
    SCHEMA_LLM_PATH_EXTRACTOR3 = "SchemaLLMPathExtractor3"
    SIMPLE_LLM_PATH_EXTRACTOR = "SimpleLLMPathExtractor"
    IMPLICIT_PATH_EXTRACTOR = "ImplicitPathExtractor"
    # Add more options as needed


class GraphExtractor:
    """ Factory"""
    def __new__(cls, graph_extra_type: GraphExtractorType | str) -> Any:

        assert graph_extra_type.value in [i.value for i in GraphExtractorType]

        if isinstance(graph_extra_type,GraphExtractorType):
            assert graph_extra_type.value in [i.value for i in GraphExtractorType]
            key_name = graph_extra_type.value
        else:
            assert graph_extra_type in [i.value for i in GraphExtractorType]
            key_name = graph_extra_type
        instance = None

        if key_name == 'MyGraphExtractor':
            instance = MyGraphExtractor()

        elif key_name == 'MyGraphExtractor':
            instance = MyGraphExtractor()
        elif key_name == 'MyGraphExtractor':
            instance = MyGraphExtractor()

        elif key_name == 'SimpleLLMPathExtractor':
            instance = SimpleLLMPathExtractor()
        elif key_name == 'ImplicitPathExtractor':
            instance = ImplicitPathExtractor()

        elif key_name == 'DynamicLLMPathExtractor':
            instance = DynamicLLMPathExtractor(
                        max_triplets_per_chunk=20,
                        num_workers=4,
                        allowed_entity_types=["POLITICIAN", "POLITICAL_PARTY"],
                        allowed_relation_types=["PRESIDENT_OF", "MEMBER_OF"],
                        allowed_relation_props=["description"],
                        allowed_entity_props=["description"],
                        )

        elif key_name == 'DynamicLLMPathExtractor2':
            instance  = DynamicLLMPathExtractor(
                                                max_triplets_per_chunk=20,
                                                num_workers=4,
                                                allowed_entity_types=None,
                                                allowed_relation_types=None,
                                                allowed_relation_props=[],
                                                allowed_entity_props=[],
                                            )
        elif key_name == 'SchemaLLMPathExtractor':
            instance = SchemaLLMPathExtractor(
                                            llm = Settings.llm,
                                            max_triplets_per_chunk=20,
                                            strict=False,
                                            possible_entities=None,
                                            possible_relations=None,
                                            possible_relation_props=[
                                                "extra_description"
                                            ],
                                            possible_entity_props=[
                                                "extra_description"
                                            ],
                                            num_workers=4,
                                            )
        elif key_name == "SchemaLLMPathExtractor2":

            # best practice to use upper-case
            entities = Literal["PERSON", "PLACE", "ORGANIZATION"]
            relations = Literal["HAS", "PART_OF", "WORKED_ON", "WORKED_WITH", "WORKED_AT"]

            # define which entities can have which relations
            validation_schema = {
                "PERSON": ["HAS", "PART_OF", "WORKED_ON", "WORKED_WITH", "WORKED_AT"],
                "PLACE": ["HAS", "PART_OF", "WORKED_AT"],
                "ORGANIZATION": ["HAS", "PART_OF", "WORKED_WITH"],
            }

            instance = SchemaLLMPathExtractor(
                llm=Settings.llm,
                possible_entities=entities,
                possible_relations=relations,
                kg_validation_schema=validation_schema,
                # if false, allows for values outside of the schema
                # useful for using the schema as a suggestion
                strict=True,
            )
        elif key_name == "SchemaLLMPathExtractor3":

            # best practice to use upper-case
            entities = Literal["人物", "地点",]
            relations = Literal["母子", "父子", "亲属", "朋友", "喜欢","归属"]

            # define which entities can have which relations
            validation_schema = {
                "人物": ["母子", "父子", "亲属", "朋友", ],
                "地点": ["归属", "喜欢"],
            }

            instance = SchemaLLMPathExtractor(
                llm=Settings.llm,
                possible_entities=entities,
                possible_relations=relations,
                kg_validation_schema=validation_schema,
                # if false, allows for values outside of the schema
                # useful for using the schema as a suggestion
                strict=True,
            )

        else:
            raise TypeError('Unknown type')

        return instance

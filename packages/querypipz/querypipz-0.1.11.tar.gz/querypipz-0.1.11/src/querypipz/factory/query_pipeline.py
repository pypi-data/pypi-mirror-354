# TODO  
from enum import Enum
from typing import List, Any

from llama_index.core.query_engine.custom import CustomQueryEngine


class PythonQueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAI
    qa_prompt: PromptTemplate
    stream:bool

    def custom_query(self, query_str: str):
        # custom_query(query_str: str) -> STR_OR_RESPONSE_TYPE
        # acustom_query(query_str: str) -> STR_OR_RESPONSE_TYPE

        queries = query_str.split('&')
        nodes = []
        for query_str in queries:
            nodes += self.retriever.retrieve(query_str)
        # nodes = self.retriever.retrieve(query_str)
        print(query_str,'query_str')
        context_str = "\n\n".join([n.node.get_metadata_str() for n in nodes])
        if self.stream:
            response = self.llm.stream_complete(
                qa_prompt.format(safe_code=context_str, prompt=query_str)
            )

            def response_gen():
                i = [0]
                for r in response:
                    i.append(len(str(r)))
                    yield str(r)[i[-2]:]

            return StreamingResponse(response_gen=response_gen(),source_nodes=nodes)
        else:
            response = self.llm.complete(qa_prompt.format(safe_code=context_str, prompt=query_str))
    
            response_obj = self.response_synthesizer.synthesize(response.text, nodes)
            return Response(response=response.text,source_nodes=nodes) # TODO 增加metadata




class QueryType(Enum):
    Simple = 'Simple'
    Simple2 = 'Simple2'
    # 添加更多选项

class QueryPipeline:
    def __new__(cls, type: QueryType) -> Any:
        assert type.value in [i.value for i in QueryType]
        instance = None

        if type.value == 'Simple':

            # instance = SomeClass(param1=value1, param2=value2)
            pass

        elif type.value == 'Simple2':

            # instance = AnotherClass(param1=value1, param2=value2)
            pass
            query_engine = RetrieverQueryEngine(
                retriever=self.query.retriver,
                response_synthesizer=response_synthesizer,
                node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
            )

        else:
            raise Exception('Unknown type')

        return instance


""" builderlib """
import os
import types
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import Settings

from llama_index.core import StorageContext,SimpleDirectoryReader

from querypipz.abc_ import QueryBuilder
from querypipz.queryer import Queryer
from querypipz.factory import (
    GraphExtractor,
    GraphExtractorType,
    Embedding,
    EmbeddingType,
    Extractor,
    ExtractorType,
    Cleaner,
    CleanerType,
    Splitter,
    SplitterType,
    Reader,
    ReaderType,
    VectorStore,
    VectorStoreType,
    GraphStore,
    GraphStoreType,
    )

load_dotenv()

api_key = os.getenv("BIANXIE_API_KEY")
api_base = os.getenv("BIANXIE_BASE")

class BaseQueryBuilder():
    """ base """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/date'): # 这里设定知识库的本地存储位置
        self.query = Queryer() # 固定
        self.query.persist_path = persist_path # 固定

    def set_llm(self):
        """_summary_
        """
        # Settings.llm = OpenAI(model="gpt-4.1",api_base=api_base,api_key=api_key)

    def build_reader(self):
        """_summary_
        """
        file_path= '/Users/zhaoxuefeng/GitHub/obsidian/工作/日记'
        self.query.reader = SimpleDirectoryReader(
                input_dir=file_path,
                file_extractor = {".md": Reader(ReaderType.CUS_OBSIDIAN_READER)},
                recursive=True,
            )
    def build_ingestion_pipeline(self):
        """_summary_
        """
        self.query.ingestion_pipeline = IngestionPipeline(
            transformations=[
                Splitter(SplitterType.TOKEN_TEXT_SPLITTER),
                Embedding(EmbeddingType.OPENAI_EMBEDDING),
                ],
            docstore=None,
            cache = None
            )

    def build_kg_extractors(self):
        """_summary_
        """
        self.query.kg_extractors = [GraphExtractor(GraphExtractorType.SCHEMA_LLM_PATH_EXTRACTOR3)]


    def build_storage_context(self):
        """_summary_
        """
        self.query.storage_context = StorageContext.from_defaults(
                vector_store=VectorStore(VectorStoreType.FAISS),
                property_graph_store=GraphStore(GraphStoreType.NEO4J_GRAPH_STORE),
            )

    def build_index(self):
        """_summary_
        """
        self.query.index_type = "VectorStoreIndex"

    def build_retriver(self):
        """_summary_
        """
        self.query.retriever_nest = None

    def build_query_pipeline(self): # query 可以直接返回query -> 也可以使用queryengine 进行包装
        """ build """
        self.query.query_engine = None


    def build_tools(self): # 增加一些特异性的函数, 使用以下方法进行添加
        """_summary_
        """
        def dynamic_method(self, name_path:str):
            return self.index.property_graph_store.save_networkx_graph(name=name_path)
        # self.query.tools = dynamic_method.__get__(self.query,Queryer)
        types.ModuleType(dynamic_method,self.query)
        # self.query.tools2 = ...

    def get_queryer(self):# 默认
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.query






class ObsidianDateBuilder(QueryBuilder):
    """_summary_

    Args:
        QueryBuilder (_type_): _description_
    """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/date'):
        """_summary_

        Args:
            persist_path (str, optional): _description_. 
            Defaults to '/Users/zhaoxuefeng/GitHub/obsidian/知识库/date'.
        """
        self.query = Queryer()
        self.query.persist_path = persist_path

    def build_reader(self):
        """_summary_
        """
        file_path= '/Users/zhaoxuefeng/GitHub/obsidian/工作/日记'
        self.query.reader = SimpleDirectoryReader(
            input_dir=file_path,
            file_extractor = {".md": Reader(ReaderType.CUS_OBSIDIAN_READER)},
            recursive=True,
            )
    def build_ingestion_pipeline(self):
        """_summary_
        """
        self.query.ingestion_pipeline = IngestionPipeline(
            transformations=[Splitter(SplitterType.TOKEN_TEXT_SPLITTER),
                             Embedding(EmbeddingType.OPENAI_EMBEDDING),
                             ])

    def build_storage_context(self):
        """_summary_
        """
        self.query.storage_context = StorageContext.from_defaults(
            vector_store=VectorStore(VectorStoreType.SIMPLE_VECTOR_STORE))

    def build_index(self):
        """_summary_
        """
        self.query.index_type = "VectorStoreIndex"

    def build_retriver(self):
        """_summary_
        """
        self.query.retriever_Nest = None

    def build_query_pipeline(self):
        """_summary_
        """
        self.query.query_engine = None

    def get_queryer(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.query

    def build_tools(self):
        """_summary_
        """


class ObsidianHabitBuilder(ObsidianDateBuilder):
    """ obsidian habit builder """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/habit'):
        super().__init__(persist_path = persist_path)

    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/GitHub/obsidian/工作/习惯'
        self.query.reader = SimpleDirectoryReader(
                input_dir=file_path,
                file_extractor = {".md": Reader(ReaderType.CUS_OBSIDIAN_READER)},
                recursive=True,
            )
    def build_tools(self):
        pass

class DeDaoJYRKBuilder(QueryBuilder):
    """ dedao jyrk builder """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/JYRK'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def set_llm(self):
        Settings.llm = OpenAI(model="gemini-2.5-flash-preview-04-17-nothinking",
                              api_base=api_key,
                              api_key=api_base)


    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/本地文稿/百度空间/实验广场/实验/04-万维钢'
        self.query.reader = SimpleDirectoryReader(
            input_dir=file_path,
            file_extractor = {".pdf": Reader(ReaderType.PDF_FILE_READER)},
            recursive=True,
            exclude=["*.mp3"],
            )
    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = IngestionPipeline(transformations=[
            Cleaner(CleanerType.DE_DAO_CLEANER),
            Splitter(SplitterType.DEDAO_JYRK_TEXT_SPLITTER),
            Extractor(ExtractorType.DEDAO_JYRK_TITLE_EXTRACTOR),
            Embedding(EmbeddingType.OPENAI_EMBEDDING),
            ])

    def build_storage_context(self):
        self.query.storage_context = None

    def build_index(self):
        self.query.index_type = "VectorStoreIndex"

    def build_retriver(self):
        self.query.retriever_nest = None

    def build_query_pipeline(self):
        self.query.query_engine = None

    def get_queryer(self):
        return self.query

    def build_tools(self):
        pass

    def build_kg_extractors(self):
        self.query.kg_extractors = None


class DeDaoJYRK2Builder(QueryBuilder):
    """ dedao jyrk 2 builder """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/JYRK2'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def set_llm(self):
        Settings.llm = OpenAI(model="gemini-2.5-flash-preview-04-17-nothinking",
                              api_base=api_key,
                              api_key=api_base)


    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/本地文稿/百度空间/实验广场/实验/04-万维钢'
        self.query.reader = SimpleDirectoryReader(
            input_dir=file_path,
            file_extractor = {".pdf": Reader(ReaderType.PDF_FILE_READER)},
            recursive=True,
            exclude=["*.mp3"],
            )
    def build_ingestion_pipeline(self):
        from llama_index.core.ingestion.cache import IngestionCache
        cache = IngestionCache()
        self.query.ingestion_pipeline = IngestionPipeline(
            transformations=[
                Cleaner(CleanerType.DE_DAO_CLEANER),
                Splitter(SplitterType.DEDAO_JYRK_TEXT_SPLITTER),
                Extractor(ExtractorType.DEDAO_JYRK_TITLE_EXTRACTOR),
                Embedding(EmbeddingType.OPENAI_EMBEDDING),
                ],
            cache=cache
            )

    def build_storage_context(self):
        self.query.storage_context = None

    def build_index(self):
        self.query.index_type = "VectorStoreIndex"

    def build_retriver(self):
        self.query.retriever_nest = None

    def build_query_pipeline(self):
        self.query.query_engine = None

    def get_queryer(self):
        return self.query

    def build_tools(self):
        pass

    def build_kg_extractors(self):
        self.query.kg_extractors = None

class DeDaoJYRK6Builder(QueryBuilder):
    """ dedao jyrk 6 builder """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/JYRK6'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def set_llm(self):
        Settings.llm = OpenAI(model="gemini-2.5-flash-preview-04-17-nothinking",
                              api_base=api_key,
                              api_key=api_base)


    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/本地文稿/百度空间/实验广场/实验/精英日课6/高手修炼手册-40讲'
        self.query.reader = SimpleDirectoryReader(
            input_dir=file_path,
            file_extractor = {".pdf": Reader(ReaderType.PDF_FILE_READER)},
            recursive=True,
            exclude=["*.mp3","*.MP3"],
            )
    def build_ingestion_pipeline(self):
        from llama_index.core.ingestion.cache import IngestionCache
        cache = IngestionCache()
        self.query.ingestion_pipeline = IngestionPipeline(
            transformations=[
                Cleaner(CleanerType.DE_DAO_CLEANER),
                Splitter(SplitterType.DEDAO_JYRK_TEXT_SPLITTER),
                Extractor(ExtractorType.DEDAO_JYRK_TITLE_EXTRACTOR),
                Embedding(EmbeddingType.OPENAI_EMBEDDING),
                ],
            cache=cache)

    def build_storage_context(self):
        self.query.storage_context = None

    def build_index(self):
        self.query.index_type = "VectorStoreIndex"

    def build_retriver(self):
        self.query.retriever_nest = None

    def build_query_pipeline(self):
        self.query.query_engine = None

    def get_queryer(self):
        return self.query

    def build_tools(self):
        pass

    def build_kg_extractors(self):
        self.query.kg_extractors = None

class HistoryMemoryBuilder(QueryBuilder):
    """ history memory builder 
        用于知识库聊天 存储历史聊天记录, 作为最简单的长期记忆

    Args:
        QueryBuilder (_type_): _description_
    """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/HistoryMemory'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def set_llm(self):
        pass

    def build_reader(self):
        self.query.reader = None

    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = None

    def build_storage_context(self):
        self.query.storage_context = None

    def build_index(self):
        self.query.index_type = "VectorStoreIndex"

    def build_retriver(self):
        self.query.retriever_nest = None

    def build_query_pipeline(self):
        self.query.query_engine = None
        self.query.ingestion_pipeline = IngestionPipeline(
            transformations=[
                Splitter(SplitterType.HISTORY_MEMORY_SPLITTER),
                Extractor(ExtractorType.HISTORY_MEMORY_KEYWORD_EXTRACTOR),
                Embedding(EmbeddingType.SIMILARITY_TEXT_3L_EMBEDDING),
                ]
            )

    def get_queryer(self):
        return self.query

    def build_tools(self):
        self.query.tools = None

    def build_kg_extractors(self):
        self.query.kg_extractors = None


class HistoryMemory2Builder(QueryBuilder):
    """用于知识库聊天 存储历史聊天记录, 作为最简单的长期记忆

    Args:
        QueryBuilder (_type_): _description_
    """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/HistoryMemory'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def set_llm(self):
        pass

    def build_reader(self):
        self.query.reader = None

    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = None

    def build_storage_context(self):
        self.query.storage_context = None

    def build_index(self):
        self.query.index_type = "VectorStoreIndex"

    def build_retriver(self):
        self.query.retriever_nest = None

    def build_query_pipeline(self):
        self.query.query_engine = None

    def get_queryer(self):
        return self.query

    def build_tools(self):
        self.query.tools = None

    def build_kg_extractors(self):
        self.query.kg_extractors = None


class TestGraphBuilder(QueryBuilder):
    """ test Graph builder """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/TestGraph'):
        self.query = Queryer()
        self.query.persist_path = persist_path


    def set_llm(self):
        Settings.llm = OpenAI(model="gpt-4.1",api_base=api_base,api_key=api_key)

    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/本地文稿/百度空间/实验广场/实验/data/chat_history_demo_dongsheng'
        self.query.reader = SimpleDirectoryReader(
            input_dir=file_path,
            file_extractor = {".md": Reader(ReaderType.PDF_FILE_READER)},
            recursive=True,
            # exclude=["*.mp3"],
            )
    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = IngestionPipeline(transformations=[])

    def build_storage_context(self):
        self.query.storage_context = StorageContext.from_defaults(
            vector_store=VectorStore(VectorStoreType.FAISS))

    def build_index(self):
        self.query.index_type = "PropertyGraphIndex"


    def build_retriver(self):
        self.query.retriever_nest = None


    def build_query_pipeline(self):
        self.query.query_engine = None

    def get_queryer(self):
        return self.query

    def build_tools(self):
        def dynamic_method(self, name_path:str):
            return self.index.property_graph_store.save_networkx_graph(name=name_path) # for debug
        types.ModuleType(dynamic_method,self.query)
        # self.query.tools = dynamic_method.__get__(self.query,Queryer)




class Test2GraphBuilder(TestGraphBuilder):
    """ test2 graph """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/TestGraph2'):
        super().__init__(persist_path = persist_path)


    def build_kg_extractors(self):
        self.query.kg_extractors = [GraphExtractor(GraphExtractorType.SIMPLE_LLM_PATH_EXTRACTOR),
                                    GraphExtractor(GraphExtractorType.IMPLICIT_PATH_EXTRACTOR)]




class Test3GraphBuilder(QueryBuilder):
    """ test3 graph """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/TestGraph3'):
        self.query = Queryer()
        self.query.persist_path = persist_path


    def set_llm(self):
        pass
        # Settings.llm = OpenAI(model="gpt-4.1",api_base=api_base,api_key=api_key)

    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/本地文稿/百度空间/实验广场/实验/data/yingjiememorycard'
        self.query.reader = SimpleDirectoryReader(input_dir=file_path)
    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = IngestionPipeline(
            transformations=[Splitter(splitter_type=SplitterType.TEST_SPLITTER)]
            )

    def build_storage_context(self):
        self.query.storage_context = StorageContext.from_defaults(
            vector_store=VectorStore(VectorStoreType.FAISS),
            property_graph_store=GraphStore(GraphStoreType.NEO4J_GRAPH_STORE)
            )

    def build_index(self):
        self.query.index_type = "PropertyGraphIndex"


    def build_retriver(self):
        self.query.retriever_nest = None


    def build_query_pipeline(self):
        self.query.query_engine = None

    def get_queryer(self):
        return self.query

    def build_kg_extractors(self):
        self.query.kg_extractors = [GraphExtractor(GraphExtractorType.SCHEMA_LLM_PATH_EXTRACTOR3)]

    def build_tools(self):
        def dynamic_method(self, name_path:str):
            return self.index.property_graph_store.save_networkx_graph(name=name_path) # for debug
        types.ModuleType(dynamic_method,self.query)
        # self.query.tools = dynamic_method.__get__(self.query,Queryer)


class Test4GraphBuilder(QueryBuilder):
    """# 基于树的加载分析逻辑

    Args:
        QueryBuilder (_type_): _description_
    """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/TestGraph4'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def set_llm(self):
        pass
        # Settings.llm = OpenAI(model="gpt-4.1",api_base=api_base,api_key=api_key)

    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/本地文稿/百度空间/实验广场/实验/data/yingjiememorycard'
        self.query.reader = SimpleDirectoryReader(input_dir=file_path)
    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = IngestionPipeline(
            transformations=[
                Splitter(splitter_type=SplitterType.TEST_SPLITTER)
                ]
            )

    def build_storage_context(self):
        self.query.storage_context = StorageContext.from_defaults(
            vector_store=VectorStore(VectorStoreType.FAISS),
            property_graph_store=GraphStore(GraphStoreType.NEO4J_GRAPH_STORE),)

    def build_index(self):
        self.query.index_type = "PropertyGraphIndex"


    def build_retriver(self):
        self.query.retriever_nest = None


    def build_query_pipeline(self):
        self.query.query_engine = None

    def get_queryer(self):
        return self.query

    def build_kg_extractors(self):
        self.query.kg_extractors = [GraphExtractor(GraphExtractorType.SCHEMA_LLM_PATH_EXTRACTOR3)]

    def build_tools(self):
        def dynamic_method(self, name_path:str):
            return self.index.property_graph_store.save_networkx_graph(name=name_path) # for debug

        types.ModuleType(dynamic_method,self.query)
        # self.query.tools = dynamic_method.__get__(self.query,Queryer)


class Test5GraphBuilder(QueryBuilder):
    """# 业务构建型
    Args:
        QueryBuilder (_type_): _description_
    """
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/TestGraph5'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def set_llm(self):
        Settings.llm = OpenAI(model="gpt-4.1-mini-2025-04-14",api_base=api_base,api_key=api_key)

    def build_reader(self):
        self.query.reader = None

    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = IngestionPipeline(
            transformations=[
                Splitter(splitter_type=SplitterType.TEST_SPLITTER)
                ]
            )

    def build_storage_context(self):
        self.query.storage_context = StorageContext.from_defaults(
            vector_store=VectorStore(VectorStoreType.FAISS),
            property_graph_store=GraphStore(GraphStoreType.NEO4J_GRAPH_STORE),)

    def build_index(self):
        self.query.index_type = "PropertyGraphIndex"


    def build_retriver(self):
        self.query.retriever_nest = None


    def build_query_pipeline(self):
        self.query.query_engine = None

    def get_queryer(self):
        return self.query

    def build_kg_extractors(self):
        self.query.kg_extractors = [GraphExtractor(GraphExtractorType.SCHEMA_LLM_PATH_EXTRACTOR3)]

    def build_tools(self):
        def dynamic_method(self, name_path:str):
            return self.index.property_graph_store.save_networkx_graph(name=name_path) # for debug

        types.ModuleType(dynamic_method,self.query)
        # self.query.tools = dynamic_method.__get__(self.query,Queryer)

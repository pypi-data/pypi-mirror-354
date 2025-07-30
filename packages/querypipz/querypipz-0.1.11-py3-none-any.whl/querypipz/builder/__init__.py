""" builder """
from enum import Enum
from typing import Any
from .builderlib import (DeDaoJYRK2Builder,
                         DeDaoJYRK6Builder,
                         HistoryMemoryBuilder,
                         HistoryMemory2Builder,
                         BaseQueryBuilder,
                         ObsidianDateBuilder,
                         ObsidianHabitBuilder,
                         DeDaoJYRKBuilder,
                         TestGraphBuilder,
                         Test2GraphBuilder,
                         Test3GraphBuilder,
                         Test4GraphBuilder,
                         Test5GraphBuilder)

class BuilderType(Enum):
    """构造者清单

    Args:
        Enum (_type_): 选择构造者
    """
    OBSIDIAN_DATE_BUILDER = 'ObsidianDateBuilder'
    OBSIDIAN_HABIT_BUILDER = "ObsidianHabitBuilder"
    DEDAO_JYRK_BUILDER = "DeDaoJYRKBuilder"
    DEDAO_JYRK_BUILDER2 = "DeDaoJYRK2Builder"
    DEDAO_JYRK_BUILDER6 = "DeDaoJYRK6Builder"
    TEST_GRAPH_BUILDER = "TestGraphBuilder"
    TEST_GRAPH_BUILDER2 = "Test2GraphBuilder"
    TEST_GRAPH_BUILDER3 = "Test3GraphBuilder"
    TEST_GRAPH_BUILDER4 = "Test4GraphBuilder"
    TEST_GRAPH_BUILDER5 = "Test5GraphBuilder"
    
    HISTORY_MEMORY_BUILDER = "HistoryMemoryBuilder"
    HISTORY_MEMORY_BUILDER2 = "HistoryMemory2Builder"
    SIMPLE = 'simple'
    # 添加更多选项

class BuilderFactory:
    """构造者工厂

    Raises:
        ValueError: _description_

    Returns:
        builder: 构造者
    """
    _builders = {
        BuilderType.OBSIDIAN_DATE_BUILDER: ObsidianDateBuilder,
        BuilderType.OBSIDIAN_HABIT_BUILDER: ObsidianHabitBuilder,
        BuilderType.DEDAO_JYRK_BUILDER: DeDaoJYRKBuilder,
        BuilderType.DEDAO_JYRK_BUILDER2: DeDaoJYRK2Builder,
        BuilderType.DEDAO_JYRK_BUILDER6: DeDaoJYRK6Builder,
        BuilderType.TEST_GRAPH_BUILDER: TestGraphBuilder,
        BuilderType.TEST_GRAPH_BUILDER2: Test2GraphBuilder,
        BuilderType.TEST_GRAPH_BUILDER3: Test3GraphBuilder,
        BuilderType.TEST_GRAPH_BUILDER4: Test4GraphBuilder,
        BuilderType.TEST_GRAPH_BUILDER5: Test5GraphBuilder,
        BuilderType.HISTORY_MEMORY_BUILDER: HistoryMemoryBuilder,
        BuilderType.HISTORY_MEMORY_BUILDER2: HistoryMemory2Builder,
    }

    def __new__(cls, builder_type: BuilderType,persist_path=None) -> Any:
        if builder_type not in cls._builders:
            raise ValueError(f"Unknown builder type: {builder_type}")
        builder_class = cls._builders[builder_type]
        if persist_path:
            instance = builder_class(persist_path = persist_path)
        else:
            instance = builder_class()
        return instance

'''
#Retrieval 类设计应该能够动态支持不同的向量数据库实现，但每个 Retrieval
实例只绑定一个具体的数据库实现。我们可以使用抽象类来定义接口，
并通过依赖注入选择具体的数据库实现。

1. 抽象接口设计
定义 VectorDatabase 接口
抽象 VectorDatabase，定义所有向量数据库需要实现的功能，如插入向量和检索向量。
'''

from abc import ABC, abstractmethod

class VectorDatabase(ABC):
    @abstractmethod
    def insert_vector(self, vector_id: str, vector: list[float]) -> None:
        """Insert a vector into the database."""
        pass

    @abstractmethod
    def search_vector(self, query_vector: list[float], top_k: int) -> list[tuple[str, float]]:
        """Search for the top-k closest vectors to the query vector."""
        pass
'''
定义 Retrieval 接口
Retrieval 类使用一个具体的 VectorDatabase 实现作为依赖。
'''

class Retrieval:
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db

    def insert(self, vector_id: str, vector: list[float]) -> None:
        """Insert a vector into the underlying database."""
        self.vector_db.insert_vector(vector_id, vector)

    def retrieve(self, query_vector: list[float], top_k: int) -> list[tuple[str, float]]:
        """Retrieve top-k vectors from the underlying database."""
        return self.vector_db.search_vector(query_vector, top_k)

'''
2. 具体的向量数据库实现
每种向量数据库实现 VectorDatabase 接口，提供自己的逻辑。
'''
class DB1(VectorDatabase):
    def __init__(self):
        self.data = {}  # 模拟数据库存储

    def insert_vector(self, vector_id: str, vector: list[float]) -> None:
        self.data[vector_id] = vector

    def search_vector(self, query_vector: list[float], top_k: int) -> list[tuple[str, float]]:
        from math import sqrt
        results = [
            (vector_id, sqrt(sum((q - v) ** 2 for q, v in zip(query_vector, vector))))
            for vector_id, vector in self.data.items()
        ]
        return sorted(results, key=lambda x: x[1])[:top_k]

class DB2(VectorDatabase):
    def __init__(self):
        self.storage = []

    def insert_vector(self, vector_id: str, vector: list[float]) -> None:
        self.storage.append((vector_id, vector))

    def search_vector(self, query_vector: list[float], top_k: int) -> list[tuple[str, float]]:
        from numpy import dot
        from numpy.linalg import norm
        results = [
            (vector_id, dot(query_vector, vector) / (norm(query_vector) * norm(vector)))
            for vector_id, vector in self.storage
        ]
        return sorted(results, key=lambda x: -x[1])[:top_k]

'''
3. 使用 Retrieval 结合不同的数据库实现
通过依赖注入将数据库实例传入 Retrieval，实现对不同数据库的支持。
'''

# 初始化不同的数据库实例
db1 = DB1()
db2 = DB2()

# 使用 DB1
retrieval1 = Retrieval(vector_db=db1)
retrieval1.insert("vec1", [1, 2, 3])
retrieval1.insert("vec2", [4, 5, 6])
retrieval1.insert("vec3", [7, 8, 9])

query = [1, 0, 0]
print("Results from DB1:", retrieval1.retrieve(query, top_k=2))

# 使用 DB2
retrieval2 = Retrieval(vector_db=db2)
retrieval2.insert("vecA", [0.1, 0.2, 0.3])
retrieval2.insert("vecB", [0.4, 0.5, 0.6])
retrieval2.insert("vecC", [0.7, 0.8, 0.9])

print("Results from DB2:", retrieval2.retrieve(query, top_k=2))

'''
接口分离：

VectorDatabase 作为数据库操作接口，适配不同的数据库实现。
Retrieval 作为高层检索逻辑，使用具体的数据库实现。
依赖注入：

Retrieval 通过构造函数接收 VectorDatabase 实例，实现对不同数据库的支持。
可扩展性：
'''

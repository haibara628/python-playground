from typing import Any, Dict
import threading
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int, data: Dict[str, Any] = None):
        """初始化.

        :param capacity: 空间上限, 0 表示不要 cache, 小于 0 的数表示不设上限
        :param data: 预先加载的数据, 来自 dump 方法的输出
        """
        self.lock = threading.Lock()
        self.capacity = capacity
        if data is None:
            self.cache = OrderedDict()
        else:
            self.load(data)

    def clear(self):
        with self.lock:
            self.cache.clear()

    def get(self, key: str) -> Any:
        with self.lock:
            if key not in self.cache:
                return None
            else:
                self.cache.move_to_end(key)
                return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        with self.lock:
            if self.capacity == 0:
                return
            self.cache[key] = value
            self.cache.move_to_end(key)
            if self.capacity >= 0:
                while len(self.cache) > self.capacity:
                    self.cache.popitem(last=False)

    def delete(self, key: str) -> None:
        with self.lock:
            if key in self.cache:
                del self.cache[key]

    def dump(self) -> Dict[str, Any]:
        with self.lock:
            return dict(self.cache)

    def load(self, data: Dict[str, Any]):
        with self.lock:
            self.cache = OrderedDict(data)
            if self.capacity >= 0:
                self.capacity = max(self.capacity, len(self.cache))

    def items(self):
        with self.lock:
            return self.cache.copy().items()
    
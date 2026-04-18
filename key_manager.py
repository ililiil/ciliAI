import os
import base64
import threading
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class KeyManager:
    def __init__(self):
        self._keys: List[Dict[str, str]] = []
        self._current_index = 0
        self._lock = threading.Lock()
        self._initialized = False

    def _decode_secret_key(self, sk: str) -> str:
        """Secret Key - 直接返回原始值（SDK内部处理）"""
        return sk

    def _load_keys(self):
        """从环境变量加载所有密钥组"""
        with self._lock:
            if self._initialized:
                return

            self._keys.clear()
            self._current_index = 0

            index = 1
            while True:
                ak = os.getenv(f'VOLC_AK_{index}')
                sk = os.getenv(f'VOLC_SK_{index}')

                if not ak and not sk:
                    if index == 1:
                        logger.warning(f"未找到 VOLC_AK_{index} 和 VOLC_SK_{index}，尝试加载旧版密钥...")
                        ak = os.getenv('VOLC_AK')
                        sk = os.getenv('VOLC_SK')
                        if ak and sk:
                            decoded_sk = self._decode_secret_key(sk)
                            self._keys.append({'ak': ak, 'sk': decoded_sk, 'index': 0})
                            logger.info(f"已加载旧版密钥组 0 (AK: {ak[:10]}...)")
                            index += 1
                            continue
                    break

                if ak and sk:
                    decoded_sk = self._decode_secret_key(sk)
                    self._keys.append({'ak': ak, 'sk': decoded_sk, 'index': index})
                    logger.info(f"已加载密钥组 {index} (AK: {ak[:10]}...)")

                index += 1

                if index > 100:
                    logger.warning("密钥组数量超过100，可能存在配置错误")
                    break

            self._initialized = True

            if not self._keys:
                logger.error("未找到任何有效的火山引擎密钥配置！")
            else:
                logger.info(f"密钥管理器初始化完成，共 {len(self._keys)} 组密钥")

    def ensure_initialized(self):
        """确保密钥已加载"""
        if not self._initialized:
            self._load_keys()

    def get_next_key(self) -> Optional[Dict[str, str]]:
        """获取下一组密钥（线程安全）"""
        self.ensure_initialized()

        with self._lock:
            if not self._keys:
                return None

            key = self._keys[self._current_index]
            self._current_index = (self._current_index + 1) % len(self._keys)

            return {
                'ak': key['ak'],
                'sk': key['sk'],
                'index': key['index']
            }

    def get_key_by_index(self, index: int) -> Optional[Dict[str, str]]:
        """获取指定索引的密钥"""
        self.ensure_initialized()

        with self._lock:
            if 0 <= index < len(self._keys):
                return {
                    'ak': self._keys[index]['ak'],
                    'sk': self._keys[index]['sk'],
                    'index': self._keys[index]['index']
                }
            return None

    def get_all_keys(self) -> List[Dict[str, str]]:
        """获取所有密钥信息（不含SK）"""
        self.ensure_initialized()

        with self._lock:
            return [{'ak': k['ak'], 'index': k['index']} for k in self._keys]

    def get_key_count(self) -> int:
        """获取密钥组数量"""
        self.ensure_initialized()

        with self._lock:
            return len(self._keys)

    def add_key(self, ak: str, sk: str) -> int:
        """动态添加新的密钥组"""
        self.ensure_initialized()

        with self._lock:
            new_index = len(self._keys) + 1 if not self._keys else max(k['index'] for k in self._keys) + 1
            self._keys.append({'ak': ak, 'sk': sk, 'index': new_index})
            logger.info(f"已动态添加密钥组 {new_index} (AK: {ak[:10]}...)")
            return new_index

    def remove_key(self, index: int) -> bool:
        """移除指定索引的密钥组"""
        self.ensure_initialized()

        with self._lock:
            for i, key in enumerate(self._keys):
                if key['index'] == index:
                    self._keys.pop(i)
                    logger.info(f"已移除密钥组 {index}")

                    if self._current_index >= len(self._keys):
                        self._current_index = 0

                    return True
            return False

    def reload_keys(self):
        """重新加载密钥"""
        with self._lock:
            self._keys.clear()
            self._current_index = 0
            self._initialized = False
        self._load_keys()


key_manager = KeyManager()

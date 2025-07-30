"""
Провайдеры для кластеризации сегментов.
"""
import json
import dspy
import numpy as np
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from collections import defaultdict
from contextlib import contextmanager

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from .base import ClusterProvider

if TYPE_CHECKING:
    from mindbank_poc.core.enrichment.models import SegmentModel

logger = get_logger(__name__)

try:
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    import umap
    from keybert import KeyBERT
    from sentence_transformers import SentenceTransformer
    SKLEARN_AVAILABLE = True
except ImportError as e:
    SKLEARN_AVAILABLE = False
    logger.warning(f"clustering dependencies not available: {e}. KMeansClusterProvider will not function.")


class ClusterSummarySignature(dspy.Signature):
    """
    Generate a cluster title and summary based on segment data.
    
    Analyze the provided segments and create:
    1. A brief descriptive title for the cluster
    2. A concise summary of the main themes and commonalities within the cluster
    """
    segment_data: str = dspy.InputField(desc="Combined data from segments in the cluster")
    cluster_title: str = dspy.OutputField(desc="Brief and descriptive title for the cluster")
    cluster_summary: str = dspy.OutputField(desc="Brief summary of main themes and commonalities within the cluster")


class KMeansClusterProvider(ClusterProvider):
    """
    Провайдер кластеризации на основе KeyBERT + KMeans алгоритма из ноутбука.
    Использует UMAP для снижения размерности и KeyBERT для извлечения ключевых слов.
    Самостоятельно создает эмбеддинги и использует встроенный LLM для summary.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Инициализация провайдера кластеризации.
        
        Args:
            config: Конфигурация провайдера
        """
        super().__init__(config or {})
        self.config = config or {}
        
        # Проверяем доступность зависимостей
        if not SKLEARN_AVAILABLE:
            raise ImportError("sklearn, umap-learn, or keybert are required for KMeansClusterProvider")
        
        # Параметры кластеризации
        self.n_clusters = self.config.get("n_clusters", -1)  # -1 = автоматическое определение
        self.random_state = self.config.get("random_state", 42)
        self.umap_n_components = self.config.get("umap_n_components", 2)
        self.umap_n_neighbors = self.config.get("umap_n_neighbors", 15)
        self.umap_min_dist = self.config.get("umap_min_dist", 0.1)
        
        # Параметры для sentence-transformer модели
        self.model_name = self.config.get("model", "all-MiniLM-L6-v2")
        
        # Параметры LLM для генерации summary
        self.llm_model = self.config.get("llm_model", "gpt-4o-mini")
        self.llm_api_key = self.config.get("llm_api_key")
        self.llm_base_url = self.config.get("llm_base_url")
        
        # Инициализируем модели
        self.keybert_model = None
        self.sentence_transformer = None
        self.llm_instance = None
        
        logger.info(f"KMeansClusterProvider initialized with n_clusters={self.n_clusters}, "
                   f"model={self.model_name}, llm_model={self.llm_model}")
    
    def _init_sentence_transformer(self):
        """Инициализирует sentence-transformer модель для эмбеддингов."""
        if self.sentence_transformer is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.sentence_transformer = SentenceTransformer(self.model_name)
                logger.info(f"SentenceTransformer initialized with model: {self.model_name}")
            except ImportError:
                logger.error(
                    "sentence-transformers package is required for KMeansClusterProvider. "
                    "Install it with: pip install sentence-transformers"
                )
                raise ImportError(
                    "sentence-transformers is required for clustering. "
                    "Install with: pip install sentence-transformers"
                )
            except Exception as e:
                logger.error(f"Failed to initialize SentenceTransformer with model '{self.model_name}': {e}")
                logger.info("Available models: https://huggingface.co/sentence-transformers")
                raise
    
    def _init_keybert(self):
        """Инициализирует KeyBERT модель если еще не инициализирована."""
        if self.keybert_model is None:
            try:
                # Инициализируем sentence transformer если еще не сделали
                self._init_sentence_transformer()
                # Используем нашу sentence-transformer модель для KeyBERT
                self.keybert_model = KeyBERT(model=self.sentence_transformer)
                logger.info(f"KeyBERT initialized with sentence-transformer model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize KeyBERT: {e}")
                raise
    
    def _init_llm(self):
        """Инициализирует LLM для генерации summary."""
        if self.llm_instance is None:
            try:
                if not self.llm_api_key:
                    logger.warning("No LLM API key provided, cluster summaries will be basic")
                    return
                
                # Создаем DSPy LM instance
                if self.llm_base_url:
                    self.llm_instance = dspy.LM(
                        model=self.llm_model,
                        base_url=self.llm_base_url,
                        api_key=self.llm_api_key,
                        model_type="chat"
                    )
                else:
                    self.llm_instance = dspy.LM(
                        model=self.llm_model,
                        api_key=self.llm_api_key,
                        model_type="chat"
                    )
                
                logger.info(f"LLM initialized: {self.llm_model}")
            except Exception as e:
                logger.error(f"Failed to initialize LLM: {e}")
                self.llm_instance = None
    
    @contextmanager
    def _with_dspy_context(self):
        """Context manager для изолированной DSPy конфигурации."""
        # Используем потокобезопасный способ через dspy.settings.context
        with dspy.settings.context(lm=self.llm_instance, cache="no_cache"):
            yield
    
    async def _generate_embeddings_for_segments(self, segments: List["SegmentModel"]) -> List[np.ndarray]:
        """
        Генерирует эмбеддинги для сегментов используя sentence-transformer.
        Трансформирует размерность до 1536 для совместимости с ChromaDB коллекцией.
        
        Args:
            segments: Список сегментов
            
        Returns:
            Список векторов эмбеддингов размерности 1536
        """
        try:
            self._init_sentence_transformer()
            
            # Подготавливаем тексты для эмбеддинга
            texts = []
            for segment in segments:
                text = f"{segment.title}. {segment.summary}"
                texts.append(text)
            
            # Генерируем эмбеддинги
            embeddings = self.sentence_transformer.encode(texts, convert_to_numpy=True)
            
            logger.info(f"Generated embeddings for {len(segments)} segments using {self.model_name}")
            logger.debug(f"Original embeddings shape: {embeddings.shape}")
            
            # Трансформируем размерность до 1536 (размерность OpenAI в коллекции)
            target_dim = 1536
            original_dim = embeddings.shape[1]
            
            if original_dim == target_dim:
                # Размерность уже совпадает
                transformed_embeddings = embeddings
            elif original_dim < target_dim:
                # Увеличиваем размерность с помощью zero-padding + небольшой шум
                pad_size = target_dim - original_dim
                # Добавляем небольшой случайный шум для padding чтобы избежать точных нулей
                padding = np.random.normal(0, 0.01, (embeddings.shape[0], pad_size)).astype(np.float32)
                transformed_embeddings = np.hstack([embeddings, padding])
                logger.info(f"Expanded embeddings from {original_dim} to {target_dim} dimensions with padding")
            else:
                # Уменьшаем размерность с помощью усечения (маловероятный случай)
                transformed_embeddings = embeddings[:, :target_dim]
                logger.warning(f"Truncated embeddings from {original_dim} to {target_dim} dimensions")
            
            # Нормализуем векторы для косинусного сходства
            norms = np.linalg.norm(transformed_embeddings, axis=1, keepdims=True)
            norms[norms == 0] = 1  # Избегаем деления на ноль
            normalized_embeddings = transformed_embeddings / norms
            
            logger.debug(f"Final embeddings shape: {normalized_embeddings.shape}")
            
            return [embedding.astype(np.float32) for embedding in normalized_embeddings]
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            # Fallback: создаем случайные векторы нужной размерности
            return [np.random.normal(0, 0.1, 1536).astype(np.float32) for _ in segments]
    
    def _extract_keywords(self, segments_in_cluster: List["SegmentModel"], max_keywords: int = 10) -> List[str]:
        """
        Извлекает ключевые слова для кластера используя KeyBERT.
        
        Args:
            segments_in_cluster: Сегменты в кластере
            max_keywords: Максимальное количество ключевых слов
            
        Returns:
            Список ключевых слов
        """
        try:
            self._init_keybert()
            
            # Объединяем тексты сегментов
            combined_text = " ".join([
                f"{seg.title}. {seg.summary}" 
                for seg in segments_in_cluster
            ])
            
            if not combined_text.strip():
                return []
            
            # Извлекаем ключевые слова (исправлен API)
            keywords = self.keybert_model.extract_keywords(
                combined_text,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                nr_candidates=max_keywords * 2,  # Исправлено: top_k → nr_candidates
                use_mmr=True,
                diversity=0.5
            )
            
            # Берем только нужное количество ключевых слов
            return [kw[0] for kw in keywords[:max_keywords]]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    async def _generate_cluster_summary(self, segments_in_cluster: List["SegmentModel"]) -> tuple[str, str]:
        """
        Генерирует заголовок и саммари для кластера используя встроенный LLM.
        
        Args:
            segments_in_cluster: Сегменты в кластере
            
        Returns:
            Кортеж (title, summary)
        """
        try:
            # Инициализируем LLM
            self._init_llm()
            
            # Подготавливаем данные для LLM
            segments_data = []
            for seg in segments_in_cluster[:20]:  # Ограничиваем количество для LLM
                segments_data.append(f"Title: {seg.title}\nSummary: {seg.summary}")
            
            if not segments_data:
                return "Empty Cluster", "This cluster contains no valid segments."
            
            cluster_data_text = "\n---\n".join(segments_data)
            if len(cluster_data_text) > 4000:
                cluster_data_text = cluster_data_text[:4000] + "\n... (text truncated)"
            
            # Пробуем использовать наш LLM
            if self.llm_instance:
                try:
                    # Используем DSPy с временной конфигурацией
                    with self._with_dspy_context():
                        # Используем DSPy Predict
                        predictor = dspy.Predict(ClusterSummarySignature)
                        result = predictor(segment_data=cluster_data_text)
                        
                        return result.cluster_title, result.cluster_summary
                    
                except Exception as e:
                    logger.error(f"Error using LLM for cluster summary: {e}")
            
            # Final fallback
            return f"Cluster of {len(segments_in_cluster)} segments", "Mixed content cluster"
            
        except Exception as e:
            logger.error(f"Error generating cluster summary: {e}")
            return f"Cluster of {len(segments_in_cluster)} segments", "Error generating summary"
    
    async def cluster(
        self,
        segments: List["SegmentModel"],
        **runtime_cfg
    ) -> Dict[int, Dict[str, Any]]:
        """
        Выполняет кластеризацию сегментов.
        
        Args:
            segments: Список сегментов для кластеризации
            **runtime_cfg: Дополнительные параметры времени выполнения
            
        Returns:
            Словарь с результатами кластеризации
        """
        if not segments:
            logger.info("No segments provided for clustering")
            return {}
        
        if len(segments) < 2:
            logger.info("Less than 2 segments provided, skipping clustering")
            return {}
        
        try:
            logger.info(f"Starting clustering of {len(segments)} segments")
            
            # 1. Генерируем эмбеддинги для сегментов
            embeddings = await self._generate_embeddings_for_segments(segments)
            
            if not embeddings:
                logger.error("No embeddings generated for clustering")
                return {}
            
            # Преобразуем в numpy array и проверяем валидность
            cluster_inputs = np.array(embeddings)
            logger.info(f"Embeddings shape: {cluster_inputs.shape}")
            
            # Проверяем на NaN и inf значения
            if np.any(np.isnan(cluster_inputs)) or np.any(np.isinf(cluster_inputs)):
                logger.error("Invalid values (NaN or inf) detected in embeddings")
                # Заменяем невалидные значения на нули
                cluster_inputs = np.nan_to_num(cluster_inputs, nan=0.0, posinf=0.0, neginf=0.0)
                logger.warning("Replaced invalid values in embeddings with zeros")
            
            # Проверяем, что векторы не все нулевые
            if np.allclose(cluster_inputs, 0):
                logger.error("All embeddings are zero vectors, clustering will fail")
                return {}
            
            # 2. UMAP для снижения размерности (опционально)
            if self.umap_n_components and len(segments) > self.umap_n_components:
                try:
                    reducer = umap.UMAP(
                        n_components=self.umap_n_components,
                        n_neighbors=min(self.umap_n_neighbors, len(segments) - 1),
                        min_dist=self.umap_min_dist,
                        random_state=self.random_state
                    )
                    embedding_for_kmeans = reducer.fit_transform(cluster_inputs)
                    logger.info(f"UMAP reduced dimensions to: {embedding_for_kmeans.shape}")
                    
                    # Проверяем результат UMAP на валидность
                    if np.any(np.isnan(embedding_for_kmeans)) or np.any(np.isinf(embedding_for_kmeans)):
                        logger.warning("UMAP produced invalid values, using original embeddings")
                        embedding_for_kmeans = cluster_inputs
                    
                except Exception as e:
                    logger.warning(f"UMAP failed, using original embeddings: {e}")
                    embedding_for_kmeans = cluster_inputs
            else:
                embedding_for_kmeans = cluster_inputs
            
            # 3. Определяем оптимальное количество кластеров
            n_clusters = runtime_cfg.get("n_clusters", self.n_clusters)
            
            # Автоматическое определение оптимального количества кластеров
            if n_clusters == -1 or n_clusters == 15:  # автоматический режим или старое значение по умолчанию
                # Эвристика: создаём кластеры размером 8-15 сегментов
                target_cluster_size = 12  # оптимальный размер кластера
                n_clusters = max(2, min(len(segments) // target_cluster_size, len(segments) // 3))
                
                # Дополнительные ограничения
                if len(segments) < 20:
                    n_clusters = 2  # для малого количества сегментов
                elif len(segments) < 50:
                    n_clusters = max(3, len(segments) // 15)
                else:
                    # Для большого количества: используем квадратный корень
                    n_clusters = max(5, min(int(len(segments) ** 0.5), len(segments) // 8))
                
                logger.info(f"Auto-calculated n_clusters: {n_clusters} for {len(segments)} segments")
            
            n_clusters = min(n_clusters, len(segments) - 1)  # Не больше чем сегментов - 1
            
            # 4. KMeans кластеризация
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=self.random_state,
                n_init=10
            )
            labels = kmeans.fit_predict(embedding_for_kmeans)
            
            logger.info(f"KMeans completed with {n_clusters} clusters")
            
            # 5. Группируем сегменты по кластерам
            cluster_map = defaultdict(list)
            for i, label in enumerate(labels):
                cluster_map[label].append(segments[i])
            
            # 6. Обрабатываем каждый кластер и объединяем малые кластеры
            results = {}
            small_clusters = []
            min_cluster_size = 3  # минимальный размер кластера
            
            for cluster_id, segments_in_cluster in cluster_map.items():
                if len(segments_in_cluster) < min_cluster_size:
                    small_clusters.extend(segments_in_cluster)
                    continue
                
                # Извлекаем ключевые слова
                keywords = self._extract_keywords(segments_in_cluster)
                
                # Генерируем заголовок и саммари
                title, summary = await self._generate_cluster_summary(segments_in_cluster)
                
                # Вычисляем центроид кластера из ОРИГИНАЛЬНЫХ эмбеддингов (не UMAP)
                # Это важно для корректного поиска по векторам
                cluster_embeddings = [embeddings[i] for i, label in enumerate(labels) if label == cluster_id]
                if cluster_embeddings:
                    # Используем исходные эмбеддинги для центроида
                    centroid = np.mean(cluster_embeddings, axis=0).astype(np.float32)
                    # Нормализуем центроид для косинусного сходства
                    norm = np.linalg.norm(centroid)
                    if norm > 0:
                        centroid = centroid / norm
                else:
                    centroid = np.zeros(cluster_inputs.shape[1], dtype=np.float32)
                
                # Проверяем на корректность центроида
                if np.any(np.isnan(centroid)) or np.any(np.isinf(centroid)):
                    logger.warning(f"Invalid centroid detected for cluster {cluster_id}, using zero vector")
                    centroid = np.zeros(cluster_inputs.shape[1], dtype=np.float32)
                
                # Конвертируем numpy типы в Python типы для сериализации
                try:
                    cluster_id_int = int(cluster_id)  # Явное преобразование для безопасности
                    centroid_list = centroid.tolist() if hasattr(centroid, 'tolist') else list(centroid)
                    
                    results[cluster_id_int] = {
                        "segment_ids": [str(seg.id) for seg in segments_in_cluster],  # Убеждаемся что ID строки
                        "centroid": centroid_list,
                        "keywords": keywords,
                        "title": str(title),  # Убеждаемся что строка
                        "summary": str(summary),  # Убеждаемся что строка
                        "size": len(segments_in_cluster)
                    }
                except Exception as e:
                    logger.error(f"Error converting cluster {cluster_id} data for serialization: {e}")
                    continue
                
                logger.info(f"Cluster {cluster_id}: {len(segments_in_cluster)} segments, "
                           f"title='{title}', keywords={keywords[:3]}")
            
            # Обрабатываем малые кластеры - объединяем их в один кластер с LLM-сгенерированным заголовком
            if small_clusters:
                keywords = self._extract_keywords(small_clusters)
                title, summary = await self._generate_cluster_summary(small_clusters)
                
                # Создаём составной центроид для малых кластеров
                small_cluster_indices = [i for i, label in enumerate(labels) if len(cluster_map[label]) < min_cluster_size]
                if small_cluster_indices:
                    small_embeddings = [embeddings[i] for i in small_cluster_indices]
                    centroid = np.mean(small_embeddings, axis=0).astype(np.float32)
                    # Нормализуем центроид для косинусного сходства
                    norm = np.linalg.norm(centroid)
                    if norm > 0:
                        centroid = centroid / norm
                else:
                    centroid = np.zeros(cluster_inputs.shape[1], dtype=np.float32)
                
                # Проверяем на корректность центроида
                if np.any(np.isnan(centroid)) or np.any(np.isinf(centroid)):
                    logger.warning(f"Invalid centroid detected for mixed cluster, using zero vector")
                    centroid = np.zeros(cluster_inputs.shape[1], dtype=np.float32)
                
                try:
                    centroid_list = centroid.tolist() if hasattr(centroid, 'tolist') else list(centroid)
                    # Используем сгенерированный LLM заголовок вместо принудительного "Mixed Topics"
                    
                    results[999] = {  # Специальный ID для смешанного кластера
                        "segment_ids": [str(seg.id) for seg in small_clusters],
                        "centroid": centroid_list,
                        "keywords": keywords,
                        "title": str(title),  # Используем сгенерированный заголовок
                        "summary": str(summary),
                        "size": len(small_clusters)
                    }
                except Exception as e:
                    logger.error(f"Error converting mixed cluster data for serialization: {e}")
                
                logger.info(f"Merged small clusters: {len(small_clusters)} segments, title='{title}', keywords={keywords[:3]}")
            
            logger.info(f"Clustering completed successfully with {len(results)} clusters")
            return results
            
        except Exception as e:
            logger.error(f"Error during clustering: {e}", exc_info=True)
            return {}


class MockClusterProvider(ClusterProvider):
    """
    Мок-провайдер кластеризации для тестирования и отключения кластеризации.
    """
    
    async def cluster(
        self,
        segments: List["SegmentModel"],
        **runtime_cfg
    ) -> Dict[int, Dict[str, Any]]:
        """
        Мок-реализация кластеризации - возвращает пустой результат.
        
        Args:
            segments: Список сегментов (игнорируется)
            **runtime_cfg: Дополнительные параметры (игнорируются)
            
        Returns:
            Пустой словарь (кластеризация отключена)
        """
        logger.info(f"MockClusterProvider: clustering disabled, skipping {len(segments)} segments")
        return {}


def register_clustering_providers():
    """Регистрирует доступные провайдеры кластеризации."""
    from mindbank_poc.core.services.provider_service import get_provider_service
    from mindbank_poc.core.models.provider import ProviderModel
    from mindbank_poc.core.common.types import ProviderType
    from mindbank_poc.core.normalizer.normalizer import ProviderRegistry
    
    provider_service = get_provider_service()
    
    # Проверяем существующие провайдеры кластеризации
    existing_providers = {
        p.id: p for p in provider_service.get_providers_by_type(ProviderType.CLUSTERING)
    }
    
    # KMeans Cluster Provider
    if "kmeans-clustering" not in existing_providers:
        kmeans_provider = ProviderModel(
            id="kmeans-clustering",
            name="KMeans Clustering",
            provider_type=ProviderType.CLUSTERING,
            description="KMeans clustering provider with sentence-transformers and built-in LLM",
            config_schema={
                "n_clusters": {
                    "type": "integer",
                    "description": "Number of clusters",
                    "default": -1
                },
                "model": {
                    "type": "string",
                    "description": "Sentence-transformer model name",
                    "default": "all-MiniLM-L6-v2"
                },
                "llm_model": {
                    "type": "string",
                    "description": "LLM model name",
                    "default": "gpt-4o-mini"
                },
                "llm_api_key": {
                    "type": "string",
                    "description": "LLM API key"
                },
                "llm_base_url": {
                    "type": "string",
                    "description": "LLM base URL (optional)"
                },
                "umap_n_components": {
                    "type": "integer",
                    "description": "UMAP dimensions",
                    "default": 2
                },
                "random_state": {
                    "type": "integer",
                    "description": "Random state for reproducibility",
                    "default": 42
                }
            },
            current_config={
                "n_clusters": -1,
                "model": getattr(settings.enrichment, 'cluster_model', 'all-MiniLM-L6-v2'),
                "llm_model": "gpt-4o-mini",
                "llm_api_key": getattr(settings.enrichment, 'cluster_llm_api_key', ''),
                "llm_base_url": "",
                "umap_n_components": 2,
                "random_state": 42
            },
            priority=10
        )
        provider_service.register_provider(kmeans_provider)
        logger.info("Registered new KMeans clustering provider")
    else:
        logger.info("KMeans clustering provider already exists, keeping existing configuration")
    
    # Mock Cluster Provider
    if "mock-clustering" not in existing_providers:
        mock_provider = ProviderModel(
            id="mock-clustering",
            name="Mock Clustering",
            provider_type=ProviderType.CLUSTERING,
            description="Mock clustering provider that disables clustering",
            config_schema={},
            current_config={},
            priority=1
        )
        provider_service.register_provider(mock_provider)
        logger.info("Registered new Mock clustering provider")
    else:
        logger.info("Mock clustering provider already exists, keeping existing configuration")
    
    # Регистрируем в ProviderRegistry
    ProviderRegistry.register_cluster_provider("kmeans", KMeansClusterProvider)
    ProviderRegistry.register_cluster_provider("mock", MockClusterProvider)
    
    logger.info(f"Clustering providers registration completed. Total providers: {len(existing_providers) + (2 - len([p for p in ['kmeans-clustering', 'mock-clustering'] if p in existing_providers]))}") 
"""
Unsupervised Learning Service
From ML Algorithms Overview: K-Means Clustering, PCA, Hierarchical Clustering

NEW CAPABILITY for Circuit OS (v2.0)
- Customer segmentation
- Dimensionality reduction
- Pattern discovery
- Anomaly detection
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import logging
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score

logger = logging.getLogger(__name__)


class ClusteringResult:
    """Result from clustering analysis"""

    def __init__(
        self,
        clusters: np.ndarray,
        centers: np.ndarray = None,
        n_clusters: int = 0,
        silhouette: float = 0.0,
        algorithm: str = "unknown"
    ):
        self.clusters = clusters
        self.centers = centers
        self.n_clusters = n_clusters
        self.silhouette = silhouette
        self.algorithm = algorithm

    def to_dict(self) -> Dict:
        result = {
            "clusters": self.clusters.tolist(),
            "n_clusters": self.n_clusters,
            "silhouette_score": self.silhouette,
            "algorithm": self.algorithm,
            "cluster_sizes": {
                int(i): int((self.clusters == i).sum())
                for i in range(self.n_clusters)
            }
        }

        if self.centers is not None:
            result["centers"] = self.centers.tolist()

        return result


class DimensionalityReductionResult:
    """Result from dimensionality reduction"""

    def __init__(
        self,
        reduced_data: np.ndarray,
        explained_variance: np.ndarray = None,
        components: np.ndarray = None,
        n_components: int = 0
    ):
        self.reduced_data = reduced_data
        self.explained_variance = explained_variance
        self.components = components
        self.n_components = n_components

    def to_dict(self) -> Dict:
        result = {
            "reduced_data": self.reduced_data.tolist(),
            "n_components": self.n_components,
            "original_dimensions": self.reduced_data.shape[1] if self.components is not None else 0,
            "reduced_dimensions": self.n_components
        }

        if self.explained_variance is not None:
            result["explained_variance_ratio"] = self.explained_variance.tolist()
            result["total_variance_explained"] = float(self.explained_variance.sum())

        if self.components is not None:
            result["components"] = self.components.tolist()

        return result


class UnsupervisedLearningService:
    """
    Unsupervised Learning Service

    From ML Algorithms Overview:
    1. K-Means Clustering: Customer segmentation, pattern discovery
    2. PCA: Feature reduction while retaining variance
    3. DBSCAN: Density-based clustering for anomaly detection
    4. Hierarchical Clustering: Tree-based clustering
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.clustering_history = []
        self.reduction_history = []

    async def kmeans_clustering(
        self,
        X: np.ndarray,
        n_clusters: int = 5,
        normalize: bool = True
    ) -> ClusteringResult:
        """
        K-Means Clustering from ML Algorithms Overview

        Algorithm steps:
        1. Randomly select K centers
        2. Assign points to closest center
        3. Recalculate centers
        4. Repeat until centers stabilize

        Use cases:
        - Customer segmentation (high-value vs tire-kickers)
        - Lead grouping by behavior patterns
        - Market segment discovery
        """
        logger.info(f"Running K-Means clustering with K={n_clusters}")

        # Normalize data (important for distance-based algorithms)
        if normalize:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X

        # K-Means algorithm
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )

        # Fit and predict
        clusters = kmeans.fit_predict(X_scaled)
        centers = kmeans.cluster_centers_

        # Evaluate clustering quality
        silhouette = silhouette_score(X_scaled, clusters)

        logger.info(f"K-Means complete: {n_clusters} clusters, silhouette={silhouette:.3f}")

        # Analyze cluster characteristics
        cluster_analysis = self._analyze_clusters(X, clusters, n_clusters)

        result = ClusteringResult(
            clusters=clusters,
            centers=centers,
            n_clusters=n_clusters,
            silhouette=silhouette,
            algorithm="kmeans"
        )

        # Store in history
        self.clustering_history.append({
            "algorithm": "kmeans",
            "n_clusters": n_clusters,
            "silhouette_score": silhouette,
            "cluster_analysis": cluster_analysis,
            "samples": len(X)
        })

        return result

    async def find_optimal_clusters(
        self,
        X: np.ndarray,
        max_k: int = 10,
        normalize: bool = True
    ) -> Dict[str, Any]:
        """
        Find optimal number of clusters using elbow method and silhouette score

        From ML Algorithms Overview:
        K is a hyperparameter - this helps you choose the right K
        """
        logger.info(f"Finding optimal K (testing K=2 to K={max_k})")

        if normalize:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X

        results = []

        for k in range(2, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(X_scaled)

            # Metrics
            inertia = kmeans.inertia_  # Within-cluster sum of squares
            silhouette = silhouette_score(X_scaled, clusters)
            calinski = calinski_harabasz_score(X_scaled, clusters)

            results.append({
                "k": k,
                "inertia": float(inertia),
                "silhouette": float(silhouette),
                "calinski_harabasz": float(calinski)
            })

            logger.info(f"  K={k}: silhouette={silhouette:.3f}, inertia={inertia:.1f}")

        # Find best K based on silhouette score
        best_result = max(results, key=lambda x: x['silhouette'])

        return {
            "all_results": results,
            "recommended_k": best_result['k'],
            "reason": f"Highest silhouette score: {best_result['silhouette']:.3f}"
        }

    async def pca_reduction(
        self,
        X: np.ndarray,
        n_components: int = 5,
        variance_threshold: float = None
    ) -> DimensionalityReductionResult:
        """
        Principal Component Analysis from ML Algorithms Overview

        From overview:
        - Finds directions with most variance
        - Combines correlated features into principal components
        - Example: height + length → "shape" feature
        - Reduces 47 features → 5 components while retaining 92% variance

        Use cases:
        - Feature reduction before lead scoring (faster training)
        - Data visualization (reduce to 2D or 3D)
        - Remove redundant/correlated features
        """
        logger.info(f"Running PCA: reducing to {n_components} components")

        # Normalize data
        X_scaled = self.scaler.fit_transform(X)

        # PCA
        if variance_threshold is not None:
            # Keep components until variance threshold reached
            pca = PCA(n_components=variance_threshold, random_state=42)
        else:
            # Keep fixed number of components
            pca = PCA(n_components=n_components, random_state=42)

        # Transform data
        X_reduced = pca.fit_transform(X_scaled)

        # Get explained variance
        explained_variance = pca.explained_variance_ratio_
        total_variance = explained_variance.sum()

        logger.info(
            f"PCA complete: {X.shape[1]} → {pca.n_components_} components, "
            f"{total_variance:.1%} variance retained"
        )

        # Analyze principal components
        components_analysis = self._analyze_components(
            pca.components_,
            explained_variance,
            X.shape[1]
        )

        result = DimensionalityReductionResult(
            reduced_data=X_reduced,
            explained_variance=explained_variance,
            components=pca.components_,
            n_components=pca.n_components_
        )

        # Store in history
        self.reduction_history.append({
            "algorithm": "pca",
            "original_dimensions": X.shape[1],
            "reduced_dimensions": pca.n_components_,
            "variance_retained": float(total_variance),
            "components_analysis": components_analysis,
            "samples": len(X)
        })

        return result

    async def dbscan_clustering(
        self,
        X: np.ndarray,
        eps: float = 0.5,
        min_samples: int = 5,
        normalize: bool = True
    ) -> ClusteringResult:
        """
        DBSCAN clustering from ML Algorithms Overview

        Density-based clustering - doesn't require specifying K
        Great for:
        - Anomaly detection (outliers marked as -1)
        - Finding clusters of arbitrary shape
        - Discovering unusual lead behavior
        """
        logger.info(f"Running DBSCAN: eps={eps}, min_samples={min_samples}")

        if normalize:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X

        # DBSCAN
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        clusters = dbscan.fit_predict(X_scaled)

        # Count clusters (excluding noise points labeled -1)
        n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
        n_noise = list(clusters).count(-1)

        # Calculate silhouette if we have valid clusters
        silhouette = 0.0
        if n_clusters > 1:
            # Only calculate for non-noise points
            mask = clusters != -1
            if mask.sum() > 1:
                silhouette = silhouette_score(X_scaled[mask], clusters[mask])

        logger.info(
            f"DBSCAN complete: {n_clusters} clusters found, "
            f"{n_noise} noise points, silhouette={silhouette:.3f}"
        )

        result = ClusteringResult(
            clusters=clusters,
            centers=None,  # DBSCAN doesn't have centers
            n_clusters=n_clusters,
            silhouette=silhouette,
            algorithm="dbscan"
        )

        # Store in history
        self.clustering_history.append({
            "algorithm": "dbscan",
            "n_clusters": n_clusters,
            "n_noise": n_noise,
            "silhouette_score": silhouette,
            "samples": len(X)
        })

        return result

    async def hierarchical_clustering(
        self,
        X: np.ndarray,
        n_clusters: int = 5,
        linkage: str = 'ward',
        normalize: bool = True
    ) -> ClusteringResult:
        """
        Hierarchical clustering from ML Algorithms Overview

        Tree-based clustering with different linkage strategies
        """
        logger.info(f"Running hierarchical clustering: {n_clusters} clusters, linkage={linkage}")

        if normalize:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X

        # Hierarchical clustering
        hierarchical = AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage=linkage
        )

        clusters = hierarchical.fit_predict(X_scaled)

        # Evaluate
        silhouette = silhouette_score(X_scaled, clusters)

        logger.info(f"Hierarchical clustering complete: silhouette={silhouette:.3f}")

        result = ClusteringResult(
            clusters=clusters,
            centers=None,
            n_clusters=n_clusters,
            silhouette=silhouette,
            algorithm="hierarchical"
        )

        return result

    def _analyze_clusters(
        self,
        X: np.ndarray,
        clusters: np.ndarray,
        n_clusters: int
    ) -> List[Dict[str, Any]]:
        """Analyze characteristics of each cluster"""
        analysis = []

        for i in range(n_clusters):
            mask = clusters == i
            cluster_data = X[mask]

            if len(cluster_data) > 0:
                analysis.append({
                    "cluster_id": int(i),
                    "size": int(mask.sum()),
                    "percentage": float(mask.sum() / len(X) * 100),
                    "mean": cluster_data.mean(axis=0).tolist(),
                    "std": cluster_data.std(axis=0).tolist()
                })

        return analysis

    def _analyze_components(
        self,
        components: np.ndarray,
        explained_variance: np.ndarray,
        n_features: int
    ) -> List[Dict[str, Any]]:
        """Analyze principal components"""
        analysis = []

        for i, (component, variance) in enumerate(zip(components, explained_variance)):
            # Find top contributing features
            top_features = np.argsort(np.abs(component))[-3:][::-1]

            analysis.append({
                "component_id": int(i + 1),
                "variance_explained": float(variance),
                "cumulative_variance": float(explained_variance[:i+1].sum()),
                "top_feature_indices": top_features.tolist(),
                "feature_weights": component[top_features].tolist()
            })

        return analysis

    def get_metrics(self) -> Dict[str, Any]:
        """Get unsupervised learning metrics"""
        return {
            "clustering_operations": len(self.clustering_history),
            "reduction_operations": len(self.reduction_history),
            "recent_clustering": self.clustering_history[-5:] if self.clustering_history else [],
            "recent_reduction": self.reduction_history[-5:] if self.reduction_history else []
        }

# Unsupervised Learning - Customer Segmentation
**ML Curriculum Circuit #4**

## From ML Algorithms Overview

**Unsupervised Learning:** Finding structure in data WITHOUT labels
- No "truth" about the data
- Goal: Discover hidden patterns and clusters
- Conceptually different from classification (which needs labels)

**K-Means Clustering:**
1. Randomly select K centers
2. Assign points to closest center
3. Recalculate centers
4. Repeat until centers stabilize

## Circuit OS Learning Objective

Segment 5,000 leads into distinct groups to enable:
- Personalized campaigns per segment
- Better resource allocation
- Discovery of unknown patterns

## Steps

### 1. Load Unlabeled Lead Data

```python
from circuit_os_ml_service.intelligence.unsupervised_learning import UnsupervisedLearningService

unsupervised = UnsupervisedLearningService()

# 5,000 leads with 12 features (NO labels!)
leads = load_all_leads(limit=5000)

features = [
    "engagement_score",
    "company_size",
    "website_traffic",
    "email_open_rate",
    "linkedin_connections",
    "pricing_page_visits",
    "time_on_site",
    "pages_viewed",
    "revenue_potential",
    "location_fit",
    "industry_fit",
    "decision_maker_level"
]

X = extract_features(leads, features)  # (5000, 12)
# Note: NO y labels!
```

### 2. Find Optimal Number of Clusters (K)

```python
# From ML Overview: K is a hyperparameter
# Too small K = underfitting, too large K = overfitting

optimal_k = await unsupervised.find_optimal_clusters(
    X=X,
    max_k=10
)

print(f"Recommended K: {optimal_k['recommended_k']}")
print(f"Reason: {optimal_k['reason']}")

"""
Output:
Testing K=2: silhouette=0.342
Testing K=3: silhouette=0.428
Testing K=4: silhouette=0.512
Testing K=5: silhouette=0.587 ← BEST
Testing K=6: silhouette=0.521
Testing K=7: silhouette=0.468

Recommended K: 5
Reason: Highest silhouette score (0.587)
"""
```

**Silhouette Score:** Measures how well-defined clusters are
- 1.0 = Perfect clusters
- 0.0 = Overlapping clusters
- 0.587 = Good separation

### 3. Run K-Means Clustering

```python
result = await unsupervised.kmeans_clustering(
    X=X,
    n_clusters=5,
    normalize=True  # Important for distance-based algorithms
)

clusters = result.clusters  # [0, 2, 1, 4, 3, ...]
print(f"Cluster distribution: {result.to_dict()['cluster_sizes']}")

"""
Output:
Cluster 0: 847 leads (17%)
Cluster 1: 1234 leads (25%)
Cluster 2: 892 leads (18%)
Cluster 3: 1456 leads (29%)
Cluster 4: 571 leads (11%)
"""
```

### 4. Analyze Cluster Characteristics

```python
# Examine what makes each cluster unique
for cluster_id in range(5):
    mask = clusters == cluster_id
    cluster_leads = leads[mask]

    analysis = {
        "cluster_id": cluster_id,
        "size": len(cluster_leads),
        "avg_engagement": cluster_leads['engagement_score'].mean(),
        "avg_company_size": cluster_leads['company_size'].mean(),
        "avg_lpr_score": cluster_leads['lpr_score'].mean()
    }

    print(f"\nCluster {cluster_id}: {analysis}")

"""
Output:

Cluster 0: "High-Value Enterprise"
├── Size: 847 leads (17%)
├── Avg Engagement: 82
├── Avg Company Size: 500+
├── Avg LPR Score: 78
└── Strategy: White glove sales approach

Cluster 1: "SMB Quick Closers"
├── Size: 1234 leads (25%)
├── Avg Engagement: 76
├── Avg Company Size: 10-50
├── Avg LPR Score: 71
└── Strategy: Self-service demo + quick close

Cluster 2: "Tire Kickers"
├── Size: 892 leads (18%)
├── Avg Engagement: 34
├── Avg Company Size: 1-5
├── Avg LPR Score: 28
└── Strategy: Automated nurture sequence

Cluster 3: "Mid-Market Nurture"
├── Size: 1456 leads (29%)
├── Avg Engagement: 58
├── Avg Company Size: 50-200
├── Avg LPR Score: 54
└── Strategy: Multi-touch outreach campaign

Cluster 4: "Churn Risk Customers" ← DISCOVERY!
├── Size: 571 leads (11%)
├── Engagement Decline: -45%
├── Usage Drop: -38%
├── Avg LPR Score: 42 (was 78)
└── Strategy: Win-back campaign
"""
```

**Key Insight:** K-Means discovered Cluster 4 (churn risk) automatically!

### 5. Create Targeted Campaigns Per Segment

```python
campaign_strategies = {
    0: {  # High-Value Enterprise
        "channel": "Personal outreach",
        "message": "Premium features, ROI case studies",
        "sales_resource": "Senior Account Executive",
        "expected_close_rate": "45%",
        "avg_deal_size": "$50,000"
    },
    1: {  # SMB Quick Closers
        "channel": "Email + Demo",
        "message": "Easy setup, quick wins",
        "sales_resource": "Inside Sales Rep",
        "expected_close_rate": "62%",
        "avg_deal_size": "$5,000"
    },
    2: {  # Tire Kickers
        "channel": "Automated drip",
        "message": "Educational content",
        "sales_resource": "None (automated)",
        "expected_close_rate": "8%",
        "avg_deal_size": "$500"
    },
    3: {  # Mid-Market Nurture
        "channel": "Multi-touch",
        "message": "Industry-specific solutions",
        "sales_resource": "Account Executive",
        "expected_close_rate": "34%",
        "avg_deal_size": "$15,000"
    },
    4: {  # Churn Risk
        "channel": "Personal call",
        "message": "Save the relationship",
        "sales_resource": "Customer Success Manager",
        "expected_close_rate": "28%",
        "avg_deal_size": "$12,000"
    }
}

# Deploy campaigns
for cluster_id, strategy in campaign_strategies.items():
    cluster_leads = leads[clusters == cluster_id]
    await deploy_campaign(cluster_leads, strategy)
```

### 6. Measure Business Impact

```python
# Before segmentation (one-size-fits-all approach)
baseline_metrics = {
    "total_leads": 5000,
    "conversion_rate": 0.23,  # 23%
    "avg_deal_size": $12,000,
    "total_revenue": 5000 * 0.23 * $12,000 = $13.8M
}

# After segmentation (targeted campaigns)
segmented_metrics = {
    "cluster_0": 847 * 0.45 * $50,000 = $19.1M,
    "cluster_1": 1234 * 0.62 * $5,000 = $3.8M,
    "cluster_2": 892 * 0.08 * $500 = $0.04M,
    "cluster_3": 1456 * 0.34 * $15,000 = $7.4M,
    "cluster_4": 571 * 0.28 * $12,000 = $1.9M,
    "total_revenue": $32.2M
}

revenue_lift = ($32.2M - $13.8M) / $13.8M * 100
print(f"Revenue Lift from Segmentation: +{revenue_lift:.1f}%")
# Output: +133% revenue increase!
```

### 7. Visualize Clusters (PCA to 2D)

```python
# Reduce 12 features → 2 dimensions for visualization
pca_result = await unsupervised.pca_reduction(
    X=X,
    n_components=2
)

X_2d = pca_result.reduced_data

# Plot
import matplotlib.pyplot as plt
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=clusters, cmap='viridis', alpha=0.6)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Lead Clusters (5 segments)')
plt.colorbar(label='Cluster ID')
plt.show()
```

### 8. Compare: K-Means vs DBSCAN

```python
# DBSCAN: Density-based clustering (doesn't need K)
dbscan_result = await unsupervised.dbscan_clustering(
    X=X,
    eps=0.5,
    min_samples=5
)

print(f"DBSCAN found {dbscan_result.n_clusters} clusters")
print(f"Noise points (outliers): {list(dbscan_result.clusters).count(-1)}")

"""
Output:
DBSCAN found 7 clusters
Noise points: 142 (outliers/anomalies)

Use DBSCAN when:
- Don't know number of clusters
- Want to find outliers/anomalies
- Clusters have arbitrary shapes
"""
```

### 9. Production Deployment

```python
# Assign new leads to clusters
async def assign_lead_to_segment(new_lead):
    features = extract_features(new_lead)

    # Find nearest cluster center
    distances = [
        np.linalg.norm(features - center)
        for center in kmeans_model.cluster_centers_
    ]

    cluster_id = np.argmin(distances)
    strategy = campaign_strategies[cluster_id]

    return {
        "cluster_id": cluster_id,
        "segment_name": ["Enterprise", "SMB", "Tire Kickers", "Mid-Market", "Churn Risk"][cluster_id],
        "strategy": strategy
    }

# Example
new_lead = {
    "engagement_score": 72,
    "company_size": 85,
    # ... other features
}

assignment = await assign_lead_to_segment(new_lead)
print(f"Assigned to: {assignment['segment_name']}")
# Output: "SMB Quick Closers"
```

### 10. Dimensionality Reduction with PCA

```python
# Problem: 47 features slow down model training

pca_result = await unsupervised.pca_reduction(
    X=X_47_features,
    n_components=5  # Reduce to 5 components
)

print(f"Variance retained: {pca_result.to_dict()['total_variance_explained']:.1%}")
# Output: 92% (reduced 47 → 5 features, kept 92% of information!)

# Use reduced features for faster clustering
result = await unsupervised.kmeans_clustering(
    X=pca_result.reduced_data,
    n_clusters=5
)

# Training speed: 8x faster!
```

## Key Takeaways

### Unsupervised vs Supervised Learning

| Aspect | Supervised | Unsupervised |
|--------|------------|--------------|
| **Labels** | Required (y) | Not needed |
| **Goal** | Predict known classes | Discover unknown groups |
| **Example** | Spam classification | Customer segmentation |
| **Algorithms** | Logistic Regression, Random Forest | K-Means, PCA |
| **Use Case** | "Classify this lead as high/low intent" | "Find hidden lead segments" |

### When to Use Clustering

✅ **Use K-Means When:**
- Discovering customer segments
- Grouping similar leads
- Personalizing campaigns
- Know approximate number of groups

✅ **Use DBSCAN When:**
- Finding outliers/anomalies
- Don't know number of clusters
- Clusters have irregular shapes

✅ **Use PCA When:**
- Too many features (high dimensionality)
- Visualizing data in 2D/3D
- Faster model training
- Removing correlated features

### Business Value

```
Before Segmentation:
├── One campaign for all 5,000 leads
├── 23% conversion rate
└── $13.8M revenue

After K-Means Segmentation:
├── 5 targeted campaigns
├── 133% revenue lift
└── $32.2M revenue

ROI: $18.4M additional revenue from ML clustering
```

## Production Checklist

- [x] Find optimal K using silhouette score
- [x] Run K-Means clustering
- [x] Analyze cluster characteristics
- [x] Create targeted campaigns per segment
- [x] Deploy production segmentation
- [x] Measure business impact
- [x] Use PCA for dimensionality reduction
- [x] Compare K-Means vs DBSCAN
- [x] Visualize clusters (2D/3D)
- [x] Auto-assign new leads to segments

## Next Steps

1. ✅ Complete unsupervised learning tutorial
2. ➡️ Advanced: Neural networks for complex patterns
3. ➡️ Experiment: Hierarchical clustering
4. ➡️ Production: Auto-retraining on new lead data

---

**© 2025 CircuitOS™ - ML Education Series**

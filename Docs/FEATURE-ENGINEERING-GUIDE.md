# Feature Engineering Guide for Circuit OS
**Turning Raw Data into ML Gold**

**From ML Algorithms Overview:**
> "SVM uses kernel trick for implicit feature engineering"
> "Neural networks automatically design complex features without human guidance"
> "PCA combines correlated features (height + length → shape)"

---

## 🎯 What is Feature Engineering?

**Feature Engineering** = Creating new features from raw data that help ML models make better predictions

**Example:**
```python
# Raw data (weak features)
raw_data = {
    "created_at": "2025-11-15 14:30:00",
    "email": "john@acme.com"
}

# Engineered features (powerful!)
engineered = {
    "days_since_signup": 3,
    "hour_of_day": 14,
    "is_business_hours": True,
    "is_business_email": True,  # .com vs .gmail
    "company_domain": "acme.com",
    "email_length": 14
}
```

**Impact:** Good features can improve model accuracy by 20-50%!

---

## 📊 Feature Engineering Techniques

### 1. Temporal Features (Time-Based)

**From Raw Timestamps:**
```python
from datetime import datetime

def engineer_time_features(timestamp):
    dt = datetime.fromisoformat(timestamp)

    return {
        "hour_of_day": dt.hour,  # 0-23
        "day_of_week": dt.weekday(),  # 0=Monday, 6=Sunday
        "is_business_hours": 9 <= dt.hour < 17,
        "is_weekend": dt.weekday() >= 5,
        "is_monday": dt.weekday() == 0,  # Monday = high email open rate
        "is_friday": dt.weekday() == 4,  # Friday = low engagement

        # Cyclical encoding (preserve circular nature of time)
        "hour_sin": np.sin(2 * np.pi * dt.hour / 24),
        "hour_cos": np.cos(2 * np.pi * dt.hour / 24),

        # Time since reference
        "days_since_signup": (datetime.now() - dt).days,
        "weeks_since_first_contact": (datetime.now() - dt).days // 7
    }
```

**Circuit OS Use Case:**
```python
# LPR scoring with time features
lead = {
    "contacted_at": "2025-11-15 10:30:00",
    "signed_up_at": "2025-11-12 14:00:00"
}

features = engineer_time_features(lead['contacted_at'])
features['days_since_signup'] = 3
features['response_speed'] = "fast" if features['days_since_signup'] < 7 else "slow"

# Insight: Leads contacted within 3 days have 2x conversion rate!
```

---

### 2. Interaction Features (Combining Features)

**Multiplication, Division, Ratios:**
```python
def engineer_interaction_features(lead):
    return {
        # Ratio features (often powerful!)
        "email_engagement_rate": lead['emails_opened'] / max(lead['emails_sent'], 1),
        "website_engagement_rate": lead['pages_viewed'] / max(lead['sessions'], 1),
        "pricing_interest_ratio": lead['pricing_page_visits'] / max(lead['total_visits'], 1),

        # Product features
        "engagement_x_company_size": lead['engagement_score'] * lead['company_size'],
        "traffic_per_employee": lead['website_traffic'] / max(lead['company_size'], 1),

        # Boolean interactions
        "high_engagement_and_big_company": (
            lead['engagement_score'] > 70 and lead['company_size'] > 100
        )
    }
```

**From ML Overview:**
> "Finding complex relationships between features is what ensemble methods and neural networks excel at"

---

### 3. Categorical Encoding

**One-Hot Encoding:**
```python
# Before: industry = "Technology"
# After: industry_Technology = 1, industry_Finance = 0, industry_Healthcare = 0

from sklearn.preprocessing import OneHotEncoder

industries = ["Technology", "Finance", "Healthcare", "Retail"]
encoder = OneHotEncoder(sparse=False)

encoded = encoder.fit_transform([[industry] for industry in industries])

"""
Output:
[[1, 0, 0, 0],  # Technology
 [0, 1, 0, 0],  # Finance
 [0, 0, 1, 0],  # Healthcare
 [0, 0, 0, 1]]  # Retail
"""
```

**Label Encoding (Ordinal):**
```python
# For ordered categories
priority_map = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "urgent": 3
}

lead['priority_encoded'] = priority_map[lead['priority']]
```

**Target Encoding (Advanced):**
```python
# Encode category by its average target value
def target_encode(df, category_col, target_col):
    """
    Example: Industry → avg conversion rate per industry
    """
    encoding = df.groupby(category_col)[target_col].mean().to_dict()

    return df[category_col].map(encoding)

# Technology: 0.45 avg conversion
# Finance: 0.38 avg conversion
# Healthcare: 0.52 avg conversion
```

---

### 4. Text Features

**From ML Overview:**
> "Naive Bayes counts word occurrences and multiplies probabilities. Good for text-based tasks."

**Basic Text Features:**
```python
def engineer_text_features(message):
    return {
        "word_count": len(message.split()),
        "char_count": len(message),
        "avg_word_length": len(message) / len(message.split()),

        # Punctuation
        "question_marks": message.count("?"),
        "exclamation_marks": message.count("!"),
        "has_question": "?" in message,

        # Keywords (pricing intent)
        "mentions_price": any(word in message.lower() for word in ["price", "cost", "rate", "$"]),
        "mentions_demo": "demo" in message.lower(),
        "mentions_trial": any(word in message.lower() for word in ["trial", "free", "test"]),

        # Sentiment (simple rule-based)
        "positive_words": sum(1 for word in ["great", "thanks", "excellent"] if word in message.lower()),
        "negative_words": sum(1 for word in ["issue", "problem", "complaint"] if word in message.lower()),

        # Advanced: TF-IDF (Circuit OS integration)
        # See sklearn.feature_extraction.text.TfidfVectorizer
    }
```

**Email Quality Features:**
```python
def engineer_email_quality_features(email):
    """For neural network email scoring"""
    return {
        "word_count": len(email.split()),
        "sentence_count": email.count(".") + email.count("!") + email.count("?"),
        "avg_sentence_length": len(email.split()) / max(email.count("."), 1),

        "has_personalization": "{{name}}" in email or "{{company}}" in email,
        "personalization_count": email.count("{{"),

        "has_hook": any(phrase in email[:100] for phrase in ["Quick question", "Noticed that", "Saw that"]),
        "has_cta": any(phrase in email for phrase in ["book a call", "schedule", "reply"]),

        "reading_level": calculate_flesch_score(email),  # 0-100 scale
        "sentiment_score": analyze_sentiment(email)  # -1 to 1
    }
```

---

### 5. Aggregation Features (Group Statistics)

**From Lead History:**
```python
def engineer_aggregation_features(lead_id, conversations):
    """Aggregate features from conversation history"""
    lead_convos = [c for c in conversations if c['lead_id'] == lead_id]

    return {
        # Count features
        "total_conversations": len(lead_convos),
        "total_messages": sum(len(c['messages']) for c in lead_convos),

        # Timing features
        "avg_response_time_minutes": np.mean([c['response_time'] for c in lead_convos]),
        "days_since_last_contact": (datetime.now() - lead_convos[-1]['timestamp']).days,

        # Engagement features
        "avg_sentiment": np.mean([c['sentiment'] for c in lead_convos]),
        "sentiment_trend": lead_convos[-1]['sentiment'] - lead_convos[0]['sentiment'],  # Improving?
        "lpr_score_trend": lead_convos[-1]['lpr_score'] - lead_convos[0]['lpr_score'],

        # Behavioral patterns
        "pricing_inquiries": sum(1 for c in lead_convos if c['intent'] == 'pricing'),
        "demo_requests": sum(1 for c in lead_convos if 'demo' in c['message'].lower()),
        "complaint_count": sum(1 for c in lead_convos if c['intent'] == 'complaint')
    }
```

**From ML-FEEDBACK-LOOP-SYSTEM.md:**
> "Conversation history generates ML training signals: successful paths, key phrases, sentiment progression"

---

### 6. Missing Data Handling

**Strategies:**
```python
def handle_missing_data(features):
    """
    Different strategies for different feature types
    """

    # Strategy 1: Fill with default
    features['company_size'] = features.get('company_size', 0)

    # Strategy 2: Fill with mean/median
    features['website_traffic'] = features.get(
        'website_traffic',
        50000  # median traffic
    )

    # Strategy 3: Create "missing" indicator
    features['has_company_size'] = 'company_size' in features
    features['has_traffic_data'] = 'website_traffic' in features

    # Strategy 4: Fill with category mode
    features['industry'] = features.get('industry', 'Technology')  # Most common

    return features
```

**Circuit OS Best Practice:**
```python
# Always create "has_X" indicators for important features
# Random Forest and XGBoost handle missing data well
# Linear Regression and Logistic Regression need imputation
```

---

### 7. Scaling and Normalization

**Why Scale?**
> Neural networks, SVM, and KNN are sensitive to feature scales
> Random Forest and XGBoost are NOT sensitive (tree-based)

**Standard Scaling (Z-score normalization):**
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# Before scaling
X = [[10000, 0.85, 150],  # [traffic, geo_fit, company_size]
     [500, 0.42, 20]]

# After scaling (mean=0, std=1)
X_scaled = scaler.fit_transform(X)
# [[ 1.0,  1.0,  1.0],
#  [-1.0, -1.0, -1.0]]
```

**Min-Max Scaling (0-1 range):**
```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)
# [[1.0, 1.0, 1.0],
#  [0.0, 0.0, 0.0]]
```

**When to Use:**
- ✅ **Standard Scaling:** Neural networks, SVM, Logistic Regression
- ✅ **Min-Max Scaling:** When you need features in [0,1] range
- ❌ **No Scaling:** Random Forest, XGBoost, Decision Trees

---

### 8. Polynomial Features

**Create Feature Interactions Automatically:**
```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)

# Original features: [engagement, company_size]
X = [[75, 150]]

# Polynomial features: [engagement, company_size, engagement^2, engagement*company_size, company_size^2]
X_poly = poly.fit_transform(X)
# [[75, 150, 5625, 11250, 22500]]
```

**Use Case:**
```python
# Capture non-linear relationships
# engagement^2 might be important: very high engagement (90+) converts 3x better
# engagement * company_size: big companies with high engagement are gold
```

**Warning:** Creates many features, can lead to overfitting on small datasets

---

### 9. SVM Kernel Trick (Implicit Feature Engineering)

**From ML Overview:**
> "SVM kernel functions use the kernel trick to implicitly turn original features into new, more complex features (implicit feature engineering)"

**Explicit vs Implicit:**
```python
# Explicit: You manually create features
features = {
    "engagement": 75,
    "company_size": 150,
    "engagement_squared": 75^2,  # Manual
    "engagement_x_size": 75 * 150  # Manual
}

# Implicit: SVM RBF kernel does it automatically
from sklearn.svm import SVC

svm = SVC(kernel='rbf')  # Implicitly creates infinite-dimensional features!
svm.fit(X, y)

# RBF kernel automatically finds complex patterns without you engineering features
```

**When to Use SVM Kernel:**
- ✅ Complex non-linear patterns
- ✅ Don't know which feature interactions matter
- ✅ Medium datasets (1,000-10,000)

---

### 10. Neural Network Feature Learning

**From ML Overview:**
> "Neural networks automatically design complex features without human guidance. Hidden layers learn to represent complex information."

**Circuit OS Example:**
```python
# You provide simple features:
simple_features = [
    "word_count", "sentiment", "question_marks",
    "personalization_tokens", "reading_level"
]

# Neural network hidden layers learn:
# Layer 1 (100 neurons): Tone patterns, engagement indicators
# Layer 2 (50 neurons): Hook-Story-Offer structure, CTA strength
# Layer 3 (25 neurons): Overall persuasiveness, conversion probability

# No manual feature engineering needed for these complex patterns!
```

**Trade-off:**
- ✅ Automatic complex feature learning
- ✅ No domain expertise needed
- ❌ Requires large datasets (10,000+)
- ❌ Black box (hard to interpret)

---

## 🎯 CIRCUIT OS FEATURE ENGINEERING PATTERNS

### LPR Score Features

```python
def engineer_lpr_features(lead):
    """
    Complete feature set for LPR scoring
    47 features total
    """
    return {
        # Core features (10)
        "engagement_score": lead['engagement_score'],
        "company_size": lead.get('company_size', 0),
        "geographic_fit": lead.get('geographic_fit', 0),
        "website_traffic": lead.get('website_traffic', 0),
        "email_open_rate": lead.get('email_open_rate', 0),
        "email_click_rate": lead.get('email_click_rate', 0),
        "linkedin_connections": lead.get('linkedin_connections', 0),
        "pricing_page_visits": lead.get('pricing_page_visits', 0),
        "time_on_site": lead.get('time_on_site', 0),
        "pages_viewed": lead.get('pages_viewed', 0),

        # Ratio features (5)
        "click_to_open_ratio": lead.get('email_click_rate', 0) / max(lead.get('email_open_rate', 1), 0.01),
        "pricing_interest_ratio": lead.get('pricing_page_visits', 0) / max(lead.get('total_visits', 1), 1),
        "engagement_per_employee": lead.get('engagement_score', 0) / max(lead.get('company_size', 1), 1),
        "traffic_per_employee": lead.get('website_traffic', 0) / max(lead.get('company_size', 1), 1),
        "pages_per_session": lead.get('pages_viewed', 0) / max(lead.get('sessions', 1), 1),

        # Time features (7)
        "days_since_signup": (datetime.now() - lead['created_at']).days,
        "days_since_last_contact": (datetime.now() - lead.get('last_contacted', datetime.now())).days,
        "is_business_hours": 9 <= datetime.now().hour < 17,
        "is_weekend": datetime.now().weekday() >= 5,
        "response_speed_score": calculate_response_speed(lead),
        "recency_score": 100 - min((datetime.now() - lead.get('last_contacted', datetime.now())).days, 100),
        "frequency_score": min(lead.get('total_interactions', 0) * 10, 100),

        # Categorical (encoded) (10)
        "industry_Technology": lead.get('industry') == 'Technology',
        "industry_Finance": lead.get('industry') == 'Finance',
        "industry_Healthcare": lead.get('industry') == 'Healthcare',
        "company_size_segment": categorize_company_size(lead.get('company_size', 0)),
        "location_tier": categorize_location(lead.get('location')),
        "source_organic": lead.get('source') == 'organic',
        "source_paid": lead.get('source') == 'paid',
        "source_referral": lead.get('source') == 'referral',
        "has_demo_requested": lead.get('demo_requested', False),
        "has_pricing_inquiry": lead.get('pricing_inquiry_count', 0) > 0,

        # Aggregated conversation features (10)
        "total_conversations": lead.get('conversation_count', 0),
        "avg_sentiment": lead.get('avg_sentiment', 0),
        "sentiment_trend": lead.get('sentiment_trend', 0),
        "lpr_progression": lead.get('current_lpr', 50) - lead.get('initial_lpr', 50),
        "pricing_inquiry_count": lead.get('pricing_inquiry_count', 0),
        "demo_request_count": lead.get('demo_request_count', 0),
        "complaint_count": lead.get('complaint_count', 0),
        "positive_response_rate": lead.get('positive_responses', 0) / max(lead.get('total_responses', 1), 1),
        "avg_response_time_hours": lead.get('avg_response_time', 0) / 3600,
        "engagement_consistency": calculate_engagement_consistency(lead),

        # Missing data indicators (5)
        "has_company_size": 'company_size' in lead,
        "has_traffic_data": 'website_traffic' in lead,
        "has_linkedin_data": 'linkedin_connections' in lead,
        "has_pricing_data": 'pricing_page_visits' in lead,
        "has_conversation_history": lead.get('conversation_count', 0) > 0
    }
```

### Email Intent Classification Features

```python
def engineer_intent_features(message):
    """
    Text features for Naive Bayes / Random Forest intent classification
    """
    message_lower = message.lower()

    return {
        # Basic text features
        "word_count": len(message.split()),
        "char_count": len(message),
        "sentence_count": message.count(".") + message.count("!") + message.count("?"),

        # Keyword features (pricing intent)
        "mentions_pricing": any(word in message_lower for word in ["price", "cost", "rate", "pricing", "$", "quote"]),
        "mentions_demo": any(word in message_lower for word in ["demo", "demonstration", "show me"]),
        "mentions_trial": any(word in message_lower for word in ["trial", "free", "test", "try"]),
        "mentions_complaint": any(word in message_lower for word in ["issue", "problem", "not working", "broken"]),
        "mentions_cancel": any(word in message_lower for word in ["cancel", "unsubscribe", "stop", "remove"]),

        # Question indicators
        "has_question": "?" in message,
        "question_count": message.count("?"),
        "starts_with_question": message.strip().startswith(("what", "how", "why", "when", "where", "can", "do")),

        # Sentiment indicators
        "has_thanks": any(word in message_lower for word in ["thanks", "thank you", "appreciate"]),
        "has_positive": any(word in message_lower for word in ["great", "excellent", "perfect", "love"]),
        "has_negative": any(word in message_lower for word in ["bad", "terrible", "worst", "hate"]),

        # Urgency indicators
        "has_urgency": any(word in message_lower for word in ["asap", "urgent", "immediately", "quickly", "soon"]),
        "has_time_reference": any(word in message_lower for word in ["today", "tomorrow", "this week", "monday"]),

        # Advanced: TF-IDF vector (for production)
        # Use sklearn.feature_extraction.text.TfidfVectorizer
    }
```

---

## 🚀 PRODUCTION FEATURE ENGINEERING PIPELINE

### Complete Example

```python
class FeatureEngineer:
    """Production feature engineering pipeline for Circuit OS"""

    def __init__(self):
        self.scaler = StandardScaler()
        self.poly = PolynomialFeatures(degree=2, include_bias=False)

    def transform(self, lead):
        """Transform raw lead data into ML-ready features"""

        # Step 1: Engineer all features
        features = {}

        features.update(engineer_lpr_features(lead))
        features.update(engineer_time_features(lead.get('created_at')))
        features.update(engineer_interaction_features(lead))
        features.update(engineer_aggregation_features(lead['id'], get_conversations(lead['id'])))

        # Step 2: Handle missing data
        features = handle_missing_data(features)

        # Step 3: Create feature vector
        X = np.array([[features[key] for key in sorted(features.keys())]])

        # Step 4: Scale (for neural networks, SVM)
        # Skip for Random Forest, XGBoost
        X_scaled = self.scaler.fit_transform(X)

        # Step 5: Optional - Add polynomial features
        # X_poly = self.poly.fit_transform(X_scaled)

        return X_scaled, features

# Usage
engineer = FeatureEngineer()
X, features = engineer.transform(new_lead)

# Predict
lpr_score = xgboost_model.predict(X)[0]
```

---

## ✅ FEATURE ENGINEERING CHECKLIST

**Before Training:**
- [ ] Handle missing data (impute or create indicators)
- [ ] Encode categorical variables (one-hot or target encoding)
- [ ] Scale numerical features (for neural networks, SVM)
- [ ] Create time-based features (hour, day, days_since)
- [ ] Create ratio features (engagement_rate, click_to_open)
- [ ] Create aggregation features (avg, sum, count from history)
- [ ] Create interaction features (feature_A * feature_B)
- [ ] Create missing data indicators (has_company_size)
- [ ] Remove highly correlated features (use PCA or manual selection)
- [ ] Check for data leakage (no future data in features!)

**After Initial Training:**
- [ ] Analyze feature importance (Random Forest, XGBoost)
- [ ] Remove low-importance features
- [ ] Create new features based on domain insights
- [ ] Test polynomial features (degree=2)
- [ ] Try PCA for dimensionality reduction

**Production:**
- [ ] Save feature transformer (scaler, encoder)
- [ ] Document all feature transformations
- [ ] Monitor feature distributions for drift
- [ ] Version control feature engineering code

---

**Status:** ✅ Complete Feature Engineering Guide
**Integration:** Circuit OS production patterns
**Next:** Apply features to `ml_service.py` for improved predictions

---

**© 2025 CircuitOS™ - Feature Engineering Documentation**

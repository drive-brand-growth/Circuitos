# Google SGE / AI Overviews Optimization Plan
## Critical Gap #7 - Build World-Class SEO for 2025

**Gap Addressed:** Google Search Generative Experience (SGE) / AI Overviews optimization
**Impact:** 61% of mobile searches now show AI summaries (2025 data)
**Build Time:** 2-3 weeks (40 hours)
**Cost:** $0 (code only, no API costs)

---

## The Problem: You're Optimizing for 2018 Google

### Current SEO Agents ⚠️
**What you have:**
- ✅ Local SEO Content Engine (958 lines)
- ✅ AI Search Optimizer (834 lines)
- ✅ Schema markup (FAQ, How-To, Article)
- ✅ Keyword research
- ✅ Local listings management

**What's missing:**
- ❌ E-E-A-T optimization (Experience, Expertise, Authoritativeness, Trust)
- ❌ AEO format (Answer Engine Optimization)
- ❌ Citation optimization (getting cited in AI summaries)
- ❌ Content freshness automation
- ❌ AI snippet targeting
- ❌ Voice search optimization
- ❌ Entity-based SEO
- ❌ Semantic search optimization

**The gap:**
Your SEO agents optimize for **traditional Google search** (2018-2020).

In 2025, **61% of mobile searches** show **AI Overviews** (Google's AI-generated summaries) ABOVE traditional results.

**If you're not optimized for SGE, you're invisible to 61% of searches.**

---

## What is Google SGE / AI Overviews?

### Before (Traditional Search):
```
Google Search: "best gym near me"

Results:
1. [Ad] Planet Fitness
2. [Map Pack] Local gyms
3. [Organic] Top 10 gym websites
4. [People Also Ask] Questions
```

### After (AI Overviews, 2025):
```
Google Search: "best gym near me"

[AI Overview - 200 words]
✨ Based on 47 sources, the best gyms near you are:

1. MetroFlex Gym (4.9 stars, 230 reviews)
   - Specializes in powerlifting and functional fitness
   - Known for experienced trainers and community atmosphere
   - Pricing: $89/month (mid-range)

2. Equinox Manhattan (4.7 stars, 180 reviews)
   - Premium facility with spa amenities
   - Best for: Luxury fitness experience
   - Pricing: $250/month (premium)

Key factors to consider:
- Proximity to your location (within 2 miles recommended)
- Training style match (CrossFit vs traditional)
- Budget (ranges $30-250/month)

[Sources cited: 47 websites, including MetroFlex Gym website, Yelp, Google reviews]

---

[Traditional results below - BELOW THE FOLD, 61% of users never scroll here]
```

**The shift:**
- Traditional SEO = rank in top 10 organic results
- SGE optimization = **get cited in the AI Overview**

**If you're cited:**
- ✅ Appear at top of page (highest attention zone)
- ✅ Clickable reference with your brand name
- ✅ Instant credibility (Google AI trusts your content)

**If you're NOT cited:**
- ❌ Below the fold (61% of users never see you)
- ❌ Traffic drops 40-60% (industry data)
- ❌ Competitors dominate AI Overview

---

## World-Class Benchmark: Semrush/Ahrefs SGE Optimization (2025)

### What Industry Leaders Are Doing

**E-E-A-T Optimization:**
- Experience: Author bios with credentials
- Expertise: Cite research, data, expert quotes
- Authoritativeness: Backlinks from .edu/.gov
- Trustworthiness: HTTPS, privacy policy, contact info

**AEO Format (Answer Engine Optimization):**
- Content structured as Q&A
- Clear, concise answers in first 100 words
- H2 headers as questions
- Bullet points for scannability

**Citation Optimization:**
- Primary sources cited (not just Wikipedia)
- Data tables with footnotes
- Clear attribution for stats
- Schema markup for citations

**Content Freshness:**
- Updated within last 3 months
- "Last updated: [date]" timestamp
- Current year in content (2025, not 2023)
- Fresh stats (2024-2025 data)

**Featured Snippet Targeting:**
- Answer in first paragraph
- 40-60 words (optimal length)
- Definition format or list format
- Schema markup (FAQ/How-To)

---

## Implementation: SGE Optimization Agent

### New Agent: `sge-optimization-agent` (800-1,000 lines)

**Location:** `/circuit_script/agents/SGEOptimizationAgent.py`

**Capabilities:**
1. E-E-A-T Scoring (0-100)
2. AEO Format Conversion (traditional → question/answer)
3. Citation Tracking (which sources get cited)
4. Content Freshness Automation (auto-update dates/stats)
5. Featured Snippet Optimization
6. Voice Search Optimization
7. Entity-based SEO
8. Semantic Search Optimization

---

### Module 1: E-E-A-T Scorer (200 lines)

**Purpose:** Score content on Google's E-E-A-T framework (0-100)

**Algorithm:**
```python
def score_eeat(content: str, metadata: Dict) -> Dict:
    """Score content on E-E-A-T framework"""
    score = 0
    max_score = 100

    # EXPERIENCE (25 points)
    experience_score = 0

    # Author has credentials? +10
    if has_author_bio_with_credentials(content):
        experience_score += 10

    # First-hand experience demonstrated? +10
    if has_first_hand_anecdotes(content):
        experience_score += 10

    # Author photo + social proof? +5
    if has_author_photo_and_social_links(metadata):
        experience_score += 5

    # EXPERTISE (25 points)
    expertise_score = 0

    # Cites research/data? +10
    citations = extract_citations(content)
    if len(citations) >= 3:
        expertise_score += 10

    # Expert quotes? +8
    expert_quotes = extract_expert_quotes(content)
    if len(expert_quotes) >= 2:
        expertise_score += 8

    # Technical depth? +7
    if has_technical_depth(content):
        expertise_score += 7

    # AUTHORITATIVENESS (25 points)
    auth_score = 0

    # Backlinks from .edu/.gov? +10
    authoritative_backlinks = count_authoritative_backlinks(metadata['url'])
    if authoritative_backlinks >= 5:
        auth_score += 10
    elif authoritative_backlinks >= 1:
        auth_score += 5

    # Domain authority >40? +8
    if metadata.get('domain_authority', 0) > 40:
        auth_score += 8

    # Published on authoritative site? +7
    if is_authoritative_domain(metadata['domain']):
        auth_score += 7

    # TRUSTWORTHINESS (25 points)
    trust_score = 0

    # HTTPS? +5
    if metadata['url'].startswith('https://'):
        trust_score += 5

    # Privacy policy? +5
    if has_privacy_policy(metadata['domain']):
        trust_score += 5

    # Contact info visible? +5
    if has_contact_info(content):
        trust_score += 5

    # No spammy ads? +5
    if not has_excessive_ads(metadata['url']):
        trust_score += 5

    # Last updated recently? +5
    if was_updated_within_months(content, 3):
        trust_score += 5

    total_score = experience_score + expertise_score + auth_score + trust_score

    return {
        'total': total_score,
        'max': max_score,
        'percentage': (total_score / max_score) * 100,
        'breakdown': {
            'experience': experience_score,
            'expertise': expertise_score,
            'authoritativeness': auth_score,
            'trustworthiness': trust_score
        },
        'recommendations': generate_eeat_recommendations(
            experience_score, expertise_score, auth_score, trust_score
        )
    }
```

---

### Module 2: AEO Format Converter (200 lines)

**Purpose:** Convert traditional content to Answer Engine Optimization format

**Before (Traditional):**
```markdown
# Best Gyms in Dallas

Dallas has many great gyms. MetroFlex Gym is a popular choice for
powerlifters and CrossFit enthusiasts. The facility offers state-of-the-art
equipment and experienced trainers.

Founded in 2015, MetroFlex has grown to serve over 1,200 members...
```

**After (AEO Format):**
```markdown
# What are the best gyms in Dallas for powerlifting?

**Quick Answer:** MetroFlex Gym (4.9 stars, 230 reviews) is the top-rated
powerlifting gym in Dallas, known for competition-grade equipment, experienced
coaches, and a strong community atmosphere. Pricing starts at $89/month.

## Why MetroFlex Gym ranks #1 for Dallas powerlifters:

1. **Equipment:** Competition-grade powerlifting platforms, calibrated plates,
   specialty bars (Source: MetroFlex equipment inventory, updated 2025)

2. **Coaching:** USAPL-certified coaches with 10+ years experience
   (Source: Coach certification records)

3. **Community:** 230+ five-star reviews highlighting supportive culture
   (Source: Google Reviews, 2024-2025)

4. **Results:** Members have won 15+ state championships since 2020
   (Source: MetroFlex competition results)

## How much does MetroFlex Gym cost?

- Monthly: $89/month (mid-range vs Dallas average $75)
- Annual: $950/year (saves $118 vs monthly)
- Drop-in: $25/day

(Source: MetroFlex pricing page, last updated Jan 2025)

## Who should choose MetroFlex Gym?

✅ Best for:
- Competitive powerlifters (beginner to elite)
- CrossFit athletes wanting powerlifting coaching
- Strength training enthusiasts (3-5 days/week)

❌ Not ideal for:
- Cardio-focused workouts (limited machines)
- Budget seekers (basic gyms start at $10/month)
- Luxury amenities (no spa, pool, or sauna)

---

**Author:** John Smith, CSCS, USAPL Coach (15 years powerlifting experience)
**Last Updated:** January 15, 2025
**Sources:** 12 citations (MetroFlex Gym, USAPL, Google Reviews, Census Bureau)
```

**Algorithm:**
```python
def convert_to_aeo(content: str) -> str:
    """Convert traditional content to AEO format"""

    # 1. Extract main topic
    topic = extract_main_topic(content)

    # 2. Identify questions being answered
    questions = identify_implied_questions(content)

    # 3. Restructure as Q&A
    aeo_sections = []

    for question in questions:
        answer = extract_answer_for_question(content, question)

        aeo_sections.append({
            'question': question,
            'quick_answer': summarize_answer(answer, max_words=60),
            'detailed_answer': format_with_bullets(answer),
            'sources': extract_sources_for_answer(answer)
        })

    # 4. Add E-E-A-T elements
    author_bio = generate_author_bio_from_metadata()
    last_updated = datetime.now().strftime('%B %d, %Y')
    source_citations = compile_all_sources(aeo_sections)

    # 5. Format for SGE
    aeo_content = format_aeo_template(
        topic=topic,
        sections=aeo_sections,
        author=author_bio,
        updated=last_updated,
        citations=source_citations
    )

    return aeo_content
```

---

### Module 3: Citation Tracker (150 lines)

**Purpose:** Track which content gets cited in AI Overviews

**How it works:**
1. Search Google for target keywords
2. Extract AI Overview citations
3. Analyze what content Google cites
4. Recommend improvements

**Algorithm:**
```python
def track_sge_citations(keyword: str, our_domain: str) -> Dict:
    """Track SGE citations for a keyword"""

    # 1. Perform Google search
    search_result = google_search(keyword, include_ai_overview=True)

    # 2. Extract AI Overview
    ai_overview = search_result.get('ai_overview')

    if not ai_overview:
        return {'cited': False, 'reason': 'No AI Overview shown for this keyword'}

    # 3. Extract cited sources
    cited_sources = ai_overview['sources']

    # 4. Check if our domain is cited
    our_citations = [s for s in cited_sources if our_domain in s['url']]

    # 5. Analyze competitors
    competitor_citations = [s for s in cited_sources if our_domain not in s['url']]

    # 6. Extract what makes cited content special
    citation_patterns = analyze_citation_patterns(cited_sources)

    return {
        'keyword': keyword,
        'cited': len(our_citations) > 0,
        'our_citations': our_citations,
        'competitor_citations': competitor_citations,
        'total_sources': len(cited_sources),
        'ai_overview_text': ai_overview['text'],
        'patterns': citation_patterns,
        'recommendations': generate_citation_recommendations(
            our_citations, competitor_citations, citation_patterns
        )
    }

def analyze_citation_patterns(sources: List[Dict]) -> Dict:
    """Analyze what makes content get cited"""

    patterns = {
        'avg_word_count': [],
        'has_data_tables': 0,
        'has_expert_quotes': 0,
        'content_freshness_months': [],
        'uses_schema_markup': 0,
        'avg_eeat_score': []
    }

    for source in sources:
        content = fetch_url(source['url'])

        patterns['avg_word_count'].append(count_words(content))
        patterns['has_data_tables'] += 1 if has_tables(content) else 0
        patterns['has_expert_quotes'] += 1 if has_quotes(content) else 0
        patterns['content_freshness_months'].append(get_content_age_months(content))
        patterns['uses_schema_markup'] += 1 if has_schema(content) else 0
        patterns['avg_eeat_score'].append(score_eeat(content)['total'])

    return {
        'avg_word_count': mean(patterns['avg_word_count']),
        'data_tables_percentage': patterns['has_data_tables'] / len(sources),
        'expert_quotes_percentage': patterns['has_expert_quotes'] / len(sources),
        'avg_content_age_months': mean(patterns['content_freshness_months']),
        'schema_markup_percentage': patterns['uses_schema_markup'] / len(sources),
        'avg_eeat_score': mean(patterns['avg_eeat_score'])
    }
```

---

### Module 4: Content Freshness Automation (150 lines)

**Purpose:** Auto-update dates, stats, and time-sensitive content

**How it works:**
1. Scan content for outdated elements
2. Fetch fresh data from APIs
3. Update content automatically
4. Trigger republish

**Algorithm:**
```python
def auto_refresh_content(article_id: str) -> Dict:
    """Automatically refresh outdated content"""

    article = load_article(article_id)

    updates_made = []

    # 1. Update "last updated" date
    if not has_recent_update_date(article):
        article['content'] = update_timestamp(article['content'])
        updates_made.append('Updated timestamp to current date')

    # 2. Refresh statistics
    stats_to_update = extract_statistics(article['content'])

    for stat in stats_to_update:
        # Example: "61% of mobile searches show AI Overviews (2024 data)"
        # → "64% of mobile searches show AI Overviews (2025 data)"

        fresh_stat = fetch_fresh_statistic(stat['metric'], stat['source'])

        if fresh_stat != stat['value']:
            article['content'] = replace_statistic(
                article['content'],
                old_value=stat['value'],
                new_value=fresh_stat,
                source=stat['source']
            )
            updates_made.append(f"Updated {stat['metric']}: {stat['value']} → {fresh_stat}")

    # 3. Update year references
    current_year = datetime.now().year
    article['content'] = replace_year_references(article['content'], current_year)
    updates_made.append(f'Updated year references to {current_year}')

    # 4. Refresh external links
    broken_links = check_links(article['content'])
    for link in broken_links:
        replacement = find_replacement_link(link)
        if replacement:
            article['content'] = replace_link(article['content'], link, replacement)
            updates_made.append(f'Replaced broken link: {link} → {replacement}')

    # 5. Update schema markup
    article['schema'] = generate_updated_schema(article)
    updates_made.append('Regenerated schema markup with current data')

    # 6. Save and republish
    save_article(article)
    trigger_republish(article_id)

    return {
        'article_id': article_id,
        'updates_made': updates_made,
        'freshness_score_before': calculate_freshness_score(article['original_content']),
        'freshness_score_after': calculate_freshness_score(article['content']),
        'republished_at': datetime.now().isoformat()
    }
```

---

### Module 5: Featured Snippet Optimizer (100 lines)

**Purpose:** Optimize first paragraph for featured snippet capture

**Target:** 40-60 words, definition or list format

**Algorithm:**
```python
def optimize_for_featured_snippet(content: str, keyword: str) -> str:
    """Optimize content for featured snippet"""

    # 1. Extract or generate definition
    definition = extract_definition(content, keyword)

    if not definition:
        definition = generate_definition_from_content(content, keyword)

    # 2. Ensure optimal length (40-60 words)
    if count_words(definition) > 60:
        definition = summarize_to_length(definition, target_words=50)
    elif count_words(definition) < 40:
        definition = expand_with_context(definition, content, target_words=50)

    # 3. Add to first paragraph
    optimized_content = insert_featured_snippet(content, definition, position='first_paragraph')

    # 4. Add schema markup
    optimized_content = add_faq_schema(optimized_content, keyword, definition)

    return optimized_content
```

---

## Integration with Existing Agents

### Update Local SEO Content Engine

**Before:**
```python
def generate_content(topic: str, location: str) -> str:
    # Traditional SEO content
    keyword_research = research_keywords(topic, location)
    content = generate_blog_post(keyword_research)
    return content
```

**After (with SGE Optimization):**
```python
from circuit_script.agents.SGEOptimizationAgent import SGEOptimizationAgent

def generate_content(topic: str, location: str) -> str:
    # 1. Traditional keyword research
    keyword_research = research_keywords(topic, location)

    # 2. Generate traditional content
    content = generate_blog_post(keyword_research)

    # 3. SGE optimization
    sge_agent = SGEOptimizationAgent()

    # Convert to AEO format
    aeo_content = sge_agent.convert_to_aeo(content)

    # Optimize for featured snippet
    snippet_optimized = sge_agent.optimize_for_featured_snippet(
        aeo_content,
        keyword=keyword_research['primary_keyword']
    )

    # Score E-E-A-T
    eeat_score = sge_agent.score_eeat(snippet_optimized, metadata={
        'url': f"https://metroflexgym.com/blog/{topic}",
        'domain': 'metroflexgym.com',
        'domain_authority': 35
    })

    # If E-E-A-T score < 70, enhance
    if eeat_score['percentage'] < 70:
        snippet_optimized = sge_agent.enhance_eeat(
            snippet_optimized,
            eeat_score['recommendations']
        )

    # Add schema markup
    final_content = sge_agent.add_advanced_schema(snippet_optimized)

    return final_content
```

---

## Deployment Roadmap

### Week 1: Build Core Modules (20 hours)

**Day 1-2:** E-E-A-T Scorer (8 hours)
- Build scoring algorithm
- Test on 10 sample articles
- Validate against manual E-E-A-T audit

**Day 3-4:** AEO Format Converter (8 hours)
- Build Q&A restructuring
- Test on 5 traditional blog posts
- Validate readability + SEO impact

**Day 5:** Featured Snippet Optimizer (4 hours)
- Build 40-60 word summarization
- Test on target keywords
- Measure featured snippet capture rate

---

### Week 2: Advanced Features (20 hours)

**Day 6-7:** Citation Tracker (10 hours)
- Build Google search scraper
- Extract AI Overview citations
- Analyze citation patterns
- Test on 20 target keywords

**Day 8-9:** Content Freshness Automation (8 hours)
- Build auto-update system
- Test on 10 outdated articles
- Measure freshness score improvement

**Day 10:** Integration + Testing (2 hours)
- Integrate with Local SEO Content Engine
- Test end-to-end workflow
- Deploy to production

---

## Success Metrics

### Week 1:
- ✅ E-E-A-T scorer built (accuracy >85% vs manual audit)
- ✅ AEO converter built (improves readability by 40%)
- ✅ Featured snippet optimizer built (captures snippets for 30% of keywords)

### Week 2:
- ✅ Citation tracker working (identifies citation gaps)
- ✅ Content freshness automation working (auto-updates 100% of content)
- ✅ Integrated with Local SEO Content Engine

### Month 1 Post-Launch:
- ✅ 20+ articles optimized for SGE
- ✅ E-E-A-T scores improved from avg 45 → 75
- ✅ Featured snippet capture rate: 30% → 50%

### Month 3 Post-Launch:
- ✅ Organic traffic increase: +25-40% (industry benchmark)
- ✅ AI Overview citations: 5+ keywords
- ✅ Voice search visibility: +50%

---

## Cost Analysis

### Traditional SEO (2018-2020):
- **Tools:** Ahrefs ($99/month) + Semrush ($119/month) = $218/month
- **Content creation:** 10 articles/month @ 4 hours each = 40 hours
- **Optimization:** Manual E-E-A-T audit = 2 hours/article = 20 hours
- **Total time:** 60 hours/month

### SGE Optimization (2025):
- **Tools:** $0 (built into Circuit Script)
- **Content creation:** 10 articles/month @ 2 hours each = 20 hours (50% faster with AEO templates)
- **Optimization:** Automated E-E-A-T + AEO conversion = 0 hours
- **Total time:** 20 hours/month

**Savings:** 40 hours/month @ $100/hr = **$4,000/month**
**ROI:** Infinite (saves $4K/month, costs $0 to run)

---

## Steve Jobs Protocol Verification

### Question 1: Does it make revenue faster?
✅ **YES**
- More organic traffic = more leads = more revenue
- 61% of searches show AI Overviews; if you're not optimized, you're invisible
- +25-40% organic traffic in 90 days (industry benchmark)

### Question 2: Can you explain it in <2 minutes?
✅ **YES**
"Google's new AI search shows AI-generated summaries ABOVE traditional results. 61% of people never scroll past this. If you're not cited in the AI summary, you're invisible. This agent optimizes your content to get cited."

### Question 3: Can you deploy in <5 minutes?
⚠️ **NO** (but worth the 2-3 week build)
- Build time: 40 hours (2-3 weeks)
- Deployment: 5 minutes (after built)
- Long-term: Saves 40 hours/month forever

### Question 4: No bullshit - is this critical?
✅ **YES - CRITICAL**
- 61% of mobile searches show AI Overviews
- If you're not optimized, traffic drops 40-60%
- Competitors optimizing for SGE will dominate your keywords

**Verdict:** Critical Gap #7 - Build immediately

---

**© 2025 CircuitOS™ - SGE/AI Overviews Optimization Plan**
**Status:** Critical Gap #7 - Weeks 3-4 of Build Roadmap
**Build Time:** 40 hours (2-3 weeks)
**Cost:** $0 (code only)
**Impact:** +25-40% organic traffic, 61% of searches visible
**Priority:** 🔴 CRITICAL (build immediately after Google AI Maps)

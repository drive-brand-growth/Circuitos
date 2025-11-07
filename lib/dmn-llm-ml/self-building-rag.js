/**
 * Self-Building RAG System
 * Automatically constructs and optimizes its own retrieval system
 *
 * @module self-building-rag
 * @copyright 2025 CircuitOS™ - HIGHLY CONFIDENTIAL
 */

const Anthropic = require('@anthropic-ai/sdk');

class SelfBuildingRAG {
  constructor(config = {}) {
    this.config = {
      anthropicApiKey: config.anthropicApiKey || process.env.ANTHROPIC_API_KEY,
      model: config.model || 'claude-sonnet-4-5-20250929',
      vectorDbPath: config.vectorDbPath || './data/vector-db',
      ...config
    };

    this.anthropic = new Anthropic({
      apiKey: this.config.anthropicApiKey
    });

    this.vectorDB = new InMemoryVectorDB();
    this.embeddingEngine = new AdaptiveEmbeddings(this.anthropic, this.config);
    this.chunkOptimizer = new ChunkOptimizer();
    this.retrievalLearner = new RetrievalLearner();
  }

  /**
   * Automatically index an interaction
   */
  async autoIndexInteraction(interaction) {
    console.log('📚 Auto-indexing interaction...');

    // 1. Extract indexable knowledge
    const knowledge = await this.extractIndexableKnowledge(interaction);

    // 2. Optimize chunking strategy
    const chunks = await this.chunkOptimizer.optimalChunk(knowledge);

    // 3. Generate embeddings
    const embeddings = await this.embeddingEngine.embedBatch(chunks);

    // 4. Store in vector database
    const ids = [];
    for (let i = 0; i < chunks.length; i++) {
      const id = await this.vectorDB.upsert({
        id: `${interaction.id || Date.now()}-chunk-${i}`,
        vector: embeddings[i].vector,
        text: chunks[i],
        metadata: {
          source: 'interaction',
          timestamp: Date.now(),
          outcome: interaction.outcome,
          confidence: this.calculateRelevance(interaction),
          accessCount: 0,
          successRate: null
        }
      });
      ids.push(id);
    }

    console.log(`✅ Indexed ${chunks.length} chunks`);

    return {
      chunksIndexed: chunks.length,
      ids
    };
  }

  /**
   * Extract knowledge suitable for indexing
   * @private
   */
  async extractIndexableKnowledge(interaction) {
    const parts = [];

    // Add conversation
    if (interaction.input && interaction.output) {
      parts.push(`Q: ${interaction.input}\nA: ${interaction.output}`);
    }

    // Add outcome context
    if (interaction.outcome) {
      parts.push(`Outcome: ${interaction.outcome.converted ? 'Converted' : 'Not converted'}`);

      if (interaction.outcome.revenue) {
        parts.push(`Revenue: $${interaction.outcome.revenue}`);
      }
    }

    // Add context
    if (interaction.context) {
      parts.push(`Context: ${JSON.stringify(interaction.context)}`);
    }

    return parts.join('\n\n');
  }

  /**
   * Intelligent retrieval with learning
   */
  async intelligentRetrieve(query, context = {}) {
    console.log('🔍 Retrieving relevant knowledge...');

    // 1. Generate query embedding
    const queryEmbedding = await this.embeddingEngine.embed(query, context);

    // 2. Use learned retrieval strategy
    const strategy = await this.retrievalLearner.getBestStrategy(context);

    // 3. Retrieve with hybrid approach
    const results = await this.vectorDB.query({
      vector: queryEmbedding.vector,
      topK: strategy.topK,
      filters: strategy.filters
    });

    // 4. Log retrieval for learning
    const retrievalId = await this.logRetrieval({
      query,
      results,
      strategy,
      timestamp: Date.now()
    });

    console.log(`✅ Retrieved ${results.length} relevant documents`);

    return {
      results,
      retrievalId,
      strategy
    };
  }

  /**
   * Update retrieval success based on outcome
   */
  async updateRetrievalSuccess(retrievalId, outcome) {
    const retrieval = this.retrievalLearner.getRetrieval(retrievalId);
    if (!retrieval) return;

    // Update success metrics for retrieved documents
    for (const result of retrieval.results) {
      await this.vectorDB.updateMetadata(result.id, {
        accessCount: (result.metadata.accessCount || 0) + 1,
        successRate: outcome.converted ? 1 : 0
      });
    }

    // Update strategy preferences
    await this.retrievalLearner.learn({
      strategy: retrieval.strategy,
      outcome: outcome.converted,
      context: retrieval.context
    });

    console.log(`✅ Updated retrieval success metrics`);
  }

  /**
   * Calculate relevance score
   * @private
   */
  calculateRelevance(interaction) {
    let relevance = 0.5;

    if (interaction.outcome?.converted) relevance += 0.3;
    if (interaction.outcome?.revenue > 100) relevance += 0.2;

    return Math.min(relevance, 1.0);
  }

  /**
   * Log retrieval for learning
   * @private
   */
  async logRetrieval(data) {
    return this.retrievalLearner.logRetrieval(data);
  }

  /**
   * Get RAG statistics
   */
  getStats() {
    return {
      totalDocuments: this.vectorDB.size(),
      totalRetrievals: this.retrievalLearner.totalRetrievals,
      avgRetrievalTime: this.retrievalLearner.avgRetrievalTime,
      strategies: this.retrievalLearner.getStrategyPerformance()
    };
  }
}

/**
 * In-Memory Vector Database (for MVP, replace with Pinecone/Weaviate later)
 */
class InMemoryVectorDB {
  constructor() {
    this.vectors = new Map();
  }

  /**
   * Add or update a vector
   */
  async upsert({ id, vector, text, metadata }) {
    this.vectors.set(id, {
      id,
      vector,
      text,
      metadata: metadata || {},
      createdAt: Date.now()
    });

    return id;
  }

  /**
   * Query similar vectors
   */
  async query({ vector, topK = 10, filters = {} }) {
    const results = [];

    for (const [id, doc] of this.vectors) {
      // Apply filters
      if (filters.source && doc.metadata.source !== filters.source) {
        continue;
      }

      // Calculate cosine similarity
      const similarity = this.cosineSimilarity(vector, doc.vector);

      results.push({
        id,
        text: doc.text,
        metadata: doc.metadata,
        score: similarity
      });
    }

    // Sort by similarity and return topK
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  }

  /**
   * Update metadata
   */
  async updateMetadata(id, updates) {
    const doc = this.vectors.get(id);
    if (!doc) return;

    doc.metadata = {
      ...doc.metadata,
      ...updates
    };
  }

  /**
   * Get database size
   */
  size() {
    return this.vectors.size;
  }

  /**
   * Calculate cosine similarity
   * @private
   */
  cosineSimilarity(a, b) {
    if (!a || !b || a.length !== b.length) return 0;

    let dotProduct = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }

    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }
}

/**
 * Adaptive Embeddings - Changes strategy based on what works
 */
class AdaptiveEmbeddings {
  constructor(anthropic, config) {
    this.anthropic = anthropic;
    this.config = config;
    this.strategies = ['semantic', 'syntactic', 'hybrid'];
    this.performance = new Map();
  }

  /**
   * Generate embedding for text
   */
  async embed(text, context = {}) {
    // For MVP, use simple word embedding simulation
    // In production, use Anthropic's embeddings API or OpenAI
    const strategy = this.selectStrategy(context);

    const embedding = await this.generateEmbedding(text, strategy);

    return {
      vector: embedding,
      strategy,
      timestamp: Date.now()
    };
  }

  /**
   * Generate embeddings for multiple texts
   */
  async embedBatch(texts) {
    const embeddings = [];

    for (const text of texts) {
      const embedding = await this.embed(text);
      embeddings.push(embedding);
    }

    return embeddings;
  }

  /**
   * Select best embedding strategy
   * @private
   */
  selectStrategy(context) {
    const contextType = this.classifyContext(context);
    const strategies = this.performance.get(contextType) || this.strategies;

    // Epsilon-greedy: 90% exploit, 10% explore
    if (Math.random() < 0.9) {
      return strategies[0];
    } else {
      return strategies[Math.floor(Math.random() * strategies.length)];
    }
  }

  /**
   * Classify context type
   * @private
   */
  classifyContext(context) {
    if (context.industry) return context.industry;
    if (context.type) return context.type;
    return 'general';
  }

  /**
   * Generate embedding (simple simulation for MVP)
   * @private
   */
  async generateEmbedding(text, strategy) {
    // Simple bag-of-words embedding (replace with real embeddings)
    const words = text.toLowerCase().split(/\s+/);
    const embedding = new Array(384).fill(0); // 384-dimensional

    for (let i = 0; i < words.length; i++) {
      const word = words[i];
      const hash = this.simpleHash(word);
      embedding[hash % 384] += 1;
    }

    // Normalize
    const norm = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
    return embedding.map(val => val / (norm || 1));
  }

  /**
   * Simple hash function
   * @private
   */
  simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash);
  }
}

/**
 * Chunk Optimizer - Learns optimal chunk sizes
 */
class ChunkOptimizer {
  async optimalChunk(text) {
    // Simple chunking: split into paragraphs/sections
    const chunks = [];
    const paragraphs = text.split(/\n\n+/);

    for (const para of paragraphs) {
      if (para.trim().length > 0) {
        // If paragraph is too long, split further
        if (para.length > 500) {
          const sentences = para.split(/[.!?]+/);
          let currentChunk = '';

          for (const sentence of sentences) {
            if (currentChunk.length + sentence.length > 500) {
              if (currentChunk.trim()) chunks.push(currentChunk.trim());
              currentChunk = sentence;
            } else {
              currentChunk += sentence + '. ';
            }
          }

          if (currentChunk.trim()) chunks.push(currentChunk.trim());
        } else {
          chunks.push(para.trim());
        }
      }
    }

    return chunks.length > 0 ? chunks : [text];
  }

  async analyzeContent(text) {
    const words = text.split(/\s+/).length;
    const sentences = text.split(/[.!?]+/).length;

    return {
      wordCount: words,
      sentenceCount: sentences,
      avgSentenceLength: words / sentences,
      hasCode: text.includes('```') || text.includes('function') || text.includes('class')
    };
  }
}

/**
 * Retrieval Learner - Learns which strategies work best
 */
class RetrievalLearner {
  constructor() {
    this.retrievals = new Map();
    this.strategies = [
      { name: 'standard', topK: 10, filters: {} },
      { name: 'high_recall', topK: 20, filters: {} },
      { name: 'high_precision', topK: 5, filters: { confidence: 0.7 } }
    ];
    this.performance = new Map();
    this.totalRetrievals = 0;
    this.avgRetrievalTime = 0;
  }

  async getBestStrategy(context) {
    // Simple: use standard strategy for MVP
    return this.strategies[0];
  }

  logRetrieval(data) {
    const id = `retrieval-${Date.now()}`;
    this.retrievals.set(id, data);
    this.totalRetrievals++;
    return id;
  }

  getRetrieval(id) {
    return this.retrievals.get(id);
  }

  async learn({ strategy, outcome, context }) {
    const strategyName = strategy.name || 'standard';
    const current = this.performance.get(strategyName) || { successes: 0, failures: 0 };

    if (outcome) {
      current.successes++;
    } else {
      current.failures++;
    }

    this.performance.set(strategyName, current);
  }

  getStrategyPerformance() {
    const stats = {};
    for (const [name, perf] of this.performance) {
      stats[name] = {
        successRate: perf.successes / (perf.successes + perf.failures),
        total: perf.successes + perf.failures
      };
    }
    return stats;
  }
}

module.exports = {
  SelfBuildingRAG,
  InMemoryVectorDB,
  AdaptiveEmbeddings,
  ChunkOptimizer,
  RetrievalLearner
};

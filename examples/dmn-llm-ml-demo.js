/**
 * DMN-LLM-ML System Demo
 * Demonstrates the world's first self-evolving AI with exponential learning
 *
 * @copyright 2025 CircuitOS™
 */

const { IntegratedDMNLLMMLSystem } = require('../lib/dmn-llm-ml');

async function main() {
  console.log('═══════════════════════════════════════════════════');
  console.log('   DMN-LLM-ML INTERACTIVE KNOWLEDGE SYSTEM DEMO');
  console.log('   World\'s First Self-Evolving AI');
  console.log('═══════════════════════════════════════════════════\n');

  // Initialize system
  const system = new IntegratedDMNLLMMLSystem({
    anthropicApiKey: process.env.ANTHROPIC_API_KEY
  });

  await system.initialize();

  console.log('\n📋 DEMO SCENARIO: Gym Lead Conversion\n');

  // Simulate a series of interactions
  const interactions = [
    {
      input: 'Do you have personal training?',
      context: {
        industry: 'gym',
        leadDistance: '0.8mi',
        timeOfDay: 'evening'
      },
      outcome: {
        converted: true,
        revenue: 500,
        timeToConversion: '2 hours'
      }
    },
    {
      input: 'What are your membership rates?',
      context: {
        industry: 'gym',
        leadDistance: '1.2mi',
        timeOfDay: 'morning'
      },
      outcome: {
        converted: false,
        revenue: 0
      }
    },
    {
      input: 'Are you open 24/7?',
      context: {
        industry: 'gym',
        leadDistance: '0.5mi',
        timeOfDay: 'night'
      },
      outcome: {
        converted: true,
        revenue: 300,
        timeToConversion: '4 hours'
      }
    }
  ];

  // Process each interaction
  for (let i = 0; i < interactions.length; i++) {
    console.log(`\n🔹 INTERACTION ${i + 1}/${interactions.length}`);
    console.log(`   Input: "${interactions[i].input}"`);

    const result = await system.processInteraction(interactions[i]);

    console.log(`\n   📊 Results:`);
    console.log(`   - Response: ${result.response}`);
    console.log(`   - Outcome: ${result.outcome.converted ? '✓ CONVERTED' : '✗ NO CONVERSION'}`);
    console.log(`   - Revenue: $${result.outcome.revenue || 0}`);
    console.log(`   - Strategy Used: ${result.derivative}`);
    console.log(`   - Learning Rate: ${result.learning.learningRate.toFixed(2)}x`);
    console.log(`   - Acceleration: ${result.learning.acceleration.toFixed(2)}x`);
    console.log(`   - New Concepts: ${result.newKnowledge.novelConcepts.length}`);

    if (result.alternatives.length > 0) {
      console.log(`\n   💡 Non-Traditional Alternatives:`);
      result.alternatives.slice(0, 3).forEach((alt, idx) => {
        console.log(`      ${idx + 1}. [${alt.type}] ${alt.approach}`);
      });
    }
  }

  // Show final system stats
  console.log('\n\n═══════════════════════════════════════════════════');
  console.log('   FINAL SYSTEM STATISTICS');
  console.log('═══════════════════════════════════════════════════\n');

  const stats = system.getStats();

  console.log('📚 Knowledge Graph:');
  console.log(`   - Total Concepts: ${stats.knowledgeGraph.totalConcepts}`);
  console.log(`   - Total Relationships: ${stats.knowledgeGraph.totalRelationships}`);
  console.log(`   - Emergent Patterns: ${stats.knowledgeGraph.emergentPatterns}`);

  console.log('\n🔍 RAG System:');
  console.log(`   - Indexed Documents: ${stats.rag.totalDocuments}`);
  console.log(`   - Total Retrievals: ${stats.rag.totalRetrievals}`);

  console.log('\n🚀 Learning System:');
  console.log(`   - Total Learning Events: ${stats.learning.totalLearningEvents}`);
  console.log(`   - Avg Acceleration: ${stats.learning.avgAcceleration.toFixed(2)}x`);

  console.log('\n🔀 Derivatives System:');
  console.log(`   - Active Strategies: ${stats.derivatives.totalDerivatives}`);
  console.log('\n   Strategy Performance:');
  stats.derivatives.activeStrategies.forEach(s => {
    console.log(`      - ${s.id}: ${(s.successRate * 100).toFixed(1)}% (${s.interactions} interactions)`);
  });

  // Demonstrate system evolution
  console.log('\n\n═══════════════════════════════════════════════════');
  console.log('   DEMONSTRATING SYSTEM EVOLUTION');
  console.log('═══════════════════════════════════════════════════\n');

  const evolution = await system.evolveSystem();

  console.log('\n🧬 Evolution Results:');
  console.log(`   - Strategies Killed: ${evolution.derivativeEvolution.killed.length}`);
  console.log(`   - Strategies Boosted: ${evolution.derivativeEvolution.boosted.length}`);
  console.log(`   - New Strategies Spawned: ${evolution.derivativeEvolution.newDerivatives.length}`);
  console.log(`   - Experiments Created: ${evolution.derivativeEvolution.experiments.length}`);
  console.log(`   - Breakthroughs Discovered: ${evolution.breakthroughs.length}`);

  if (evolution.breakthroughs.length > 0) {
    console.log('\n   💫 Breakthrough Hypotheses:');
    evolution.breakthroughs.forEach((b, idx) => {
      console.log(`      ${idx + 1}. ${b.name}: ${b.hypothesis}`);
    });
  }

  // Export final state
  const state = await system.exportState();

  console.log('\n\n═══════════════════════════════════════════════════');
  console.log('   DEMO COMPLETE');
  console.log('═══════════════════════════════════════════════════\n');

  console.log('✅ System successfully demonstrated:');
  console.log('   ✓ Interactive Knowledge Generation');
  console.log('   ✓ Self-Building RAG');
  console.log('   ✓ Exponential Learning');
  console.log('   ✓ Isolated Derivatives');
  console.log('   ✓ Non-Traditional Path Suggestions');
  console.log('   ✓ System Evolution');

  console.log('\n📊 Final State Exported');
  console.log(`   Timestamp: ${new Date(state.timestamp).toISOString()}`);

  console.log('\n🎯 This is the world\'s first DMN-LLM-ML system!');
  console.log('\n');
}

// Run demo
if (require.main === module) {
  main().catch(error => {
    console.error('\n❌ Demo failed:', error);
    process.exit(1);
  });
}

module.exports = { main };

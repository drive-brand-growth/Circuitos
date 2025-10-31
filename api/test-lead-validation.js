/**
 * Test endpoint for Virtual LPR™ lead validation
 *
 * Test scenarios:
 * 1. High-intent GMB direction click
 * 2. Website visit from nearby location
 * 3. Low-quality far away visitor
 */

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'text/html');

  const html = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Virtual LPR™ - Test Lead Validation</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 40px 20px;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
    }
    .header {
      text-align: center;
      color: white;
      margin-bottom: 40px;
    }
    .header h1 {
      font-size: 2.5rem;
      margin-bottom: 10px;
    }
    .header p {
      font-size: 1.1rem;
      opacity: 0.9;
    }
    .test-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    .test-card {
      background: white;
      border-radius: 12px;
      padding: 25px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .test-card h3 {
      color: #667eea;
      margin-bottom: 15px;
      font-size: 1.3rem;
    }
    .test-scenario {
      background: #f7f7f7;
      padding: 15px;
      border-radius: 8px;
      margin-bottom: 15px;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .test-scenario strong {
      color: #333;
      display: block;
      margin-bottom: 5px;
    }
    button {
      width: 100%;
      padding: 15px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s;
    }
    button:hover {
      transform: translateY(-2px);
    }
    button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .result {
      margin-top: 15px;
      padding: 15px;
      border-radius: 8px;
      font-size: 0.9rem;
      line-height: 1.6;
      display: none;
    }
    .result.show {
      display: block;
    }
    .result.qualified {
      background: #d4edda;
      border: 2px solid #28a745;
      color: #155724;
    }
    .result.not-qualified {
      background: #f8d7da;
      border: 2px solid #dc3545;
      color: #721c24;
    }
    .result.error {
      background: #fff3cd;
      border: 2px solid #ffc107;
      color: #856404;
    }
    .loading {
      text-align: center;
      padding: 20px;
    }
    .spinner {
      border: 3px solid #f3f3f3;
      border-top: 3px solid #667eea;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      animation: spin 1s linear infinite;
      margin: 0 auto;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    pre {
      background: #2d2d2d;
      color: #f8f8f2;
      padding: 15px;
      border-radius: 8px;
      overflow-x: auto;
      font-size: 0.85rem;
      margin-top: 10px;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-top: 10px;
    }
    .stat {
      background: #f0f0f0;
      padding: 10px;
      border-radius: 6px;
      text-align: center;
    }
    .stat-label {
      font-size: 0.75rem;
      color: #666;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .stat-value {
      font-size: 1.5rem;
      font-weight: bold;
      color: #667eea;
      margin-top: 5px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎯 Virtual LPR™ Test Console</h1>
      <p>Test lead validation with different scenarios</p>
    </div>

    <div class="test-grid">
      <!-- Test 1: High Intent GMB -->
      <div class="test-card">
        <h3>✅ Test 1: High-Intent GMB</h3>
        <div class="test-scenario">
          <strong>Scenario:</strong>
          User clicked "Get Directions" on Google My Business listing from 2 miles away in affluent ZIP code.
        </div>
        <button onclick="runTest('gmb-high-intent')">Run Test</button>
        <div id="result-gmb-high-intent" class="result"></div>
      </div>

      <!-- Test 2: Website Visit -->
      <div class="test-card">
        <h3>📊 Test 2: Website Visit</h3>
        <div class="test-scenario">
          <strong>Scenario:</strong>
          User visited pricing page from 7 miles away, spent 3 minutes on site.
        </div>
        <button onclick="runTest('website-visit')">Run Test</button>
        <div id="result-website-visit" class="result"></div>
      </div>

      <!-- Test 3: Low Quality -->
      <div class="test-card">
        <h3>❌ Test 3: Low Quality Lead</h3>
        <div class="test-scenario">
          <strong>Scenario:</strong>
          User viewed homepage from 30 miles away, low income area, 10 second visit.
        </div>
        <button onclick="runTest('low-quality')">Run Test</button>
        <div id="result-low-quality" class="result"></div>
      </div>
    </div>
  </div>

  <script>
    const testData = {
      'gmb-high-intent': {
        signal_type: 'gmb_view',
        signal_data: {
          action: 'directions',
          location: {
            city: 'Arlington',
            zip_code: '76011',
            lat: 32.7450,
            lng: -97.1180
          },
          timestamp: new Date().toISOString()
        },
        business: {
          name: 'MetroFlex Gym',
          city: 'Arlington',
          state: 'Texas',
          lat: 32.7357,
          lng: -97.1081,
          type: 'Hardcore powerlifting/strongman gym',
          target_radius_miles: 10,
          max_distance_miles: 25
        }
      },
      'website-visit': {
        signal_type: 'website_visit',
        signal_data: {
          page_url: '/pricing',
          session_duration: 180,
          pages_viewed: 5,
          location: {
            city: 'Fort Worth',
            zip_code: '76107',
            lat: 32.7555,
            lng: -97.3308
          },
          ip_address: '8.8.8.8',
          source: 'google',
          medium: 'organic',
          timestamp: new Date().toISOString()
        },
        business: {
          name: 'MetroFlex Gym',
          city: 'Arlington',
          state: 'Texas',
          lat: 32.7357,
          lng: -97.1081,
          type: 'Hardcore powerlifting/strongman gym',
          target_radius_miles: 10,
          max_distance_miles: 25
        }
      },
      'low-quality': {
        signal_type: 'website_visit',
        signal_data: {
          page_url: '/',
          session_duration: 10,
          pages_viewed: 1,
          location: {
            city: 'Dallas',
            zip_code: '75201',
            lat: 32.7767,
            lng: -96.7970
          },
          bounce: true,
          timestamp: new Date().toISOString()
        },
        business: {
          name: 'MetroFlex Gym',
          city: 'Arlington',
          state: 'Texas',
          lat: 32.7357,
          lng: -97.1081,
          type: 'Hardcore powerlifting/strongman gym',
          target_radius_miles: 10,
          max_distance_miles: 25
        }
      }
    };

    async function runTest(testId) {
      const button = event.target;
      const resultDiv = document.getElementById(\`result-\${testId}\`);

      button.disabled = true;
      resultDiv.className = 'result show';
      resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p style="margin-top: 10px;">Validating lead...</p></div>';

      try {
        const response = await fetch('/api/virtual-lpr', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(testData[testId])
        });

        const data = await response.json();

        if (data.success && data.qualified) {
          resultDiv.className = 'result show qualified';
          resultDiv.innerHTML = \`
            <strong>✅ LEAD QUALIFIED</strong>
            <div class="stats">
              <div class="stat">
                <div class="stat-label">Signal Score</div>
                <div class="stat-value">\${data.detection.signal_strength}</div>
              </div>
              <div class="stat">
                <div class="stat-label">LPR Score</div>
                <div class="stat-value">\${data.detection.predicted_lpr_score}</div>
              </div>
              <div class="stat">
                <div class="stat-label">Distance</div>
                <div class="stat-value">\${data.detection.enrichment_summary.distance_miles || 'N/A'} mi</div>
              </div>
            </div>
            <p style="margin-top: 10px;"><strong>Reasoning:</strong> \${data.detection.reasoning}</p>
            <p style="margin-top: 10px;"><strong>Tags:</strong> \${data.detection.initial_tags.join(', ')}</p>
            <p style="margin-top: 10px;"><strong>Next Step:</strong> \${data.ghl_integration.next_workflow}</p>
          \`;
        } else if (data.success && !data.qualified) {
          resultDiv.className = 'result show not-qualified';
          resultDiv.innerHTML = \`
            <strong>❌ LEAD NOT QUALIFIED</strong>
            <p style="margin-top: 10px;"><strong>Signal Score:</strong> \${data.detection.signal_strength}/100</p>
            <p style="margin-top: 10px;"><strong>Reasoning:</strong> \${data.detection.reasoning}</p>
            <p style="margin-top: 10px;"><strong>Recommendation:</strong> \${data.detection.recommended_action}</p>
          \`;
        } else {
          throw new Error(data.error || 'Unknown error');
        }

        // Show full response
        resultDiv.innerHTML += \`<details style="margin-top: 15px;"><summary style="cursor: pointer; font-weight: 600;">View Full Response</summary><pre>\${JSON.stringify(data, null, 2)}</pre></details>\`;

      } catch (error) {
        resultDiv.className = 'result show error';
        resultDiv.innerHTML = \`
          <strong>⚠️ ERROR</strong>
          <p style="margin-top: 10px;">\${error.message}</p>
          <p style="margin-top: 10px; font-size: 0.85rem;">Make sure ANTHROPIC_API_KEY is set in your environment variables.</p>
        \`;
      } finally {
        button.disabled = false;
      }
    }
  </script>
</body>
</html>
  `;

  res.status(200).send(html);
}

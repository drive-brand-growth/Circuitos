# Circuit OS Landing Page

## Live Demo

The Circuit OS landing page is now running with live metrics!

### Access the Site

**Local Access:**
- URL: `http://localhost:8080`
- The server is running on port 8080

### Features

- **Live Metrics Dashboard**: Real-time animated metrics showing:
  - Pipeline Activated (0% → 92%)
  - Meetings Booked (0 → 18)
  - Revenue Recovered ($0 → $482,900)

- **Interactive Elements**:
  - Deploy Quick Switch button
  - Enter Operator Mode button (toggles signal indicator)
  - Expandable revenue details dropdown

- **Design System**:
  - Dark theme (#0A0B0C background)
  - Industrial operator aesthetic
  - Eurostile font family for headers
  - JetBrains Mono for metrics
  - Animated signal indicators

### Running the Server

The server is currently running in the background. To manage it:

**Start the server:**
```bash
cd Active/circuit-os-landing
python3 -m http.server 8080
```

**Stop the server:**
```bash
# Find the process
ps aux | grep "http.server 8080" | grep -v grep

# Kill it (replace PID with actual process ID)
kill <PID>
```

**Check server status:**
```bash
curl -I http://localhost:8080
```

### File Structure

```
Active/circuit-os-landing/
├── index.html          # Main landing page with live metrics
└── README.md          # This file
```

### Deployment Notes

This is a static HTML page that can be deployed to:
- Railway (add to existing deployment)
- Vercel/Netlify (static hosting)
- Any web server (nginx, Apache, etc.)

For production deployment, update the port configuration in your deployment platform's settings.

---

**Server Status**: ✅ Running on port 8080
**Last Updated**: 2025-11-17

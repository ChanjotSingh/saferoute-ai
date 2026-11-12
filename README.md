# SafeRoute AI

An interactive, browser-based demonstration of **Intelligent Traffic Accident Risk Prediction and Hotspot Analysis Using Machine Learning**.

## Run it

The project has no external Python dependencies. For the complete dashboard plus ML API, run:

```powershell
python backend/server.py
```

Then visit `http://localhost:8001`.

For a containerized deployment, see [DEPLOYMENT.md](DEPLOYMENT.md).

## What is included

- A Leaflet map with clustered historical-accident hotspot zones
- Interactive risk scoring from time, weather, road type, traffic volume, and speed limit
- Explainable contributing factors and recommended interventions
- Model comparison metrics and a small evaluation chart
- A dependency-free logistic-regression API with synthetic training data, clearly marked as demonstrative

For production use, replace the `hotspots` and `accidents` arrays in `app.js` with validated historical data and call a trained model through a protected backend API. This prototype is a decision-support demonstration, not a real-time safety service.

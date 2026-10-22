def get_advisory_suggestions(n, p, k, humidity, ph, score_label):
    suggestions = []
    if n < 20: suggestions.append("⚠️ **Nitrogen is low** — apply Urea at 50–60 kg/acre or use DAP.")
    if p < 15: suggestions.append("⚠️ **Phosphorus is low** — apply Single Superphosphate (SSP) at 35–40 kg/acre.")
    if k < 15: suggestions.append("⚠️ **Potassium is low** — apply Muriate of Potash (MOP) at 20–25 kg/acre.")
    if humidity < 30: suggestions.append("💧 **Soil moisture is low** — irrigate regularly or consider drip irrigation.")
    if ph < 5.5: suggestions.append("🧪 **Soil is too acidic** — apply agricultural lime to raise pH.")
    if ph > 8.0: suggestions.append("🧪 **Soil is too alkaline** — apply gypsum or sulfur to lower pH.")
    if score_label == "Poor": suggestions.append("🛑 **Overall soil health is poor** — consider a full nutrient management plan.")
    if not suggestions: suggestions.append("✅ **All measured metrics are within optimal baselines!** Proceed with standard schedules.")
    return suggestions

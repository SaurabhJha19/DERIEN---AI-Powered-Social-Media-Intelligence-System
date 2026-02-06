ARCHETYPES = {
    "normal": {
        "posts_per_day": (1, 2),
        "risk_bias": 0.05
    },
    "low_signal_seller": {
        "posts_per_day": (3, 5),
        "risk_bias": 0.3
    },
    "high_risk_trafficker": {
        "posts_per_day": (6, 10),
        "risk_bias": 0.8
    },
    "burner": {
        "posts_per_day": (4, 8),
        "risk_bias": 0.7,
        "account_age_days": (5, 30)
    }
}

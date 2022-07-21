from prediction.prediction import Predictor
predictor = Predictor(model_path='models/gcnae.pkl')


new_sample = {
    'athlete_id_real': 153,
    'specific_gravity': 1.016,
    'in_competition': True,
    'adiol': 27.22,
    'bdiol': 144.12,
    'androsterone': 2254.7,
    'etiocholanolone': 2364.2,
    'epitestosterone': 6.08,
    'testosterone': 5.92,
    't_e_ratio': 0.85,
    'andro_t_ratio': 380.86,
    'andro_etio_ratio': 0.95,
    'adiol_bdiol_ratio': 0.19,
    'adiol_e_ratio': 4.48,
    'adiol_corr': 34.03,
    'bdiol_corr': 180.15,
    'androsterone_corr': 2818.38,
    'etiocholanolone_corr': 2955.25,
    'epitestosterone_corr': 7.6,
    'testosterone_corr': 7.4,
#     'total_observations': 4,
    'is_male': False,
#     'sample_id': 40,
    'athlete_id': 153
}

anomaly_score = predictor.predict_sample(new_sample)
print(anomaly_score)
"""
Thin wrapper around your existing GNN‐based inference in pka_predictor/GNN/predict.py
"""
def predict(input_data, pH: float = 7.4, **kwargs):
    # import the only function you need, as it already lives in GNN/predict.py
    from .GNN.predict import predict as _gnn_predict
    return _gnn_predict(input_data, pH=pH, **kwargs)
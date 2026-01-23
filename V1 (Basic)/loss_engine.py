import numpy as np
def mse_loss(y_true,y_pred):
    return np.mean(np.square(y_true-y_pred))
real_value=np.array([1,0,1])
pred_value=np.array([0.9,0.2,0.4])
error=mse_loss(real_value,pred_value)
print(f"The AI was off by {error:.4f}")
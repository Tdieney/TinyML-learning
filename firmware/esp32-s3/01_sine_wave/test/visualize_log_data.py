import re
import matplotlib.pyplot as plt
import numpy as np

# 1. Raw log data from ESP32 TFLM execution
log_data = """
I (323) SINE_WAVE_INFERENCE: x = 0.00, y_pred = 0.0414
I (423) SINE_WAVE_INFERENCE: x = 0.10, y_pred = 0.1077
I (523) SINE_WAVE_INFERENCE: x = 0.20, y_pred = 0.1987
I (623) SINE_WAVE_INFERENCE: x = 0.30, y_pred = 0.2816
I (723) SINE_WAVE_INFERENCE: x = 0.40, y_pred = 0.3809
I (823) SINE_WAVE_INFERENCE: x = 0.50, y_pred = 0.4555
I (923) SINE_WAVE_INFERENCE: x = 0.60, y_pred = 0.5465
I (1023) SINE_WAVE_INFERENCE: x = 0.70, y_pred = 0.6045
I (1123) SINE_WAVE_INFERENCE: x = 0.80, y_pred = 0.7122
I (1223) SINE_WAVE_INFERENCE: x = 0.90, y_pred = 0.7784
I (1323) SINE_WAVE_INFERENCE: x = 1.00, y_pred = 0.8198
I (1423) SINE_WAVE_INFERENCE: x = 1.10, y_pred = 0.8861
I (1523) SINE_WAVE_INFERENCE: x = 1.20, y_pred = 0.8943
I (1623) SINE_WAVE_INFERENCE: x = 1.30, y_pred = 0.9854
I (1723) SINE_WAVE_INFERENCE: x = 1.40, y_pred = 0.9937
I (1823) SINE_WAVE_INFERENCE: x = 1.50, y_pred = 1.0103
I (1923) SINE_WAVE_INFERENCE: x = 1.60, y_pred = 1.0517
I (2023) SINE_WAVE_INFERENCE: x = 1.70, y_pred = 1.0103
I (2123) SINE_WAVE_INFERENCE: x = 1.80, y_pred = 0.9772
I (2223) SINE_WAVE_INFERENCE: x = 1.90, y_pred = 0.9358
I (2323) SINE_WAVE_INFERENCE: x = 2.00, y_pred = 0.8943
I (2423) SINE_WAVE_INFERENCE: x = 2.10, y_pred = 0.8447
I (2523) SINE_WAVE_INFERENCE: x = 2.20, y_pred = 0.8033
I (2623) SINE_WAVE_INFERENCE: x = 2.30, y_pred = 0.7039
I (2723) SINE_WAVE_INFERENCE: x = 2.40, y_pred = 0.6542
I (2823) SINE_WAVE_INFERENCE: x = 2.50, y_pred = 0.5465
I (2923) SINE_WAVE_INFERENCE: x = 2.60, y_pred = 0.4803
I (3023) SINE_WAVE_INFERENCE: x = 2.70, y_pred = 0.4058
I (3123) SINE_WAVE_INFERENCE: x = 2.80, y_pred = 0.3230
I (3223) SINE_WAVE_INFERENCE: x = 2.90, y_pred = 0.2153
I (3323) SINE_WAVE_INFERENCE: x = 3.00, y_pred = 0.1325
I (3423) SINE_WAVE_INFERENCE: x = 3.10, y_pred = 0.0331
I (3523) SINE_WAVE_INFERENCE: x = 3.20, y_pred = -0.0414
I (3623) SINE_WAVE_INFERENCE: x = 3.30, y_pred = -0.1656
I (3723) SINE_WAVE_INFERENCE: x = 3.40, y_pred = -0.2401
I (3823) SINE_WAVE_INFERENCE: x = 3.50, y_pred = -0.3726
I (3923) SINE_WAVE_INFERENCE: x = 3.60, y_pred = -0.4555
I (4023) SINE_WAVE_INFERENCE: x = 3.70, y_pred = -0.5797
I (4123) SINE_WAVE_INFERENCE: x = 3.80, y_pred = -0.6625
I (4223) SINE_WAVE_INFERENCE: x = 3.90, y_pred = -0.7453
I (4323) SINE_WAVE_INFERENCE: x = 4.00, y_pred = -0.8529
I (4423) SINE_WAVE_INFERENCE: x = 4.10, y_pred = -0.8861
I (4523) SINE_WAVE_INFERENCE: x = 4.20, y_pred = -0.8943
I (4623) SINE_WAVE_INFERENCE: x = 4.30, y_pred = -0.9358
I (4723) SINE_WAVE_INFERENCE: x = 4.40, y_pred = -0.9523
I (4823) SINE_WAVE_INFERENCE: x = 4.50, y_pred = -0.9772
I (4923) SINE_WAVE_INFERENCE: x = 4.60, y_pred = -0.9937
I (5023) SINE_WAVE_INFERENCE: x = 4.70, y_pred = -0.9937
I (5123) SINE_WAVE_INFERENCE: x = 4.80, y_pred = -1.0434
I (5223) SINE_WAVE_INFERENCE: x = 4.90, y_pred = -1.0517
I (5323) SINE_WAVE_INFERENCE: x = 5.00, y_pred = -0.9854
I (5423) SINE_WAVE_INFERENCE: x = 5.10, y_pred = -0.9026
I (5523) SINE_WAVE_INFERENCE: x = 5.20, y_pred = -0.8447
I (5623) SINE_WAVE_INFERENCE: x = 5.30, y_pred = -0.7867
I (5723) SINE_WAVE_INFERENCE: x = 5.40, y_pred = -0.7204
I (5823) SINE_WAVE_INFERENCE: x = 5.50, y_pred = -0.6625
I (5923) SINE_WAVE_INFERENCE: x = 5.60, y_pred = -0.5962
I (6023) SINE_WAVE_INFERENCE: x = 5.70, y_pred = -0.5134
I (6123) SINE_WAVE_INFERENCE: x = 5.80, y_pred = -0.4886
I (6223) SINE_WAVE_INFERENCE: x = 5.90, y_pred = -0.3892
I (6323) SINE_WAVE_INFERENCE: x = 6.00, y_pred = -0.3478
I (6423) SINE_WAVE_INFERENCE: x = 6.10, y_pred = -0.2981
I (6523) SINE_WAVE_INFERENCE: x = 6.20, y_pred = -0.2070
"""

# 2. Parse the log data using regular expressions
x_values = []
y_preds = []

# Regex pattern to extract x and y_pred floating-point values
pattern = r"x = ([\d\.-]+),\s+y_pred = ([\d\.-]+)"
matches = re.findall(pattern, log_data)

for match in matches:
    x_values.append(float(match[0]))
    y_preds.append(float(match[1]))

# Convert parsed lists to numpy arrays for plotting
x_arr = np.array(x_values)
y_pred_arr = np.array(y_preds)

# print("Y_pred array:", y_pred_arr)

# 3. Generate ideal reference sine wave for benchmarking
x_ideal = np.linspace(0, 6.2, 500)
y_ideal = np.sin(x_ideal)

# 4. Configure and plot the data via Matplotlib
plt.figure(figsize=(10, 6))

# Plot the ideal reference curve
plt.plot(x_ideal, y_ideal, label='Ideal Sine Wave', color='gray', linestyle='--', alpha=0.7)

# Plot the actual quantized model inference data
plt.plot(x_arr, y_pred_arr, label='TFLM y_pred (Quantized)', color='#1f77b4', linewidth=2)
plt.scatter(x_arr, y_pred_arr, color='red', s=15, zorder=3, label='Inference Points')

# Adjust layout, labels, and axes styling
plt.title('TensorFlow Lite Micro - Sine Inference Verification on ESP32', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Input (x)', fontsize=12)
plt.ylabel('Output (y)', fontsize=12)
plt.xlim(-0.2, 6.4)
plt.ylim(-1.2, 1.2)
plt.axhline(0, color='black', linewidth=0.8, linestyle=':')
plt.axvline(0, color='black', linewidth=0.8, linestyle=':')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right', frameon=True)

# Render the layout and display the window
plt.tight_layout()
plt.show()

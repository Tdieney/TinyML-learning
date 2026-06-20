#include <stdio.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"

// TensorFlow Lite Micro headers
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

static const char* TAG = "SINE_WAVE_INFERENCE";

// Model variables defined in model.cc
extern unsigned char g_model[];
extern unsigned int g_model_len;

// Define a Tensor Arena size (TFLM needs this memory space for input, output, and intermediate tensors)
// 10 KB is more than enough for this small sine wave model.
constexpr int kTensorArenaSize = 2 * 1024;
// Must align to 16 bytes for hardware compatibility
alignas(16) static uint8_t tensor_arena[kTensorArenaSize];

extern "C" void app_main(void)
{
    ESP_LOGI(TAG, "Starting TinyML Sine Wave Inference...");

    // 1. Map the model into a usable data structure
    const tflite::Model* model = tflite::GetModel(g_model);
    if (model->version() != TFLITE_SCHEMA_VERSION)
    {
        ESP_LOGE(TAG,
                 "Model schema version %d is not equal to supported version %d.",
                 (int) model->version(),
                 (int) TFLITE_SCHEMA_VERSION);
        return;
    }

    // 2. Register required operators with the MicroMutableOpResolver
    // The quantized sine wave model contains Quantize, FullyConnected, and Dequantize operators.
    static tflite::MicroMutableOpResolver<3> resolver;
    if (resolver.AddQuantize() != kTfLiteOk)
    {
        ESP_LOGE(TAG, "Failed to add Quantize operator.");
        return;
    }
    if (resolver.AddFullyConnected() != kTfLiteOk)
    {
        ESP_LOGE(TAG, "Failed to add FullyConnected operator.");
        return;
    }
    if (resolver.AddDequantize() != kTfLiteOk)
    {
        ESP_LOGE(TAG, "Failed to add Dequantize operator.");
        return;
    }

    // 3. Instantiate the interpreter
    static tflite::MicroInterpreter interpreter(model, resolver, tensor_arena, kTensorArenaSize);

    // 4. Allocate memory from the tensor_arena for the model's tensors
    if (interpreter.AllocateTensors() != kTfLiteOk)
    {
        ESP_LOGE(TAG, "AllocateTensors() failed!");
        return;
    }

    // 5. Obtain pointers to the model's input and output tensors
    TfLiteTensor* input = interpreter.input(0);
    TfLiteTensor* output = interpreter.output(0);

    // Verify input and output tensor characteristics
    if (input->type != kTfLiteFloat32)
    {
        ESP_LOGE(TAG, "Input tensor type is %d, expected kTfLiteFloat32.", input->type);
        return;
    }
    if (output->type != kTfLiteFloat32)
    {
        ESP_LOGE(TAG, "Output tensor type is %d, expected kTfLiteFloat32.", output->type);
        return;
    }

    float x = 0.0f;
    const float kXIncrement = 0.1f;
    const float kTwoPi = 2.0f * 3.1415926535f;

    ESP_LOGI(TAG, "Starting inference loop. Expected vs predicted values will be printed.");

    while (1)
    {
        // Set input value
        input->data.f[0] = x;

        // Run inference
        TfLiteStatus invoke_status = interpreter.Invoke();
        if (invoke_status != kTfLiteOk)
        {
            ESP_LOGE(TAG, "Inference invoke failed with status %d", invoke_status);
            break;
        }

        // Retrieve prediction
        float y_pred = output->data.f[0];

        // Print values in a clean format
        ESP_LOGI(TAG, "x = %.2f, y_pred = %.4f", x, y_pred);

        // Advance x
        x += kXIncrement;
        if (x > kTwoPi)
        {
            x = 0.0f;
        }

        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

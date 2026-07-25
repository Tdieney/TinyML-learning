# TinyML Integration on ESP32-S3 from Scratch

This guide documents the step-by-step process of setting up and building a TensorFlow Lite for Microcontrollers (TFLM) project on the **ESP32-S3** from scratch.

We compile TFLM directly from the source tree (`porting/tflm-tree`) using custom CMake logic, without relying on any pre-packaged IDE components or the Espressif IDF component manager registry.

---

## Project Directory Structure

```text
{project_name}/
├── CMakeLists.txt              # Project top-level CMake configuration
├── sdkconfig                   # Generated during build
├── components/
│   └── tflm/
│       └── CMakeLists.txt      # Custom CMake for compiling TFLM from porting/tflm-tree
└── main/
    ├── CMakeLists.txt          # Main component CMake configuration (compiles main and model)
    └── main.cpp                # Core application code performing the inference loop
```

---

## Integration guidelines


Please refer to the [README.md](..\tflm-tree\README.md) in the `porting/tflm-tree` folder for detailed instructions on how to generate the standalone TFLM source tree.

Create a Blank Project

```bash
cd porting/esp32-s3
idf.py create-project {project_name}
cd {project_name}
```

Rather than pulling the prebuilt `espressif/esp-tflite-micro` from the component registry (which abstracts too much), we compile TFLM directly from our local source tree which is generated in the previous step.

Create a `components/tflm` directory:
   ```bash
   mkdir -p components/tflm
   ```
Write a custom `CMakeLists.txt` in the `components/tflm` directory to register TFLM files and include paths. Refer [here](01_sine_wave\components\tflm\CMakeLists.txt) for the full content.

**Key Highlights of this Configuration:**
- Maps the include directories so any code linking to `tflm` can include TFLM headers correctly (e.g., `#include "tensorflow/lite/..."`).
- Uses `file(GLOB ...)` to dynamically compile all kernels, preventing compilation failures when adding new models.
- Registers `TF_LITE_STATIC_MEMORY` as a `PUBLIC` compile definition, so it propagates automatically to the `main` application code.
- Relaxes several compiler checks (like type-limit warnings) which ESP-IDF treats as compilation errors by default.

The pre-trained model is already serialized as a C++ array inside `models/` folder. Copy and paste it into the `main/` folder of your project. Modify `main/CMakeLists.txt` to register `main.cpp` and our shared model code.

Implement the Inference App Code (C++). Rename the boilerplate `main/{project_name}.c` to `main/main.cpp` and implement the setup and inference loop. Refer to [main.cpp](01_sine_wave\main\main.cpp) for the full implementation.

Build and Flash


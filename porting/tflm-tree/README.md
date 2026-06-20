# Standalone TFLM Tree

This is a guide details the steps taken to set up the environment and successfully generate a standalone TensorFlow Lite for Microcontrollers (TFLM) project tree on **Windows** like this.

---

## Prerequisites & Environment Setup

Clone the `tflite-micro` repository and ensure you have Anaconda installed.

```
git clone https://github.com/tensorflow/tflite-micro.git
```

The TFLM project generation script (`create_tflm_tree.py`) relies on `make` under the hood to compile library file lists and trigger `download_and_extract.sh` for third-party dependencies (like FlatBuffers and KissFFT).

### 1. Create and Activate the Conda Environment
Using the [environment.yaml](../../environment.yaml) file, create and activate your environment:
```bash
conda env create -f environment.yaml
conda activate tflm-dev
```

### 2. Ensure Make and Unix Shell Tools are Available
Since Windows does not natively include Unix tools (`make`, `bash`, `curl`, `tar`, `unzip`), you need to provide them:

* **Recommended Approach**: Run your commands from **Git Bash**. It automatically provides a Bash shell with `curl`, `tar`, `unzip`, `sed`, and other required utilities.
* **Install Make**: If `make` is missing from the environment, install it via Conda:
  ```bash
  conda install -c conda-forge make
  ```

---

## Build File Modifications for Windows Support

To prevent Python invocation errors on Windows (where Python is typically executed as `python` instead of `python3`), I made the following modifications to the build configuration files under `tensorflow/lite/micro/tools/make/`:

### 1. Makefile Modifications
In `tflite-micro/tensorflow/lite/micro/tools/make/Makefile`:
* Declared a dynamic `PYTHON` variable that defaults to `python3` but overrides to `python` when the host operating system is detected as Windows:
  ```makefile
  PYTHON := python3
  ifeq ($(HOST_OS),windows)
    PYTHON := python
  endif
  ```
* Updated all shell command calls in the Makefile from hardcoded `python3` to the dynamic variable `$(PYTHON)`.

### 2. Helper Functions Modifications
In `tflite-micro/tensorflow/lite/micro/tools/make/helper_functions.inc`:
* Replaced the hardcoded `python3` command with `$$(PYTHON)` when calling the test array generation script:
  ```makefile
  GEN_RESULT := $$(shell $$(PYTHON) $(TENSORFLOW_ROOT)tensorflow/lite/micro/tools/generate_cc_arrays.py $$(GENERATED_SRCS_DIR) $(4))
  ```

---

## Generating the Standalone Tree

Run the generation script from the root of the `tflite-micro` repository.

```bash
python tensorflow/lite/micro/tools/project_generation/create_tflm_tree.py tmp/tflm-tree
```

*(Note: Replace `tmp/tflm-tree` with your desired target output path).*

After the script runs successfully, the target directory will look like this:

```bash
tmp/tflm-tree/
├── signal/
├── tensorflow/
├── third_party/
├── LICENSE
```

* **`tensorflow/`**: The core source code and headers for TFLM.
* **`third_party/`**: Only the downloaded third-party headers/sources required for TFLM compilation (FlatBuffers, gemmlowp, kissfft, ruy, etc.).
* **`examples/`** *(Option A only)*: Standalone code for the requested examples with their local `#include` paths pre-adjusted.

## References

You can refer to the original TensorFlow Lite Micro project guideline for more details: [Porting to a new platform](https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/docs/new_platform_support.md)

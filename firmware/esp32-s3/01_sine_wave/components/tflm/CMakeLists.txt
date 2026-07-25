# Component CMakeLists.txt for compiling TensorFlow Lite Micro from porting/tflm-tree

idf_component_register(
    SRCS
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/core/api/flatbuffer_conversions.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/compiler/mlir/lite/core/api/error_reporter.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/compiler/mlir/lite/schema/schema_utils.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/core/api/tensor_utils.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/core/c/common.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/kernels/kernel_util.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/kernels/internal/common.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/kernels/internal/portable_tensor_utils.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/kernels/internal/quantization_util.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/kernels/internal/runtime_shape.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/kernels/internal/tensor_ctypes.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/kernels/internal/tensor_utils.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/memory_planner/greedy_memory_planner.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/memory_planner/linear_memory_planner.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/memory_planner/non_persistent_buffer_planner_shim.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/tflite_bridge/flatbuffer_conversions_bridge.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/tflite_bridge/micro_error_reporter.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/debug_log.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/fake_micro_context.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/flatbuffer_utils.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/hexdump.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/memory_helpers.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_allocation_info.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_allocator.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_context.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_interpreter.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_interpreter_context.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_interpreter_graph.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_log.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_op_resolver.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_profiler.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_resource_variable.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_time.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/micro_utils.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/mock_micro_graph.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/recording_micro_allocator.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/system_setup.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/test_helper_custom_ops.cc"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/test_helpers.cc"
    INCLUDE_DIRS
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/third_party/flatbuffers/include"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/third_party/gemmlowp"
        "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/third_party/ruy"
)

# Find and append all kernel source files dynamically
file(GLOB KERNEL_SRCS "${CMAKE_CURRENT_LIST_DIR}/../../../../tflm-tree/tensorflow/lite/micro/kernels/*.cc")
target_sources(${COMPONENT_LIB} PRIVATE ${KERNEL_SRCS})

# Apply static memory compile flag
target_compile_definitions(${COMPONENT_LIB} PUBLIC TF_LITE_STATIC_MEMORY)

# Disable compiler warnings that are treated as errors by ESP-IDF default build settings
target_compile_options(${COMPONENT_LIB} PRIVATE 
    -Wno-type-limits 
    -Wno-sign-compare 
    -Wno-strict-aliasing
    -Wno-ignored-qualifiers
)

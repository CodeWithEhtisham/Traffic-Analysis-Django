import cv2
import numpy as np
# import onnxruntime as ort
import onnx
import pycuda.driver as cuda
import pycuda.autoinit
# import tensorrt as trt
import torch

def load_model():
    # Check if a GPU is available
    if torch.cuda.is_available():
        # Load the TensorRT model
        # model = trt.tensorrtapi.LoadPlan('best.plan')
        pass
    else:
        # Load the ONNX model
        model = onnx.load('best.onnx')

    return model


# Load the model
model = load_model()

# Prepare the input data
img_path = 'photo6.jpg'
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (640, 640))
input_data = img.transpose(2, 0, 1).astype(np.float32)
input_data /= 255.0

# Run inference on the input data
if isinstance(model): #trt.tensorrtapi.ICudaEngine
    # TensorRT inference
    # Create a TensorRT execution context
    context = model.create_execution_context()

    # Allocate GPU memory for input and output tensors
    input_shape = (1, 3, 640, 640)
    input_binding = context.get_binding_shape(0)
    input_size = np.prod(input_shape) * np.dtype(np.float32).itemsize
    input_buf = cuda.mem_alloc(input_size)

    output_binding = context.get_binding_shape(1)
    output_size = np.prod(output_binding) * np.dtype(np.float32).itemsize
    output_buf = cuda.mem_alloc(output_size)

    # Copy input data to GPU memory
    cuda.memcpy_htod(input_buf, input_data)

    # Run inference
    context.execute_v2(bindings=[int(input_buf), int(output_buf)])

    # Copy output data to CPU memory
    output_data = np.empty(output_binding, dtype=np.float32)
    cuda.memcpy_dtoh(output_data, output_buf)
else:
    # ONNX inference
    output_data = model.run(None, {'input': input_data})

# Process the output data as needed
print(output_data)

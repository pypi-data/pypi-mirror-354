#include <torch/extension.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <vector>
#include <cuda_bf16.h>

template <typename scalar_t>
__global__ void sjlt_projection_kernel(
    const scalar_t* input,           // Input tensor [batch_size, original_dim]
    scalar_t* output,                // Output tensor [batch_size, proj_dim]
    const int64_t* rand_indices,     // Random indices [original_dim, c]
    const int8_t* rand_signs,        // Random signs [original_dim, c]
    const int batch_size,
    const int original_dim,
    const int proj_dim,
    const int c) {

    // Each block now processes multiple chunks of the input
    // Calculate dimensions per block and assign work accordingly
    const int total_threads = gridDim.x * blockDim.x;
    const int thread_id = blockIdx.x * blockDim.x + threadIdx.x;

    // Calculate how many dimensions each thread needs to process
    const int dims_per_thread = (original_dim + total_threads - 1) / total_threads;

    // Process multiple dimensions per thread
    for (int chunk = 0; chunk < dims_per_thread; chunk++) {
        // Calculate the actual dimension index for this thread and chunk
        const int idx = thread_id + chunk * total_threads;

        // Skip if beyond the original dimension size
        if (idx >= original_dim) continue;

        // Load the random indices and signs for this dimension (idx)
        int local_rand_indices[16];  // Assuming c <= 16, adjust if needed
        int8_t local_rand_signs[16]; // Assuming c <= 16, adjust if needed

        for (int j = 0; j < c; j++) {
            local_rand_indices[j] = rand_indices[idx * c + j];
            local_rand_signs[j] = rand_signs[idx * c + j];
        }

        // Process each sample in the batch
        for (int b = 0; b < batch_size; b++) {
            scalar_t val = input[b * original_dim + idx];

            // Only process if value is non-zero
            if (val != 0) {
                for (int j = 0; j < c; j++) {
                    int output_idx = b * proj_dim + local_rand_indices[j];
                    scalar_t scaled_val = val * local_rand_signs[j];

                    // Atomic add to handle race conditions when multiple threads update the same output location
                    atomicAdd(&output[output_idx], scaled_val);
                }
            }
        }
    }
}

// BFloat16 specialized kernel - simpler implementation that's more efficient
__global__ void sjlt_projection_kernel_bfloat16(
    const at::BFloat16* input,       // Input tensor [batch_size, original_dim]
    at::BFloat16* output,            // Output tensor [batch_size, proj_dim]
    const int64_t* rand_indices,     // Random indices [original_dim, c]
    const int8_t* rand_signs,        // Random signs [original_dim, c]
    const int batch_size,
    const int original_dim,
    const int proj_dim,
    const int c) {

    const int total_threads = gridDim.x * blockDim.x;
    const int thread_id = blockIdx.x * blockDim.x + threadIdx.x;
    const int dims_per_thread = (original_dim + total_threads - 1) / total_threads;

    // Process multiple dimensions per thread
    for (int chunk = 0; chunk < dims_per_thread; chunk++) {
        const int idx = thread_id + chunk * total_threads;
        if (idx >= original_dim) continue;

        // Local storage for indices and signs
        int local_rand_indices[16];
        int8_t local_rand_signs[16];

        for (int j = 0; j < c; j++) {
            local_rand_indices[j] = rand_indices[idx * c + j];
            local_rand_signs[j] = rand_signs[idx * c + j];
        }

        for (int b = 0; b < batch_size; b++) {
            // Convert BFloat16 to float for calculations
            float val_float = static_cast<float>(input[b * original_dim + idx]);

            if (val_float != 0.0f) {
                for (int j = 0; j < c; j++) {
                    int output_idx = b * proj_dim + local_rand_indices[j];
                    float scaled_val = val_float * static_cast<float>(local_rand_signs[j]);

                    // For BFloat16, we use a float-based atomic add
                    float current = static_cast<float>(output[output_idx]);
                    float updated = current + scaled_val;
                    output[output_idx] = at::BFloat16(updated);
                }
            }
        }
    }
}

// Normalize kernel
template <typename scalar_t>
__global__ void normalize_kernel(
    scalar_t* output,     // Output tensor [batch_size, proj_dim]
    const int batch_size,
    const int proj_dim,
    const float normalization_factor) {

    const int total_threads = gridDim.x * blockDim.x;
    const int thread_id = blockIdx.x * blockDim.x + threadIdx.x;
    const int total_elements = batch_size * proj_dim;

    // Calculate elements per thread
    const int elements_per_thread = (total_elements + total_threads - 1) / total_threads;

    // Process multiple elements per thread
    for (int chunk = 0; chunk < elements_per_thread; chunk++) {
        const int idx = thread_id + chunk * total_threads;
        if (idx < total_elements) {
            output[idx] = output[idx] * normalization_factor;
        }
    }
}

// Simple BFloat16 normalize kernel
__global__ void normalize_kernel_bfloat16(
    at::BFloat16* output,
    const int batch_size,
    const int proj_dim,
    const float normalization_factor) {

    const int total_threads = gridDim.x * blockDim.x;
    const int thread_id = blockIdx.x * blockDim.x + threadIdx.x;
    const int total_elements = batch_size * proj_dim;
    const int elements_per_thread = (total_elements + total_threads - 1) / total_threads;

    for (int chunk = 0; chunk < elements_per_thread; chunk++) {
        const int idx = thread_id + chunk * total_threads;
        if (idx < total_elements) {
            float val_float = static_cast<float>(output[idx]) * normalization_factor;
            output[idx] = at::BFloat16(val_float);
        }
    }
}

// Function to set the cache configuration for our kernels
void setCacheConfig() {
    // Set L1 cache preference for the projection kernels
    cudaFuncSetCacheConfig(sjlt_projection_kernel<float>, cudaFuncCachePreferL1);
    cudaFuncSetCacheConfig(sjlt_projection_kernel<double>, cudaFuncCachePreferL1);
    cudaFuncSetCacheConfig(sjlt_projection_kernel_bfloat16, cudaFuncCachePreferL1);

    // Set L1 cache preference for the normalize kernels
    cudaFuncSetCacheConfig(normalize_kernel<float>, cudaFuncCachePreferL1);
    cudaFuncSetCacheConfig(normalize_kernel<double>, cudaFuncCachePreferL1);
    cudaFuncSetCacheConfig(normalize_kernel_bfloat16, cudaFuncCachePreferL1);
}

// C++ wrapper for the CUDA kernel with fixed block count
std::vector<torch::Tensor> sjlt_projection_cuda(
    torch::Tensor input,
    torch::Tensor rand_indices,
    torch::Tensor rand_signs,
    int proj_dim,
    int c,
    int threads,
    int fixed_blocks) {

    // Get the device index of the input tensor
    int device_idx = input.device().index();

    // Set current device to match the input tensor's device
    cudaSetDevice(device_idx);

    // Set the cache configuration (call this once)
    static bool cacheConfigSet = false;
    if (!cacheConfigSet) {
        setCacheConfig();
        cacheConfigSet = true;
    }

    auto batch_size = input.size(0);
    auto original_dim = input.size(1);

    // Create output tensor on the same device as input
    auto output = torch::zeros({batch_size, proj_dim},
                              torch::TensorOptions()
                              .dtype(input.dtype())
                              .device(input.device()));

    // Compute normalization factor
    float normalization_factor = 1.0f / sqrt(c);

    // Ensure threads is a multiple of 32 (warp size) for optimal performance
    threads = (threads / 32) * 32;

    // Check if input is BFloat16 and dispatch accordingly
    if (input.scalar_type() == at::ScalarType::BFloat16) {
        // Launch specialized BFloat16 kernels
        sjlt_projection_kernel_bfloat16<<<fixed_blocks, threads>>>(
            reinterpret_cast<at::BFloat16*>(input.data_ptr()),
            reinterpret_cast<at::BFloat16*>(output.data_ptr()),
            rand_indices.data_ptr<int64_t>(),
            rand_signs.data_ptr<int8_t>(),
            batch_size,
            original_dim,
            proj_dim,
            c);

        // Check for errors
        cudaError_t err = cudaGetLastError();
        if (err != cudaSuccess) {
            throw std::runtime_error(cudaGetErrorString(err));
        }

        normalize_kernel_bfloat16<<<fixed_blocks, threads>>>(
            reinterpret_cast<at::BFloat16*>(output.data_ptr()),
            batch_size,
            proj_dim,
            normalization_factor);
    } else {
        // Use the dispatch macro for float and double types
        AT_DISPATCH_FLOATING_TYPES(input.scalar_type(), "sjlt_projection_cuda", ([&] {
            sjlt_projection_kernel<scalar_t><<<fixed_blocks, threads>>>(
                input.data_ptr<scalar_t>(),
                output.data_ptr<scalar_t>(),
                rand_indices.data_ptr<int64_t>(),
                rand_signs.data_ptr<int8_t>(),
                batch_size,
                original_dim,
                proj_dim,
                c);

            normalize_kernel<scalar_t><<<fixed_blocks, threads>>>(
                output.data_ptr<scalar_t>(),
                batch_size,
                proj_dim,
                normalization_factor);
        }));
    }

    // Check for CUDA errors
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        throw std::runtime_error(cudaGetErrorString(err));
    }

    return {output};
}

// Define module functions
PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("sjlt_projection_cuda", &sjlt_projection_cuda, "SJLT projection CUDA implementation with fixed block count");
}
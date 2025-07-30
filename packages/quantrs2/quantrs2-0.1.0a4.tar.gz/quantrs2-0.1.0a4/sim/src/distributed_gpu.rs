//! Distributed GPU state vector simulation across multiple devices.
//!
//! This module implements distributed quantum state vector simulation
//! leveraging SciRS2's GPU capabilities to scale computations across
//! multiple GPUs for large-scale quantum circuit simulation.

use ndarray::{s, Array1, Array2, ArrayView1, Axis};
use num_complex::Complex64;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use crate::error::{Result, SimulatorError};
use crate::scirs2_integration::SciRS2Backend;

#[cfg(feature = "advanced_math")]
use scirs2_core::gpu::{GpuBackend, GpuBuffer, GpuContext, GpuError};

/// Configuration for distributed GPU simulation
#[derive(Debug, Clone)]
pub struct DistributedGpuConfig {
    /// Number of GPUs to use (0 = auto-detect)
    pub num_gpus: usize,
    /// Minimum qubits required to enable GPU acceleration
    pub min_qubits_for_gpu: usize,
    /// Maximum state vector size per GPU (in complex numbers)
    pub max_state_size_per_gpu: usize,
    /// Enable automatic load balancing
    pub auto_load_balance: bool,
    /// Memory overlap for efficient transfers
    pub memory_overlap_ratio: f64,
    /// Use mixed precision for larger simulations
    pub use_mixed_precision: bool,
    /// Synchronization strategy
    pub sync_strategy: SyncStrategy,
}

impl Default for DistributedGpuConfig {
    fn default() -> Self {
        Self {
            num_gpus: 0, // Auto-detect
            min_qubits_for_gpu: 15,
            max_state_size_per_gpu: 1 << 26, // 64M complex numbers per GPU
            auto_load_balance: true,
            memory_overlap_ratio: 0.1,
            use_mixed_precision: false,
            sync_strategy: SyncStrategy::AllReduce,
        }
    }
}

/// GPU synchronization strategy
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SyncStrategy {
    /// All-reduce collective operations
    AllReduce,
    /// Ring-based reduction
    RingReduce,
    /// Tree-based reduction
    TreeReduce,
    /// Point-to-point communication
    PointToPoint,
}

/// Distributed GPU state vector
#[derive(Debug)]
pub struct DistributedGpuStateVector {
    /// GPU contexts for each device
    gpu_contexts: Vec<GpuContextWrapper>,
    /// State vector partitions on each GPU
    state_partitions: Vec<StatePartition>,
    /// Configuration
    config: DistributedGpuConfig,
    /// Total number of qubits
    num_qubits: usize,
    /// Current partition scheme
    partition_scheme: PartitionScheme,
    /// SciRS2 backend
    backend: Option<SciRS2Backend>,
    /// Performance statistics
    stats: DistributedGpuStats,
}

/// Wrapper for GPU context to handle feature flags
pub struct GpuContextWrapper {
    #[cfg(feature = "advanced_math")]
    context: GpuContext,
    device_id: usize,
    memory_available: usize,
    compute_capability: f64,
}

impl std::fmt::Debug for GpuContextWrapper {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GpuContextWrapper")
            .field("device_id", &self.device_id)
            .field("memory_available", &self.memory_available)
            .field("compute_capability", &self.compute_capability)
            .finish()
    }
}

/// State vector partition on a single GPU
pub struct StatePartition {
    /// GPU buffer containing the state amplitudes (placeholder)
    #[cfg(feature = "advanced_math")]
    buffer: Option<GpuBuffer<f64>>, // Placeholder - would need conversion from Complex64
    /// Local state vector for CPU fallback
    cpu_fallback: Array1<Complex64>,
    /// Start index in global state vector
    start_index: usize,
    /// Size of this partition
    size: usize,
    /// GPU device ID
    device_id: usize,
}

impl std::fmt::Debug for StatePartition {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("StatePartition")
            .field("start_index", &self.start_index)
            .field("size", &self.size)
            .field("device_id", &self.device_id)
            .finish()
    }
}

/// Partitioning scheme for distributing state vector
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PartitionScheme {
    /// Simple block partitioning
    Block,
    /// Interleaved partitioning for better load balance
    Interleaved,
    /// Adaptive partitioning based on computation patterns
    Adaptive,
    /// Hilbert curve space-filling partitioning
    HilbertCurve,
}

/// Performance statistics for distributed GPU simulation
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct DistributedGpuStats {
    /// Total execution time in milliseconds
    pub total_execution_time_ms: f64,
    /// GPU computation time per device
    pub gpu_computation_time_ms: Vec<f64>,
    /// Communication time between GPUs
    pub communication_time_ms: f64,
    /// Memory transfer time
    pub memory_transfer_time_ms: f64,
    /// Load balance efficiency (0-1)
    pub load_balance_efficiency: f64,
    /// GPU utilization per device (0-1)
    pub gpu_utilization: Vec<f64>,
    /// Memory usage per device in bytes
    pub memory_usage_bytes: Vec<usize>,
    /// Number of synchronization events
    pub sync_events: usize,
}

impl DistributedGpuStateVector {
    /// Create new distributed GPU state vector
    pub fn new(num_qubits: usize, config: DistributedGpuConfig) -> Result<Self> {
        if num_qubits < config.min_qubits_for_gpu {
            return Err(SimulatorError::InvalidInput(format!(
                "Distributed GPU simulation requires at least {} qubits",
                config.min_qubits_for_gpu
            )));
        }

        let state_size = 1_usize << num_qubits;

        // Initialize GPU contexts
        let gpu_contexts = Self::initialize_gpu_contexts(&config)?;
        let num_devices = gpu_contexts.len();

        if num_devices == 0 {
            return Err(SimulatorError::InitializationFailed(
                "No GPU devices available for distributed simulation".to_string(),
            ));
        }

        // Determine partitioning scheme
        let partition_scheme = Self::select_partition_scheme(num_qubits, num_devices, &config);

        // Create state partitions
        let state_partitions =
            Self::create_state_partitions(state_size, &gpu_contexts, &partition_scheme, &config)?;

        let stats = DistributedGpuStats {
            gpu_computation_time_ms: vec![0.0; num_devices],
            gpu_utilization: vec![0.0; num_devices],
            memory_usage_bytes: vec![0; num_devices],
            ..Default::default()
        };

        Ok(Self {
            gpu_contexts,
            state_partitions,
            config,
            num_qubits,
            partition_scheme,
            backend: None,
            stats,
        })
    }

    /// Initialize with SciRS2 backend
    pub fn with_backend(mut self) -> Result<Self> {
        self.backend = Some(SciRS2Backend::new());
        Ok(self)
    }

    /// Initialize |0...0⟩ state
    pub fn initialize_zero_state(&mut self) -> Result<()> {
        let start_time = std::time::Instant::now();

        for (i, partition) in self.state_partitions.iter_mut().enumerate() {
            if partition.start_index == 0 {
                // First partition contains the |0...0⟩ amplitude
                #[cfg(feature = "advanced_math")]
                {
                    // Would copy data to GPU buffer if available
                    // let mut host_data = vec![Complex64::new(0.0, 0.0); partition.size];
                    // host_data[0] = Complex64::new(1.0, 0.0);
                    // if let Some(ref mut buffer) = partition.buffer {
                    //     buffer.copy_from_host(&host_data);
                    // }
                }

                partition.cpu_fallback.fill(Complex64::new(0.0, 0.0));
                partition.cpu_fallback[0] = Complex64::new(1.0, 0.0);
            } else {
                // Other partitions are zero
                #[cfg(feature = "advanced_math")]
                {
                    // Would copy zero data to GPU buffer if available
                    // let host_data = vec![Complex64::new(0.0, 0.0); partition.size];
                    // if let Some(ref mut buffer) = partition.buffer {
                    //     buffer.copy_from_host(&host_data);
                    // }
                }

                partition.cpu_fallback.fill(Complex64::new(0.0, 0.0));
            }
        }

        self.stats.memory_transfer_time_ms += start_time.elapsed().as_secs_f64() * 1000.0;
        Ok(())
    }

    /// Apply single-qubit gate distributed across GPUs
    pub fn apply_single_qubit_gate(
        &mut self,
        qubit: usize,
        gate_matrix: &Array2<Complex64>,
    ) -> Result<()> {
        if qubit >= self.num_qubits {
            return Err(SimulatorError::IndexOutOfBounds(qubit));
        }

        let start_time = std::time::Instant::now();

        // Apply gate to each partition sequentially to avoid borrowing issues
        let mut device_times = Vec::new();
        for i in 0..self.state_partitions.len() {
            let device_start_time = std::time::Instant::now();

            // Extract device_id before borrowing
            let device_id = self.state_partitions[i].device_id;
            Self::apply_single_qubit_gate_partition_static(
                qubit,
                gate_matrix,
                &mut self.state_partitions[i],
                device_id,
            )?;

            let device_time = device_start_time.elapsed().as_secs_f64() * 1000.0;
            device_times.push(device_time);
        }

        for (i, time) in device_times.into_iter().enumerate() {
            self.stats.gpu_computation_time_ms[i] += time;
        }

        self.stats.total_execution_time_ms += start_time.elapsed().as_secs_f64() * 1000.0;
        Ok(())
    }

    /// Apply two-qubit gate with inter-GPU communication if needed
    pub fn apply_two_qubit_gate(
        &mut self,
        control: usize,
        target: usize,
        gate_matrix: &Array2<Complex64>,
    ) -> Result<()> {
        if control >= self.num_qubits || target >= self.num_qubits {
            return Err(SimulatorError::IndexOutOfBounds(control.max(target)));
        }

        let start_time = std::time::Instant::now();

        // Check if gate requires inter-GPU communication
        let requires_communication = self.requires_inter_gpu_communication(control, target);

        if requires_communication {
            self.apply_two_qubit_gate_distributed(control, target, gate_matrix)?;
        } else {
            // Gate can be applied locally on each GPU
            let mut device_times = Vec::new();
            for i in 0..self.state_partitions.len() {
                let device_start_time = std::time::Instant::now();

                let device_id = self.state_partitions[i].device_id;
                Self::apply_two_qubit_gate_partition_static(
                    control,
                    target,
                    gate_matrix,
                    &mut self.state_partitions[i],
                    device_id,
                )?;

                let device_time = device_start_time.elapsed().as_secs_f64() * 1000.0;
                device_times.push(device_time);
            }
            for (i, time) in device_times.into_iter().enumerate() {
                self.stats.gpu_computation_time_ms[i] += time;
            }
        }

        self.stats.total_execution_time_ms += start_time.elapsed().as_secs_f64() * 1000.0;
        Ok(())
    }

    /// Calculate probability of measuring qubit in |1⟩ state
    pub fn measure_probability(&mut self, qubit: usize) -> Result<f64> {
        if qubit >= self.num_qubits {
            return Err(SimulatorError::IndexOutOfBounds(qubit));
        }

        let start_time = std::time::Instant::now();

        // Calculate local probabilities on each GPU
        let local_probs: Result<Vec<f64>> = self
            .state_partitions
            .par_iter()
            .enumerate()
            .map(|(device_id, partition)| {
                self.calculate_local_probability(qubit, partition, device_id)
            })
            .collect();

        let local_probs = local_probs?;

        // Sum probabilities across all GPUs
        let total_prob = local_probs.iter().sum();

        self.stats.total_execution_time_ms += start_time.elapsed().as_secs_f64() * 1000.0;
        Ok(total_prob)
    }

    /// Get state vector (expensive operation - copies from all GPUs)
    pub fn get_state_vector(&mut self) -> Result<Array1<Complex64>> {
        let start_time = std::time::Instant::now();

        let state_size = 1 << self.num_qubits;
        let mut state_vector = Array1::zeros(state_size);

        // Copy data from each GPU partition
        for partition in &self.state_partitions {
            let end_index = (partition.start_index + partition.size).min(state_size);

            #[cfg(feature = "advanced_math")]
            {
                // Would copy data from GPU buffer if available
                // let mut host_data = vec![Complex64::new(0.0, 0.0); partition.size];
                // if let Some(ref buffer) = partition.buffer {
                //     buffer.copy_to_host(&mut host_data);
                //     state_vector.slice_mut(s![partition.start_index..end_index])
                //         .assign(&Array1::from_vec(host_data[..end_index - partition.start_index].to_vec()));
                // }
            }

            #[cfg(not(feature = "advanced_math"))]
            {
                state_vector
                    .slice_mut(s![partition.start_index..end_index])
                    .assign(
                        &partition
                            .cpu_fallback
                            .slice(s![..end_index - partition.start_index]),
                    );
            }
        }

        self.stats.memory_transfer_time_ms += start_time.elapsed().as_secs_f64() * 1000.0;
        Ok(state_vector)
    }

    /// Get performance statistics
    pub fn get_stats(&self) -> &DistributedGpuStats {
        &self.stats
    }

    /// Internal helper methods

    #[cfg(feature = "advanced_math")]
    fn initialize_gpu_contexts(config: &DistributedGpuConfig) -> Result<Vec<GpuContextWrapper>> {
        let mut contexts = Vec::new();

        let num_gpus = if config.num_gpus == 0 {
            // Auto-detect available GPUs
            Self::detect_available_gpus()?
        } else {
            config.num_gpus
        };

        for device_id in 0..num_gpus {
            match Self::create_gpu_context(device_id) {
                Ok(wrapper) => contexts.push(wrapper),
                Err(e) => {
                    eprintln!("Warning: Failed to initialize GPU {}: {}", device_id, e);
                }
            }
        }

        if contexts.is_empty() {
            return Err(SimulatorError::InitializationFailed(
                "No GPU contexts could be created".to_string(),
            ));
        }

        Ok(contexts)
    }

    #[cfg(not(feature = "advanced_math"))]
    fn initialize_gpu_contexts(_config: &DistributedGpuConfig) -> Result<Vec<GpuContextWrapper>> {
        // Fallback: create dummy contexts for CPU simulation
        Ok(vec![GpuContextWrapper {
            device_id: 0,
            memory_available: 1_000_000_000, // 1GB
            compute_capability: 1.0,
        }])
    }

    #[cfg(feature = "advanced_math")]
    fn create_gpu_context(device_id: usize) -> Result<GpuContextWrapper> {
        let context = GpuContext::new(GpuBackend::preferred()).map_err(|e| {
            SimulatorError::InitializationFailed(format!("GPU context creation failed: {}", e))
        })?;

        // Query device properties
        let memory_available = Self::query_gpu_memory(&context)?;
        let compute_capability = Self::query_compute_capability(&context)?;

        Ok(GpuContextWrapper {
            context,
            device_id,
            memory_available,
            compute_capability,
        })
    }

    #[cfg(feature = "advanced_math")]
    fn query_gpu_memory(context: &GpuContext) -> Result<usize> {
        // This would query actual GPU memory in a real implementation
        Ok(8_000_000_000) // 8GB default
    }

    #[cfg(feature = "advanced_math")]
    fn query_compute_capability(context: &GpuContext) -> Result<f64> {
        // This would query actual compute capability in a real implementation
        Ok(7.5) // Default capability
    }

    #[cfg(feature = "advanced_math")]
    fn detect_available_gpus() -> Result<usize> {
        // This would detect actual GPU count in a real implementation
        Ok(1) // Default to 1 GPU
    }

    fn select_partition_scheme(
        num_qubits: usize,
        num_devices: usize,
        config: &DistributedGpuConfig,
    ) -> PartitionScheme {
        if config.auto_load_balance {
            if num_qubits > 25 {
                PartitionScheme::Adaptive
            } else if num_devices > 4 {
                PartitionScheme::Interleaved
            } else {
                PartitionScheme::Block
            }
        } else {
            PartitionScheme::Block
        }
    }

    fn create_state_partitions(
        state_size: usize,
        gpu_contexts: &[GpuContextWrapper],
        partition_scheme: &PartitionScheme,
        config: &DistributedGpuConfig,
    ) -> Result<Vec<StatePartition>> {
        let num_devices = gpu_contexts.len();
        let mut partitions = Vec::new();

        match partition_scheme {
            PartitionScheme::Block => {
                let partition_size = (state_size + num_devices - 1) / num_devices;

                for (i, context) in gpu_contexts.iter().enumerate() {
                    let start_index = i * partition_size;
                    let end_index = ((i + 1) * partition_size).min(state_size);
                    let size = end_index - start_index;

                    if size > 0 {
                        let partition = Self::create_single_partition(
                            start_index,
                            size,
                            context.device_id,
                            config,
                        )?;
                        partitions.push(partition);
                    }
                }
            }
            PartitionScheme::Interleaved => {
                // Interleaved partitioning for better load balance
                let base_size = state_size / num_devices;
                let remainder = state_size % num_devices;

                let mut start_index = 0;
                for (i, context) in gpu_contexts.iter().enumerate() {
                    let size = base_size + if i < remainder { 1 } else { 0 };

                    if size > 0 {
                        let partition = Self::create_single_partition(
                            start_index,
                            size,
                            context.device_id,
                            config,
                        )?;
                        partitions.push(partition);
                        start_index += size;
                    }
                }
            }
            PartitionScheme::Adaptive => {
                // Adaptive partitioning based on GPU capabilities
                let total_memory: usize = gpu_contexts.iter().map(|ctx| ctx.memory_available).sum();

                let mut start_index = 0;
                for context in gpu_contexts {
                    let memory_fraction = context.memory_available as f64 / total_memory as f64;
                    let size = (state_size as f64 * memory_fraction) as usize;

                    if size > 0 && start_index < state_size {
                        let actual_size = size.min(state_size - start_index);
                        let partition = Self::create_single_partition(
                            start_index,
                            actual_size,
                            context.device_id,
                            config,
                        )?;
                        partitions.push(partition);
                        start_index += actual_size;
                    }
                }
            }
            PartitionScheme::HilbertCurve => {
                // Hilbert curve partitioning (simplified implementation)
                return Self::create_hilbert_partitions(state_size, gpu_contexts, config);
            }
        }

        if partitions.is_empty() {
            return Err(SimulatorError::InitializationFailed(
                "No valid partitions could be created".to_string(),
            ));
        }

        Ok(partitions)
    }

    fn create_single_partition(
        start_index: usize,
        size: usize,
        device_id: usize,
        _config: &DistributedGpuConfig,
    ) -> Result<StatePartition> {
        #[cfg(feature = "advanced_math")]
        let buffer = {
            // In a real implementation, this would create the GPU buffer on the specific device
            unimplemented!("GPU buffer creation not implemented in example")
        };

        let cpu_fallback = Array1::zeros(size);

        Ok(StatePartition {
            #[cfg(feature = "advanced_math")]
            buffer,
            cpu_fallback,
            start_index,
            size,
            device_id,
        })
    }

    fn create_hilbert_partitions(
        _state_size: usize,
        _gpu_contexts: &[GpuContextWrapper],
        _config: &DistributedGpuConfig,
    ) -> Result<Vec<StatePartition>> {
        // Placeholder for Hilbert curve partitioning
        Err(SimulatorError::UnsupportedOperation(
            "Hilbert curve partitioning not yet implemented".to_string(),
        ))
    }

    fn apply_single_qubit_gate_partition(
        &self,
        qubit: usize,
        gate_matrix: &Array2<Complex64>,
        partition: &mut StatePartition,
        device_id: usize,
    ) -> Result<()> {
        #[cfg(feature = "advanced_math")]
        {
            // Use SciRS2 GPU kernels for gate application
            if let Some(ref backend) = self.backend {
                self.apply_single_qubit_gate_gpu(qubit, gate_matrix, partition, device_id)
            } else {
                self.apply_single_qubit_gate_cpu_fallback(qubit, gate_matrix, partition)
            }
        }

        #[cfg(not(feature = "advanced_math"))]
        self.apply_single_qubit_gate_cpu_fallback(qubit, gate_matrix, partition)
    }

    #[cfg(feature = "advanced_math")]
    fn apply_single_qubit_gate_gpu(
        &self,
        qubit: usize,
        gate_matrix: &Array2<Complex64>,
        partition: &mut StatePartition,
        _device_id: usize,
    ) -> Result<()> {
        // This would use SciRS2's GPU kernels for quantum gate application
        // For now, fall back to CPU implementation
        self.apply_single_qubit_gate_cpu_fallback(qubit, gate_matrix, partition)
    }

    fn apply_single_qubit_gate_cpu_fallback(
        &self,
        qubit: usize,
        gate_matrix: &Array2<Complex64>,
        partition: &mut StatePartition,
    ) -> Result<()> {
        let qubit_mask = 1_usize << qubit;
        let state_size = partition.size;

        // Apply gate to CPU fallback state
        let mut new_state = partition.cpu_fallback.clone();

        for i in 0..state_size {
            let global_i = partition.start_index + i;

            if global_i & qubit_mask == 0 {
                // |0⟩ component
                let j = global_i | qubit_mask; // Corresponding |1⟩ state

                if j >= partition.start_index && j < partition.start_index + partition.size {
                    // Both states are in this partition
                    let local_j = j - partition.start_index;

                    let amp_0 = partition.cpu_fallback[i];
                    let amp_1 = partition.cpu_fallback[local_j];

                    new_state[i] = gate_matrix[[0, 0]] * amp_0 + gate_matrix[[0, 1]] * amp_1;
                    new_state[local_j] = gate_matrix[[1, 0]] * amp_0 + gate_matrix[[1, 1]] * amp_1;
                }
            }
        }

        partition.cpu_fallback = new_state;

        // Copy to GPU buffer if available
        #[cfg(feature = "advanced_math")]
        {
            // Would convert Complex64 to GPU-compatible format and copy
            // For now, just use CPU fallback since Complex64 doesn't implement GpuDataType
            // let host_data: Vec<Complex64> = partition.cpu_fallback.to_vec();
            // partition.buffer.copy_from_host(&host_data);
        }

        Ok(())
    }

    fn apply_two_qubit_gate_partition(
        &self,
        control: usize,
        target: usize,
        gate_matrix: &Array2<Complex64>,
        partition: &mut StatePartition,
        _device_id: usize,
    ) -> Result<()> {
        // Simplified two-qubit gate implementation
        // In practice, this would be much more optimized
        let control_mask = 1_usize << control;
        let target_mask = 1_usize << target;

        let mut new_state = partition.cpu_fallback.clone();

        for i in 0..partition.size {
            let global_i = partition.start_index + i;

            // Only apply gate if control qubit is |1⟩
            if global_i & control_mask != 0 {
                let target_bit = (global_i & target_mask) != 0;
                let j = if target_bit {
                    global_i & !target_mask
                } else {
                    global_i | target_mask
                };

                if j >= partition.start_index && j < partition.start_index + partition.size {
                    let local_j = j - partition.start_index;

                    let amp_i = partition.cpu_fallback[i];
                    let amp_j = partition.cpu_fallback[local_j];

                    if target_bit {
                        // i has target=1, j has target=0
                        new_state[local_j] =
                            gate_matrix[[0, 0]] * amp_j + gate_matrix[[0, 1]] * amp_i;
                        new_state[i] = gate_matrix[[1, 0]] * amp_j + gate_matrix[[1, 1]] * amp_i;
                    } else {
                        // i has target=0, j has target=1
                        new_state[i] = gate_matrix[[0, 0]] * amp_i + gate_matrix[[0, 1]] * amp_j;
                        new_state[local_j] =
                            gate_matrix[[1, 0]] * amp_i + gate_matrix[[1, 1]] * amp_j;
                    }
                }
            }
        }

        partition.cpu_fallback = new_state;

        // Copy to GPU buffer if available
        #[cfg(feature = "advanced_math")]
        {
            // Would convert Complex64 to GPU-compatible format and copy
            // For now, just use CPU fallback since Complex64 doesn't implement GpuDataType
            // let host_data: Vec<Complex64> = partition.cpu_fallback.to_vec();
            // partition.buffer.copy_from_host(&host_data);
        }

        Ok(())
    }

    fn apply_two_qubit_gate_distributed(
        &mut self,
        control: usize,
        target: usize,
        gate_matrix: &Array2<Complex64>,
    ) -> Result<()> {
        let comm_start_time = std::time::Instant::now();

        // This would implement sophisticated inter-GPU communication
        // For now, we'll use a simplified approach with CPU intermediary

        // 1. Collect all relevant state amplitudes
        // 2. Apply gate on CPU
        // 3. Redistribute updated amplitudes

        // Simplified implementation - in practice this would be much more optimized
        self.synchronize_all_reduce()?;

        // Apply gate locally on each partition
        for i in 0..self.state_partitions.len() {
            let device_id = self.state_partitions[i].device_id;
            Self::apply_two_qubit_gate_partition_static(
                control,
                target,
                gate_matrix,
                &mut self.state_partitions[i],
                device_id,
            )?;
        }

        self.stats.communication_time_ms += comm_start_time.elapsed().as_secs_f64() * 1000.0;
        self.stats.sync_events += 1;

        Ok(())
    }

    fn requires_inter_gpu_communication(&self, control: usize, target: usize) -> bool {
        // Check if the gate affects amplitudes that span multiple GPUs
        // This is a simplified heuristic
        match self.partition_scheme {
            PartitionScheme::Block => {
                // For block partitioning, inter-GPU communication is needed
                // if the gate affects states that cross partition boundaries
                let control_mask = 1_usize << control;
                let target_mask = 1_usize << target;

                // Check if any partition boundary falls between affected states
                for partition in &self.state_partitions {
                    let start = partition.start_index;
                    let end = partition.start_index + partition.size;

                    // Check if there are states with different control/target combinations
                    // that span across this partition boundary
                    for i in start..end.min(start + 1000) {
                        // Sample check
                        let pair_state = i ^ target_mask;
                        if (i & control_mask) != 0 && (pair_state < start || pair_state >= end) {
                            return true;
                        }
                    }
                }

                false
            }
            _ => true, // Conservative approach for other partitioning schemes
        }
    }

    fn calculate_local_probability(
        &self,
        qubit: usize,
        partition: &StatePartition,
        _device_id: usize,
    ) -> Result<f64> {
        let qubit_mask = 1_usize << qubit;
        let mut probability = 0.0;

        for i in 0..partition.size {
            let global_i = partition.start_index + i;
            if global_i & qubit_mask != 0 {
                probability += partition.cpu_fallback[i].norm_sqr();
            }
        }

        Ok(probability)
    }

    fn synchronize_all_reduce(&mut self) -> Result<()> {
        match self.config.sync_strategy {
            SyncStrategy::AllReduce => self.all_reduce_sync(),
            SyncStrategy::RingReduce => self.ring_reduce_sync(),
            SyncStrategy::TreeReduce => self.tree_reduce_sync(),
            SyncStrategy::PointToPoint => self.point_to_point_sync(),
        }
    }

    fn all_reduce_sync(&mut self) -> Result<()> {
        // Simplified all-reduce implementation
        // In practice, this would use efficient collective communication
        Ok(())
    }

    fn ring_reduce_sync(&mut self) -> Result<()> {
        // Ring-based reduction for better bandwidth utilization
        Ok(())
    }

    fn tree_reduce_sync(&mut self) -> Result<()> {
        // Tree-based reduction for lower latency
        Ok(())
    }

    fn point_to_point_sync(&mut self) -> Result<()> {
        // Direct point-to-point communication
        Ok(())
    }

    // Static methods to avoid borrowing issues
    fn apply_single_qubit_gate_partition_static(
        qubit: usize,
        gate_matrix: &Array2<Complex64>,
        partition: &mut StatePartition,
        device_id: usize,
    ) -> Result<()> {
        // Simplified single-qubit gate application
        let qubit_mask = 1_usize << qubit;

        for i in (0..partition.cpu_fallback.len()).step_by(2) {
            if i & qubit_mask == 0 {
                let j = i | qubit_mask;
                if j < partition.cpu_fallback.len() {
                    let amp_0 = partition.cpu_fallback[i];
                    let amp_1 = partition.cpu_fallback[j];

                    partition.cpu_fallback[i] =
                        gate_matrix[[0, 0]] * amp_0 + gate_matrix[[0, 1]] * amp_1;
                    partition.cpu_fallback[j] =
                        gate_matrix[[1, 0]] * amp_0 + gate_matrix[[1, 1]] * amp_1;
                }
            }
        }

        Ok(())
    }

    fn apply_two_qubit_gate_partition_static(
        control: usize,
        target: usize,
        gate_matrix: &Array2<Complex64>,
        partition: &mut StatePartition,
        device_id: usize,
    ) -> Result<()> {
        // Simplified two-qubit gate application
        let control_mask = 1_usize << control;
        let target_mask = 1_usize << target;

        for i in 0..partition.cpu_fallback.len() {
            if i & control_mask != 0 {
                let target_bit = (i & target_mask) != 0;
                let j = if target_bit {
                    i & !target_mask
                } else {
                    i | target_mask
                };

                if j < i || j >= partition.cpu_fallback.len() {
                    continue;
                }

                let amp_i = partition.cpu_fallback[i];
                let amp_j = partition.cpu_fallback[j];

                if target_bit {
                    partition.cpu_fallback[j] =
                        gate_matrix[[0, 0]] * amp_j + gate_matrix[[0, 1]] * amp_i;
                    partition.cpu_fallback[i] =
                        gate_matrix[[1, 0]] * amp_j + gate_matrix[[1, 1]] * amp_i;
                } else {
                    partition.cpu_fallback[i] =
                        gate_matrix[[0, 0]] * amp_i + gate_matrix[[0, 1]] * amp_j;
                    partition.cpu_fallback[j] =
                        gate_matrix[[1, 0]] * amp_i + gate_matrix[[1, 1]] * amp_j;
                }
            }
        }

        Ok(())
    }
}

/// Utilities for distributed GPU simulation
pub struct DistributedGpuUtils;

impl DistributedGpuUtils {
    /// Estimate memory requirements for distributed simulation
    pub fn estimate_memory_requirements(num_qubits: usize, num_gpus: usize) -> usize {
        let state_size = 1_usize << num_qubits;
        let complex_size = std::mem::size_of::<Complex64>();
        let total_memory = state_size * complex_size;

        // Add overhead for buffers, intermediate computations, etc.
        let overhead_factor = 1.5;
        (total_memory as f64 * overhead_factor) as usize / num_gpus
    }

    /// Calculate optimal number of GPUs for given problem size
    pub fn optimal_gpu_count(
        num_qubits: usize,
        available_gpus: usize,
        memory_per_gpu: usize,
    ) -> usize {
        let total_memory_needed = Self::estimate_memory_requirements(num_qubits, 1);
        let min_gpus_needed = (total_memory_needed + memory_per_gpu - 1) / memory_per_gpu;

        min_gpus_needed.min(available_gpus).max(1)
    }

    /// Benchmark different partitioning strategies
    pub fn benchmark_partitioning_strategies(
        num_qubits: usize,
        num_gpus: usize,
    ) -> Result<HashMap<String, f64>> {
        let mut results = HashMap::new();

        let strategies = vec![
            ("Block", PartitionScheme::Block),
            ("Interleaved", PartitionScheme::Interleaved),
            ("Adaptive", PartitionScheme::Adaptive),
        ];

        for (name, scheme) in strategies {
            let config = DistributedGpuConfig {
                num_gpus,
                ..Default::default()
            };

            let start_time = std::time::Instant::now();

            // Create simulator with this partitioning scheme
            let mut simulator = DistributedGpuStateVector::new(num_qubits, config)?;
            simulator.initialize_zero_state()?;

            // Perform some operations to benchmark
            let identity = Array2::eye(2);
            for i in 0..num_qubits.min(5) {
                simulator.apply_single_qubit_gate(i, &identity)?;
            }

            let execution_time = start_time.elapsed().as_secs_f64();
            results.insert(name.to_string(), execution_time);
        }

        Ok(results)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use approx::assert_abs_diff_eq;

    #[test]
    fn test_distributed_gpu_config_default() {
        let config = DistributedGpuConfig::default();
        assert_eq!(config.num_gpus, 0);
        assert_eq!(config.min_qubits_for_gpu, 15);
        assert_eq!(config.sync_strategy, SyncStrategy::AllReduce);
    }

    #[test]
    fn test_partition_scheme_selection() {
        let config = DistributedGpuConfig::default();

        // Small system should use Block partitioning
        let scheme = DistributedGpuStateVector::select_partition_scheme(20, 2, &config);
        assert_eq!(scheme, PartitionScheme::Block);

        // Large system should use Adaptive partitioning
        let scheme = DistributedGpuStateVector::select_partition_scheme(30, 2, &config);
        assert_eq!(scheme, PartitionScheme::Adaptive);
    }

    #[test]
    fn test_memory_estimation() {
        let memory_1gpu = DistributedGpuUtils::estimate_memory_requirements(20, 1);
        let memory_4gpu = DistributedGpuUtils::estimate_memory_requirements(20, 4);

        // Memory per GPU should be roughly 1/4 when using 4 GPUs
        assert!(memory_4gpu < memory_1gpu / 2);
    }

    #[test]
    fn test_optimal_gpu_count() {
        let memory_per_gpu = 8_000_000_000; // 8GB

        let optimal = DistributedGpuUtils::optimal_gpu_count(25, 8, memory_per_gpu);
        assert!(optimal >= 1);
        assert!(optimal <= 8);
    }

    #[test]
    fn test_distributed_simulation_small() {
        let config = DistributedGpuConfig {
            min_qubits_for_gpu: 5, // Lower threshold for testing
            num_gpus: 1,
            ..Default::default()
        };

        let mut simulator = DistributedGpuStateVector::new(5, config).unwrap();
        simulator.initialize_zero_state().unwrap();

        // Apply Pauli-X gate to first qubit
        let pauli_x = Array2::from_shape_vec(
            (2, 2),
            vec![
                Complex64::new(0.0, 0.0),
                Complex64::new(1.0, 0.0),
                Complex64::new(1.0, 0.0),
                Complex64::new(0.0, 0.0),
            ],
        )
        .unwrap();

        simulator.apply_single_qubit_gate(0, &pauli_x).unwrap();

        // Measure probability - should be 1.0 for |1⟩ on first qubit
        let prob = simulator.measure_probability(0).unwrap();
        assert_abs_diff_eq!(prob, 1.0, epsilon = 1e-10);
    }
}

//! Dynamical decoupling sequence generation and management

use std::collections::HashMap;
use std::f64::consts::PI;

use quantrs2_circuit::prelude::*;
use quantrs2_core::{
    gate::{
        single::{Hadamard, PauliX, PauliY, PauliZ},
        GateOp,
    },
    qubit::QubitId,
};

use super::config::{DDSequenceType, NoiseType};
use crate::DeviceResult;

/// Dynamical decoupling sequence representation
#[derive(Debug, Clone)]
pub struct DDSequence {
    /// Sequence type
    pub sequence_type: DDSequenceType,
    /// Target qubits
    pub target_qubits: Vec<QubitId>,
    /// Sequence duration
    pub duration: f64,
    /// Circuit implementation
    pub circuit: Circuit<32>,
    /// Pulse timings
    pub pulse_timings: Vec<f64>,
    /// Pulse phases
    pub pulse_phases: Vec<f64>,
    /// Sequence properties
    pub properties: DDSequenceProperties,
}

/// Properties of a DD sequence
#[derive(Debug, Clone)]
pub struct DDSequenceProperties {
    /// Number of pulses
    pub pulse_count: usize,
    /// Sequence order (cancellation order)
    pub sequence_order: usize,
    /// Periodicity
    pub periodicity: usize,
    /// Symmetry properties
    pub symmetry: SequenceSymmetry,
    /// Noise suppression characteristics
    pub noise_suppression: HashMap<NoiseType, f64>,
    /// Resource requirements
    pub resource_requirements: ResourceRequirements,
}

/// Sequence symmetry properties
#[derive(Debug, Clone)]
pub struct SequenceSymmetry {
    /// Time-reversal symmetry
    pub time_reversal: bool,
    /// Phase symmetry
    pub phase_symmetry: bool,
    /// Rotational symmetry
    pub rotational_symmetry: bool,
    /// Inversion symmetry
    pub inversion_symmetry: bool,
}

/// Resource requirements for a DD sequence
#[derive(Debug, Clone)]
pub struct ResourceRequirements {
    /// Gate count
    pub gate_count: usize,
    /// Circuit depth
    pub circuit_depth: usize,
    /// Required connectivity
    pub required_connectivity: Vec<(QubitId, QubitId)>,
    /// Estimated execution time
    pub execution_time: f64,
    /// Memory requirements
    pub memory_requirements: usize,
}

/// DD sequence generator
pub struct DDSequenceGenerator;

impl DDSequenceGenerator {
    /// Generate a base DD sequence
    pub fn generate_base_sequence(
        sequence_type: &DDSequenceType,
        target_qubits: &[QubitId],
        duration: f64,
    ) -> DeviceResult<DDSequence> {
        match sequence_type {
            DDSequenceType::CPMG => Self::generate_cpmg_sequence(target_qubits, duration),
            DDSequenceType::XY4 => Self::generate_xy4_sequence(target_qubits, duration),
            DDSequenceType::XY8 => Self::generate_xy8_sequence(target_qubits, duration),
            DDSequenceType::XY16 => Self::generate_xy16_sequence(target_qubits, duration),
            DDSequenceType::UDD => Self::generate_udd_sequence(target_qubits, duration),
            DDSequenceType::KDD => Self::generate_kdd_sequence(target_qubits, duration),
            DDSequenceType::QDD => Self::generate_qdd_sequence(target_qubits, duration),
            DDSequenceType::CDD => Self::generate_cdd_sequence(target_qubits, duration),
            DDSequenceType::RDD => Self::generate_rdd_sequence(target_qubits, duration),
            DDSequenceType::CarrPurcell => Self::generate_cp_sequence(target_qubits, duration),
            DDSequenceType::SciRS2Optimized => {
                Self::generate_optimized_sequence(target_qubits, duration)
            }
            DDSequenceType::Custom(name) => {
                Self::generate_custom_sequence(name, target_qubits, duration)
            }
        }
    }

    /// Generate CPMG (Carr-Purcell-Meiboom-Gill) sequence
    fn generate_cpmg_sequence(
        target_qubits: &[QubitId],
        duration: f64,
    ) -> DeviceResult<DDSequence> {
        let n_pulses = 16; // Default number of π pulses
        let pulse_spacing = duration / (n_pulses + 1) as f64;

        let mut circuit = Circuit::<32>::new();
        let mut pulse_timings = Vec::new();
        let mut pulse_phases = Vec::new();

        for qubit in target_qubits {
            for i in 1..=n_pulses {
                let timing = i as f64 * pulse_spacing;
                pulse_timings.push(timing);
                pulse_phases.push(PI); // Y rotation (π pulse)

                circuit.add_gate(PauliY { target: *qubit })?;
            }
        }

        let properties = DDSequenceProperties {
            pulse_count: n_pulses * target_qubits.len(),
            sequence_order: 1,
            periodicity: n_pulses,
            symmetry: SequenceSymmetry {
                time_reversal: true,
                phase_symmetry: true,
                rotational_symmetry: false,
                inversion_symmetry: true,
            },
            noise_suppression: {
                let mut suppression = HashMap::new();
                suppression.insert(NoiseType::PhaseDamping, 0.9);
                suppression.insert(NoiseType::AmplitudeDamping, 0.3);
                suppression
            },
            resource_requirements: ResourceRequirements {
                gate_count: n_pulses * target_qubits.len(),
                circuit_depth: n_pulses,
                required_connectivity: Vec::new(),
                execution_time: duration,
                memory_requirements: n_pulses * target_qubits.len() * 8,
            },
        };

        Ok(DDSequence {
            sequence_type: DDSequenceType::CPMG,
            target_qubits: target_qubits.to_vec(),
            duration,
            circuit,
            pulse_timings,
            pulse_phases,
            properties,
        })
    }

    /// Generate XY-4 sequence
    fn generate_xy4_sequence(target_qubits: &[QubitId], duration: f64) -> DeviceResult<DDSequence> {
        let base_sequence = vec![PI, PI / 2.0, PI, 3.0 * PI / 2.0]; // X, Y, X, -Y rotations
        let n_repetitions = 4;
        let pulse_spacing = duration / (base_sequence.len() * n_repetitions) as f64;

        let mut circuit = Circuit::<32>::new();
        let mut pulse_timings = Vec::new();
        let mut pulse_phases = Vec::new();

        for qubit in target_qubits {
            for rep in 0..n_repetitions {
                for (i, &phase) in base_sequence.iter().enumerate() {
                    let timing = (rep * base_sequence.len() + i + 1) as f64 * pulse_spacing;
                    pulse_timings.push(timing);
                    pulse_phases.push(phase);

                    match phase {
                        p if (p - PI).abs() < 1e-6 => {
                            circuit.add_gate(PauliX { target: *qubit })?;
                        }
                        p if (p - PI / 2.0).abs() < 1e-6 => {
                            circuit.add_gate(PauliY { target: *qubit })?;
                        }
                        p if (p - 3.0 * PI / 2.0).abs() < 1e-6 => {
                            circuit.add_gate(PauliY { target: *qubit })?;
                            circuit.add_gate(PauliZ { target: *qubit })?;
                            circuit.add_gate(PauliZ { target: *qubit })?;
                        }
                        _ => {
                            circuit.add_gate(PauliX { target: *qubit })?;
                        }
                    }
                }
            }
        }

        let properties = DDSequenceProperties {
            pulse_count: base_sequence.len() * n_repetitions * target_qubits.len(),
            sequence_order: 2,
            periodicity: base_sequence.len(),
            symmetry: SequenceSymmetry {
                time_reversal: true,
                phase_symmetry: true,
                rotational_symmetry: true,
                inversion_symmetry: true,
            },
            noise_suppression: {
                let mut suppression = HashMap::new();
                suppression.insert(NoiseType::PhaseDamping, 0.95);
                suppression.insert(NoiseType::AmplitudeDamping, 0.4);
                suppression.insert(NoiseType::Depolarizing, 0.8);
                suppression
            },
            resource_requirements: ResourceRequirements {
                gate_count: base_sequence.len() * n_repetitions * target_qubits.len(),
                circuit_depth: base_sequence.len() * n_repetitions,
                required_connectivity: Vec::new(),
                execution_time: duration,
                memory_requirements: base_sequence.len() * n_repetitions * target_qubits.len() * 8,
            },
        };

        Ok(DDSequence {
            sequence_type: DDSequenceType::XY4,
            target_qubits: target_qubits.to_vec(),
            duration,
            circuit,
            pulse_timings,
            pulse_phases,
            properties,
        })
    }

    /// Generate XY-8 sequence
    fn generate_xy8_sequence(target_qubits: &[QubitId], duration: f64) -> DeviceResult<DDSequence> {
        let base_sequence = vec![
            PI,
            PI / 2.0,
            PI,
            3.0 * PI / 2.0, // XY4
            3.0 * PI / 2.0,
            PI,
            PI / 2.0,
            PI, // -Y X Y X
        ];
        let n_repetitions = 2;
        let pulse_spacing = duration / (base_sequence.len() * n_repetitions) as f64;

        let mut circuit = Circuit::<32>::new();
        let mut pulse_timings = Vec::new();
        let mut pulse_phases = Vec::new();

        for qubit in target_qubits {
            for rep in 0..n_repetitions {
                for (i, &phase) in base_sequence.iter().enumerate() {
                    let timing = (rep * base_sequence.len() + i + 1) as f64 * pulse_spacing;
                    pulse_timings.push(timing);
                    pulse_phases.push(phase);

                    match phase {
                        p if (p - PI).abs() < 1e-6 => {
                            circuit.add_gate(PauliX { target: *qubit })?;
                        }
                        p if (p - PI / 2.0).abs() < 1e-6 => {
                            circuit.add_gate(PauliY { target: *qubit })?;
                        }
                        p if (p - 3.0 * PI / 2.0).abs() < 1e-6 => {
                            circuit.add_gate(PauliY { target: *qubit })?;
                            circuit.add_gate(PauliZ { target: *qubit })?;
                            circuit.add_gate(PauliZ { target: *qubit })?;
                        }
                        _ => {
                            circuit.add_gate(PauliX { target: *qubit })?;
                        }
                    }
                }
            }
        }

        let properties = DDSequenceProperties {
            pulse_count: base_sequence.len() * n_repetitions * target_qubits.len(),
            sequence_order: 3,
            periodicity: base_sequence.len(),
            symmetry: SequenceSymmetry {
                time_reversal: true,
                phase_symmetry: true,
                rotational_symmetry: true,
                inversion_symmetry: true,
            },
            noise_suppression: {
                let mut suppression = HashMap::new();
                suppression.insert(NoiseType::PhaseDamping, 0.98);
                suppression.insert(NoiseType::AmplitudeDamping, 0.5);
                suppression.insert(NoiseType::Depolarizing, 0.9);
                suppression.insert(NoiseType::CoherentErrors, 0.85);
                suppression
            },
            resource_requirements: ResourceRequirements {
                gate_count: base_sequence.len() * n_repetitions * target_qubits.len(),
                circuit_depth: base_sequence.len() * n_repetitions,
                required_connectivity: Vec::new(),
                execution_time: duration,
                memory_requirements: base_sequence.len() * n_repetitions * target_qubits.len() * 8,
            },
        };

        Ok(DDSequence {
            sequence_type: DDSequenceType::XY8,
            target_qubits: target_qubits.to_vec(),
            duration,
            circuit,
            pulse_timings,
            pulse_phases,
            properties,
        })
    }

    /// Generate XY-16 sequence (placeholder)
    fn generate_xy16_sequence(
        target_qubits: &[QubitId],
        duration: f64,
    ) -> DeviceResult<DDSequence> {
        // For now, use XY8 as base and extend
        let mut xy8_sequence = Self::generate_xy8_sequence(target_qubits, duration)?;
        xy8_sequence.sequence_type = DDSequenceType::XY16;
        xy8_sequence.properties.sequence_order = 4;
        xy8_sequence
            .properties
            .noise_suppression
            .insert(NoiseType::OneOverFNoise, 0.7);
        Ok(xy8_sequence)
    }

    /// Generate Uhrig Dynamical Decoupling (UDD) sequence
    fn generate_udd_sequence(target_qubits: &[QubitId], duration: f64) -> DeviceResult<DDSequence> {
        let n_pulses = 8;
        let mut pulse_timings = Vec::new();
        let mut pulse_phases = Vec::new();

        // UDD pulse timings: τₖ = T * sin²(πk/(2n+2))
        for k in 1..=n_pulses {
            let timing = duration
                * (PI * k as f64 / (2.0 * n_pulses as f64 + 2.0))
                    .sin()
                    .powi(2);
            pulse_timings.push(timing);
            pulse_phases.push(PI); // X rotations
        }

        let mut circuit = Circuit::<32>::new();
        for qubit in target_qubits {
            for _ in 0..n_pulses {
                circuit.add_gate(PauliX { target: *qubit })?;
            }
        }

        let properties = DDSequenceProperties {
            pulse_count: n_pulses * target_qubits.len(),
            sequence_order: n_pulses,
            periodicity: 1,
            symmetry: SequenceSymmetry {
                time_reversal: false,
                phase_symmetry: false,
                rotational_symmetry: false,
                inversion_symmetry: false,
            },
            noise_suppression: {
                let mut suppression = HashMap::new();
                suppression.insert(NoiseType::PhaseDamping, 0.99);
                suppression.insert(NoiseType::OneOverFNoise, 0.9);
                suppression
            },
            resource_requirements: ResourceRequirements {
                gate_count: n_pulses * target_qubits.len(),
                circuit_depth: n_pulses,
                required_connectivity: Vec::new(),
                execution_time: duration,
                memory_requirements: n_pulses * target_qubits.len() * 8,
            },
        };

        Ok(DDSequence {
            sequence_type: DDSequenceType::UDD,
            target_qubits: target_qubits.to_vec(),
            duration,
            circuit,
            pulse_timings,
            pulse_phases,
            properties,
        })
    }

    /// Generate Knill Dynamical Decoupling (KDD) sequence (placeholder)
    fn generate_kdd_sequence(target_qubits: &[QubitId], duration: f64) -> DeviceResult<DDSequence> {
        // Simplified KDD - use CPMG as base with modifications
        let mut cpmg_sequence = Self::generate_cpmg_sequence(target_qubits, duration)?;
        cpmg_sequence.sequence_type = DDSequenceType::KDD;
        cpmg_sequence
            .properties
            .noise_suppression
            .insert(NoiseType::CoherentErrors, 0.95);
        Ok(cpmg_sequence)
    }

    /// Generate other sequence types (placeholders)
    fn generate_qdd_sequence(target_qubits: &[QubitId], duration: f64) -> DeviceResult<DDSequence> {
        let mut base = Self::generate_udd_sequence(target_qubits, duration)?;
        base.sequence_type = DDSequenceType::QDD;
        Ok(base)
    }

    fn generate_cdd_sequence(target_qubits: &[QubitId], duration: f64) -> DeviceResult<DDSequence> {
        let mut base = Self::generate_xy8_sequence(target_qubits, duration)?;
        base.sequence_type = DDSequenceType::CDD;
        Ok(base)
    }

    fn generate_rdd_sequence(target_qubits: &[QubitId], duration: f64) -> DeviceResult<DDSequence> {
        let mut base = Self::generate_xy4_sequence(target_qubits, duration)?;
        base.sequence_type = DDSequenceType::RDD;
        base.properties
            .noise_suppression
            .insert(NoiseType::RandomTelegraphNoise, 0.8);
        Ok(base)
    }

    fn generate_cp_sequence(target_qubits: &[QubitId], duration: f64) -> DeviceResult<DDSequence> {
        let mut base = Self::generate_cpmg_sequence(target_qubits, duration)?;
        base.sequence_type = DDSequenceType::CarrPurcell;
        base.properties.symmetry.phase_symmetry = false;
        Ok(base)
    }

    fn generate_optimized_sequence(
        target_qubits: &[QubitId],
        duration: f64,
    ) -> DeviceResult<DDSequence> {
        // Start with XY8 as base for SciRS2 optimization
        let mut base = Self::generate_xy8_sequence(target_qubits, duration)?;
        base.sequence_type = DDSequenceType::SciRS2Optimized;
        base.properties.sequence_order = 5; // Higher order expected from optimization
        Ok(base)
    }

    fn generate_custom_sequence(
        name: &str,
        target_qubits: &[QubitId],
        duration: f64,
    ) -> DeviceResult<DDSequence> {
        // Placeholder for custom sequences - use CPMG as default
        let mut base = Self::generate_cpmg_sequence(target_qubits, duration)?;
        base.sequence_type = DDSequenceType::Custom(name.to_string());
        Ok(base)
    }
}

/// Sequence cache for performance optimization
#[derive(Debug, Clone)]
pub struct SequenceCache {
    pub cached_sequences: HashMap<String, DDSequence>,
    pub cache_hits: usize,
    pub cache_misses: usize,
}

impl SequenceCache {
    pub fn new() -> Self {
        Self {
            cached_sequences: HashMap::new(),
            cache_hits: 0,
            cache_misses: 0,
        }
    }

    pub fn get_sequence(&mut self, key: &str) -> Option<DDSequence> {
        if let Some(sequence) = self.cached_sequences.get(key) {
            self.cache_hits += 1;
            Some(sequence.clone())
        } else {
            self.cache_misses += 1;
            None
        }
    }

    pub fn store_sequence(&mut self, key: String, sequence: DDSequence) {
        self.cached_sequences.insert(key, sequence);
    }
}

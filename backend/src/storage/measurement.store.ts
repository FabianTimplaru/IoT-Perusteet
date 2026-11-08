import type { Measurement } from './../types/measurement';

// Temporary storage for measurements
// Eventually we will replace with a database
const measurements: Measurement[] = [];

export function addMeasurement(measurement: Measurement): void {
    measurements.push(measurement);
}

export function getAllMeasurements(): Measurement[] {
    return measurements;
}

export function getLatestMeasurement(): Measurement | undefined {
    return measurements.at(-1);
}
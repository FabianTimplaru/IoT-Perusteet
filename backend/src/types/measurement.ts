// Define the Measurement interface to represent the structure of a measurement
export interface Measurement {
    relativeMoisture: number;
    airHumidity: number;
    temperature: number;
    rawAdc: number;
    timestamp: Date;
}
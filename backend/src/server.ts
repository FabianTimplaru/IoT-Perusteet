import express, { Express, Request, Response } from 'express';
import { measurementSchema } from './schemas/measurement.schema';
import type { Measurement } from './types/measurement';
import { addMeasurement, getAllMeasurements, getLatestMeasurement } from './storage/measurement.store';
import { getSettings, updateSettings } from './storage/settings.store';
import { settingsSchema } from './schemas/settings.schema';

const app: Express = express();
const port = 3000;

// Middleware to parse JSON request bodies
app.use(express.json());

// Endpoint to check if the server is running
app.get('/', (req: Request, res: Response) => {
    res.send('Sularin api is running');
});

// Endpoint to check the status of the device and sensor
app.get('/api/status', (req: Request, res: Response) => {
    res.json({
        "status": "online",
        "device": "Pico 2 W",
        "sensor": "soil-moisture"
    });
});

// Endpoint to get the current settings
app.get('/api/settings', (req: Request, res: Response) => {
    res.status(200).json(getSettings());
});

// Endpoint to get all measurements
app.get('/api/measurements', (req: Request, res: Response) => {
    res.status(200).json(getAllMeasurements());
});

// Endpoint to get the latest measurement
app.get('/api/measurements/latest', (req: Request, res: Response) => {
    const latestMeasurement = getLatestMeasurement();
    if (latestMeasurement !== undefined) {
        res.status(200).json(latestMeasurement);
    } else {
        res.status(404).json({
            "error": "No measurements available"
        });
    }
});

// Endpoint to receive measurements from the device
// We use zod to validate the incoming data against the measurementSchema
// We temporary store the measurements in an array, but in a real application we would store them in a database
app.post('/api/measurements', (req: Request, res: Response) => {
    const result = measurementSchema.safeParse(req.body);

    if (result.success) {
        const measurement: Measurement = {
            relativeMoisture: result.data.moisture,
            airHumidity: result.data.airHumidity,
            temperature: result.data.temperature,
            rawAdc: result.data.rawAdc,
            timestamp: new Date()
        };

        console.log("Received measurement:", measurement);

        addMeasurement(measurement);
        res.status(201).json({
            "message": "Measurements received",
            "success": true
        });
    } else {
        res.status(400).json({
            "error": "Invalid measurement data"
        });
    }
});

// Endpoint to update the settings
// We use zod to validate the incoming data against the settingsSchema
// We temporary store the settings in memory, but in a real application we would store them in a database
app.patch('/api/settings', (req: Request, res: Response) => {
    const result = settingsSchema.safeParse(req.body);
    if (result.success) {
        updateSettings(result.data);
        res.status(200).json(getSettings());
    } else {
        res.status(400).json({
            "error": "Invalid settings"
        });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
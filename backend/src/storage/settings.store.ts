import type { Settings } from './../types/settings';


const settings: Settings = {
    minMoistureThreshold: 30
};

export function getSettings(): Settings {
    return settings;
}

export function updateSettings(newSettings: Settings): void {
    settings.minMoistureThreshold = newSettings.minMoistureThreshold;
}
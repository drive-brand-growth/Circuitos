/**
 * OpenWeather MCP Integration
 * Weather-based copy personalization
 *
 * Cost: $0 for 1,000 calls/day (free tier)
 * Setup: Free API key from openweathermap.org
 * Docs: https://openweathermap.org/api
 */

import axios from 'axios';

const OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5';

/**
 * Get current weather by ZIP code
 *
 * @param {string} zipCode - US ZIP code
 * @param {string} countryCode - Country code (default: 'us')
 * @returns {object} Current weather data
 */
export async function getCurrentWeather(zipCode, countryCode = 'us') {
  try {
    if (!process.env.OPENWEATHER_API_KEY) {
      console.warn('OpenWeather: No API key configured, returning mock data');
      return getMockWeather();
    }

    const response = await axios.get(`${OPENWEATHER_BASE_URL}/weather`, {
      params: {
        zip: `${zipCode},${countryCode}`,
        appid: process.env.OPENWEATHER_API_KEY,
        units: 'imperial'  // Fahrenheit
      }
    });

    const data = response.data;

    return {
      temp: Math.round(data.main.temp),
      feelsLike: Math.round(data.main.feels_like),
      condition: data.weather[0].main,
      description: data.weather[0].description,
      humidity: data.main.humidity,
      windSpeed: Math.round(data.wind.speed),
      zipCode,
      city: data.name,

      // Copy personalization signals
      isHot: data.main.temp > 85,
      isCold: data.main.temp < 50,
      isRaining: data.weather[0].main === 'Rain',
      isSnowing: data.weather[0].main === 'Snow',
      isCloudy: data.weather[0].main === 'Clouds',
      isClear: data.weather[0].main === 'Clear'
    };

  } catch (error) {
    console.error('OpenWeather Current Weather Error:', error.message);
    return getMockWeather();
  }
}

/**
 * Get 5-day weather forecast
 *
 * @param {string} zipCode - US ZIP code
 * @param {string} countryCode - Country code
 * @returns {array} Forecast data (next 5 days)
 */
export async function getForecast(zipCode, countryCode = 'us') {
  try {
    if (!process.env.OPENWEATHER_API_KEY) {
      console.warn('OpenWeather: No API key configured, returning empty forecast');
      return [];
    }

    const response = await axios.get(`${OPENWEATHER_BASE_URL}/forecast`, {
      params: {
        zip: `${zipCode},${countryCode}`,
        appid: process.env.OPENWEATHER_API_KEY,
        units: 'imperial'
      }
    });

    // Group by day and get daily highs/lows
    const dailyForecasts = {};

    response.data.list.forEach(item => {
      const date = item.dt_txt.split(' ')[0];

      if (!dailyForecasts[date]) {
        dailyForecasts[date] = {
          date,
          temps: [],
          conditions: []
        };
      }

      dailyForecasts[date].temps.push(item.main.temp);
      dailyForecasts[date].conditions.push(item.weather[0].main);
    });

    // Format daily summaries
    return Object.values(dailyForecasts).slice(0, 5).map(day => ({
      date: day.date,
      high: Math.round(Math.max(...day.temps)),
      low: Math.round(Math.min(...day.temps)),
      condition: getMostCommonCondition(day.conditions),
      isRain: day.conditions.includes('Rain'),
      isSnow: day.conditions.includes('Snow')
    }));

  } catch (error) {
    console.error('OpenWeather Forecast Error:', error.message);
    return [];
  }
}

/**
 * Get weather by lat/lng
 *
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {object} Weather data
 */
export async function getWeatherByCoords(lat, lng) {
  try {
    if (!process.env.OPENWEATHER_API_KEY) {
      return getMockWeather();
    }

    const response = await axios.get(`${OPENWEATHER_BASE_URL}/weather`, {
      params: {
        lat,
        lon: lng,
        appid: process.env.OPENWEATHER_API_KEY,
        units: 'imperial'
      }
    });

    const data = response.data;

    return {
      temp: Math.round(data.main.temp),
      feelsLike: Math.round(data.main.feels_like),
      condition: data.weather[0].main,
      description: data.weather[0].description,
      humidity: data.main.humidity,
      windSpeed: Math.round(data.wind.speed),
      city: data.name,
      isHot: data.main.temp > 85,
      isCold: data.main.temp < 50,
      isRaining: data.weather[0].main === 'Rain',
      isSnowing: data.weather[0].main === 'Snow'
    };

  } catch (error) {
    console.error('OpenWeather Coords Weather Error:', error.message);
    return getMockWeather();
  }
}

/**
 * Generate weather-based copy suggestions
 *
 * @param {object} weather - Weather data
 * @param {string} businessType - Type of business (gym, restaurant, etc.)
 * @returns {object} Copy suggestions
 */
export function getWeatherCopySuggestions(weather, businessType = 'gym') {
  const suggestions = {
    opening: '',
    hook: '',
    cta: '',
    urgency: ''
  };

  // Hot weather
  if (weather.isHot) {
    suggestions.opening = `With temperatures hitting ${weather.temp}°F today`;
    suggestions.hook = businessType === 'gym'
      ? 'our climate-controlled facility is your perfect escape from the heat'
      : 'beat the heat in comfort';
    suggestions.cta = 'Stay cool and crush your goals';
    suggestions.urgency = 'Perfect timing while it\'s scorching outside';
  }

  // Cold weather
  else if (weather.isCold) {
    suggestions.opening = `As temps drop to ${weather.temp}°F`;
    suggestions.hook = businessType === 'gym'
      ? 'keep your momentum going in our heated facility'
      : 'stay warm and focused';
    suggestions.cta = 'Don\'t let cold weather slow you down';
    suggestions.urgency = 'Cold snap is the perfect excuse to stay committed';
  }

  // Rainy weather
  else if (weather.isRaining) {
    suggestions.opening = `Perfect rainy day weather`;
    suggestions.hook = businessType === 'gym'
      ? 'to stay dry while staying active indoors'
      : 'to take advantage of indoor comfort';
    suggestions.cta = 'Rain or shine, keep progressing';
    suggestions.urgency = 'No excuses - rain makes indoor workouts perfect';
  }

  // Snowy weather
  else if (weather.isSnowing) {
    suggestions.opening = `With snow in the forecast`;
    suggestions.hook = 'skip the slippery sidewalks and stay safe indoors';
    suggestions.cta = 'Weather-proof your routine';
    suggestions.urgency = 'Snow day = perfect indoor training day';
  }

  // Clear/nice weather
  else if (weather.isClear && weather.temp >= 65 && weather.temp <= 80) {
    suggestions.opening = `Beautiful ${weather.temp}°F weather today`;
    suggestions.hook = 'perfect conditions to kick off your transformation';
    suggestions.cta = 'Great weather = great momentum';
    suggestions.urgency = 'Capitalize on this perfect weather motivation';
  }

  return suggestions;
}

/**
 * Determine if weather affects business
 * (e.g., gyms benefit from bad weather, outdoor businesses don't)
 *
 * @param {object} weather - Weather data
 * @param {string} businessType - Business type
 * @returns {object} Impact analysis
 */
export function analyzeWeatherImpact(weather, businessType = 'gym') {
  const indoorBusinesses = ['gym', 'restaurant', 'retail', 'service'];
  const outdoorBusinesses = ['landscaping', 'construction', 'roofing'];

  const isIndoor = indoorBusinesses.includes(businessType.toLowerCase());
  const isOutdoor = outdoorBusinesses.includes(businessType.toLowerCase());

  let impact = 'neutral';
  let messaging = 'standard';

  // Bad weather helps indoor businesses
  if (isIndoor && (weather.isRaining || weather.isSnowing || weather.isHot || weather.isCold)) {
    impact = 'positive';
    messaging = 'emphasize_indoor_advantage';
  }

  // Bad weather hurts outdoor businesses
  if (isOutdoor && (weather.isRaining || weather.isSnowing)) {
    impact = 'negative';
    messaging = 'postpone_or_reschedule';
  }

  // Great weather helps everyone
  if (weather.isClear && weather.temp >= 65 && weather.temp <= 80) {
    impact = 'positive';
    messaging = 'capitalize_on_mood';
  }

  return {
    impact,
    messaging,
    shouldMentionWeather: impact !== 'neutral',
    advantage: isIndoor && (weather.isRaining || weather.isHot || weather.isCold)
  };
}

/**
 * Mock weather data for development
 */
function getMockWeather() {
  return {
    temp: 75,
    feelsLike: 77,
    condition: 'Clear',
    description: 'clear sky',
    humidity: 65,
    windSpeed: 8,
    zipCode: '76102',
    city: 'Fort Worth',
    isHot: false,
    isCold: false,
    isRaining: false,
    isSnowing: false,
    isCloudy: false,
    isClear: true
  };
}

/**
 * Get most common condition from array
 */
function getMostCommonCondition(conditions) {
  const counts = {};
  conditions.forEach(c => counts[c] = (counts[c] || 0) + 1);
  return Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
}

/**
 * Check if weather is extreme (for urgent messaging)
 *
 * @param {object} weather - Weather data
 * @returns {boolean} Is extreme weather
 */
export function isExtremeWeather(weather) {
  return (
    weather.temp > 95 ||  // Heat wave
    weather.temp < 32 ||  // Freezing
    weather.isSnowing ||  // Snow
    (weather.isRaining && weather.windSpeed > 20)  // Storm
  );
}

export default {
  getCurrentWeather,
  getForecast,
  getWeatherByCoords,
  getWeatherCopySuggestions,
  analyzeWeatherImpact,
  isExtremeWeather
};

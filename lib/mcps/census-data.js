/**
 * US Census Bureau MCP Integration
 * FREE: Unlimited API calls, no key required
 *
 * Features:
 * - Demographics by ZIP code
 * - Income data
 * - Age distribution
 * - Education levels
 * - Population density
 */

const CENSUS_API_BASE = 'https://api.census.gov/data/2021/acs/acs5';

/**
 * Get comprehensive demographics for a ZIP code
 */
export async function getDemographicsByZip(zipCode) {
  // Census API variables:
  // B01003_001E - Total population
  // B19013_001E - Median household income
  // B01002_001E - Median age
  // B15003_022E - Bachelor's degree
  // B15003_023E - Master's degree
  // B11001_001E - Total households

  const variables = [
    'NAME',
    'B01003_001E', // Population
    'B19013_001E', // Income
    'B01002_001E', // Age
    'B15003_022E', // Bachelor's
    'B15003_023E', // Master's
    'B11001_001E'  // Households
  ].join(',');

  const url = `${CENSUS_API_BASE}?get=${variables}&for=zip%20code%20tabulation%20area:${zipCode}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Census API error: ${response.status}`);
  }

  const data = await response.json();

  if (!data || data.length < 2) {
    throw new Error('No Census data available for this ZIP code');
  }

  // Data format: [headers, values]
  const values = data[1];

  const population = parseInt(values[1]) || 0;
  const medianIncome = parseInt(values[2]) || 0;
  const medianAge = parseFloat(values[3]) || 0;
  const bachelors = parseInt(values[4]) || 0;
  const masters = parseInt(values[5]) || 0;
  const households = parseInt(values[6]) || 0;

  // Calculate derived metrics
  const educationRate = population > 0 ? ((bachelors + masters) / population) : 0;

  return {
    zip_code: zipCode,
    name: values[0],
    population,
    median_income: medianIncome,
    median_age: medianAge,
    total_households: households,
    education: {
      bachelors_count: bachelors,
      masters_count: masters,
      higher_ed_rate: educationRate.toFixed(3)
    },
    derived: {
      affluence: classifyAffluence(medianIncome),
      education_level: classifyEducation(educationRate),
      age_group: classifyAgeGroup(medianAge),
      household_size: population > 0 ? (population / households).toFixed(1) : 0
    }
  };
}

/**
 * Get income distribution for ZIP code
 */
export async function getIncomeDistribution(zipCode) {
  // Income bracket variables
  const variables = [
    'NAME',
    'B19001_002E', // <$10k
    'B19001_003E', // $10k-$15k
    'B19001_004E', // $15k-$20k
    'B19001_005E', // $20k-$25k
    'B19001_006E', // $25k-$30k
    'B19001_007E', // $30k-$35k
    'B19001_008E', // $35k-$40k
    'B19001_009E', // $40k-$45k
    'B19001_010E', // $45k-$50k
    'B19001_011E', // $50k-$60k
    'B19001_012E', // $60k-$75k
    'B19001_013E', // $75k-$100k
    'B19001_014E', // $100k-$125k
    'B19001_015E', // $125k-$150k
    'B19001_016E', // $150k-$200k
    'B19001_017E'  // $200k+
  ].join(',');

  const url = `${CENSUS_API_BASE}?get=${variables}&for=zip%20code%20tabulation%20area:${zipCode}`;

  const response = await fetch(url);
  const data = await response.json();

  if (!data || data.length < 2) {
    throw new Error('No income data for ZIP');
  }

  const values = data[1].slice(1, -1).map(v => parseInt(v) || 0);

  const totalHouseholds = values.reduce((sum, v) => sum + v, 0);

  return {
    zip_code: zipCode,
    total_households: totalHouseholds,
    brackets: {
      under_30k: values[0] + values[1] + values[2] + values[3] + values[4],
      _30k_to_60k: values[5] + values[6] + values[7] + values[8] + values[9],
      _60k_to_100k: values[10] + values[11],
      _100k_to_150k: values[12] + values[13],
      over_150k: values[14] + values[15]
    },
    percentages: {
      under_30k: ((values[0] + values[1] + values[2] + values[3] + values[4]) / totalHouseholds * 100).toFixed(1),
      _30k_to_60k: ((values[5] + values[6] + values[7] + values[8] + values[9]) / totalHouseholds * 100).toFixed(1),
      _60k_to_100k: ((values[10] + values[11]) / totalHouseholds * 100).toFixed(1),
      _100k_to_150k: ((values[12] + values[13]) / totalHouseholds * 100).toFixed(1),
      over_150k: ((values[14] + values[15]) / totalHouseholds * 100).toFixed(1)
    }
  };
}

/**
 * Get age distribution for ZIP code
 */
export async function getAgeDistribution(zipCode) {
  const variables = [
    'NAME',
    'B01001_003E', // Male 0-4
    'B01001_004E', // Male 5-9
    'B01001_005E', // Male 10-14
    'B01001_006E', // Male 15-17
    'B01001_007E', // Male 18-19
    'B01001_008E', // Male 20
    'B01001_009E', // Male 21
    'B01001_010E', // Male 22-24
    'B01001_011E', // Male 25-29
    'B01001_012E', // Male 30-34
    'B01001_013E', // Male 35-39
    'B01001_014E', // Male 40-44
    'B01001_015E', // Male 45-49
    'B01001_016E', // Male 50-54
    'B01001_017E', // Male 55-59
    'B01001_018E', // Male 60-61
    'B01001_019E', // Male 62-64
    'B01001_020E', // Male 65-66
    'B01001_021E', // Male 67-69
    'B01001_022E', // Male 70-74
    'B01001_023E', // Male 75-79
    'B01001_024E', // Male 80-84
    'B01001_025E'  // Male 85+
  ].join(',');

  const url = `${CENSUS_API_BASE}?get=${variables}&for=zip%20code%20tabulation%20area:${zipCode}`;

  const response = await fetch(url);
  const data = await response.json();

  if (!data || data.length < 2) {
    throw new Error('No age data for ZIP');
  }

  const values = data[1].slice(1, -1).map(v => parseInt(v) || 0);

  // Multiply by 2 to account for both genders (rough estimate)
  const totalPop = values.reduce((sum, v) => sum + v, 0) * 2;

  return {
    zip_code: zipCode,
    age_groups: {
      under_18: (values[0] + values[1] + values[2] + values[3]) * 2,
      _18_to_24: (values[4] + values[5] + values[6] + values[7]) * 2,
      _25_to_34: (values[8] + values[9]) * 2,
      _35_to_44: (values[10] + values[11]) * 2,
      _45_to_54: (values[12] + values[13]) * 2,
      _55_to_64: (values[14] + values[15] + values[16]) * 2,
      over_65: (values[17] + values[18] + values[19] + values[20] + values[21] + values[22]) * 2
    },
    total_population: totalPop
  };
}

// Helper functions
function classifyAffluence(income) {
  if (income >= 100000) return 'high';
  if (income >= 75000) return 'upper_middle';
  if (income >= 50000) return 'middle';
  if (income >= 35000) return 'lower_middle';
  return 'low';
}

function classifyEducation(rate) {
  if (rate >= 0.4) return 'high';
  if (rate >= 0.25) return 'medium';
  return 'low';
}

function classifyAgeGroup(medianAge) {
  if (medianAge < 30) return 'young';
  if (medianAge < 45) return 'middle_aged';
  if (medianAge < 60) return 'mature';
  return 'senior';
}

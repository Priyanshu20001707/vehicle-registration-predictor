use SmartVehicleDb;

-- 1. Top 5 Vehicle Manufacturers for Each Year
SELECT *
FROM (
    SELECT 
        year,
        makerName,
        COUNT(*) AS total_vehicles,
        RANK() OVER (PARTITION BY year ORDER BY COUNT(*) DESC) AS manufacturer_rank
    FROM vehicle_data_cleaned
    WHERE year IS NOT NULL
    GROUP BY year, makerName
) AS ranked_makers
WHERE manufacturer_rank <= 5
ORDER BY year, manufacturer_rank;

--2. Fuel-Type Sales Distribution Across Registration Offices

SELECT 
    OfficeCd,
    fuel_type_group,
    COUNT(*) AS total_vehicles
FROM vehicle_data_cleaned
WHERE fuel_type_group IS NOT NULL AND OfficeCd IS NOT NULL
GROUP BY OfficeCd, fuel_type_group
ORDER BY OfficeCd, total_vehicles DESC;

-- 3. Detect Spikes in Registration Activity Before Festivals or Year-End

SELECT 
    DATENAME(year, fromdate) AS reg_year,
    DATENAME(month, fromdate) AS reg_month,
    MONTH(fromdate) AS month_number,
    COUNT(*) AS total_registrations
FROM vehicle_data_cleaned
WHERE fromdate IS NOT NULL
GROUP BY DATENAME(year, fromdate), DATENAME(month, fromdate), MONTH(fromdate)
ORDER BY reg_year, month_number;

--4. EV Adoption Trend Month-Wise

SELECT 
    FORMAT(fromdate, 'yyyy-MM') AS month_year,
    COUNT(*) AS ev_registrations
FROM vehicle_data_cleaned
WHERE LOWER(fuel_type_group) = 'ev'
GROUP BY FORMAT(fromdate, 'yyyy-MM')
ORDER BY month_year;



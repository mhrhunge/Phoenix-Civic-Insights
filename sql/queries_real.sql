-- Trend in city water production
SELECT
  year,
  month,
  million_gallons,
  LAG(million_gallons) OVER (ORDER BY year, month) AS prev_mg,
  (million_gallons - prev_mg) * 100.0 / prev_mg AS pct_change
FROM phoenix_water_production
ORDER BY year, month;

-- Top call types
SELECT
  final_call_type,
  COUNT(*) AS call_count
FROM phoenix_calls_for_service
GROUP BY final_call_type
ORDER BY call_count DESC
LIMIT 25;

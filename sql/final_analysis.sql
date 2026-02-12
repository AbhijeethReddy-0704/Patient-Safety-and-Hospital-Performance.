USE Healthcare_Analysis;

SELECT
    g.`Facility Name`            AS Facility_Name,
    g.`City/Town`                AS City,
    g.`Hospital overall rating`  AS Hospital_overall_rating,
    s.`Measure Name`             AS Measure_Name,
    s.`Score`                    AS Mortality_Score
FROM cleaned_general_info g
JOIN cleaned_safety_scores s
    ON g.`Facility ID` = s.`Facility ID`
WHERE g.`State` = 'TX'
  AND g.`Hospital overall rating` = 5
  AND s.`Measure ID` = 'MORT_30_AMI'
ORDER BY s.`Score` ASC;
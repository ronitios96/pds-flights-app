-- CS 6083 HW3, Question 4: Metadata Queries
-- Using the airline flights database (same schema as Problem 1)

-- (a) Tables with at least 2 outgoing foreign keys referencing distinct tables
SELECT tc.table_name
FROM information_schema.table_constraints tc
JOIN information_schema.referential_constraints rc
  ON tc.constraint_name = rc.constraint_name
JOIN information_schema.table_constraints tc2
  ON rc.unique_constraint_name = tc2.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
GROUP BY tc.table_name
HAVING COUNT(DISTINCT tc2.table_name) >= 2;


-- (b) All columns configured to store timestamp/date type data
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND data_type IN ('date', 'timestamp without time zone',
                    'timestamp with time zone',
                    'time without time zone',
                    'time with time zone',
                    'interval')
ORDER BY table_name, ordinal_position;


-- (c) Distinct values per attribute in the Flight table
SELECT 'flight_number' AS attribute,
       COUNT(DISTINCT flight_number) AS distinct_count
FROM Flight
UNION ALL
SELECT 'departure_date', COUNT(DISTINCT departure_date)
FROM Flight
UNION ALL
SELECT 'plane_type', COUNT(DISTINCT plane_type)
FROM Flight;


-- (d) Tables where the primary key is composite (more than one attribute)
SELECT tc.table_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
WHERE tc.constraint_type = 'PRIMARY KEY'
  AND tc.table_schema = 'public'
GROUP BY tc.table_name
HAVING COUNT(kcu.column_name) > 1;


-- (e) All attributes containing the substring "name"
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND column_name LIKE '%name%'
ORDER BY table_name, column_name;

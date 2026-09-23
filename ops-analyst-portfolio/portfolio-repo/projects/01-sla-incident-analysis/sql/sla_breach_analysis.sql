-- SLA breach root-cause pull: 90 days of tickets with SLA outcomes
-- Warehouse-flavored for BigQuery. Adjust table + SLA targets to your org.

WITH tickets AS (
  SELECT
    ticket_id,
    created_at,
    first_responded_at,
    resolved_at,
    priority,            -- P1/P2/P3/P4
    channel,             -- email / chat / phone / portal
    agent_id,
    TIMESTAMP_DIFF(first_responded_at, created_at, MINUTE) AS first_response_min,
    TIMESTAMP_DIFF(resolved_at, created_at, HOUR)          AS resolution_hours
  FROM `support_prod.tickets`
  WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
    AND status = 'resolved'
),
sla AS (
  SELECT
    t.*,
    -- first-response SLA targets by priority (minutes)
    CASE priority WHEN 'P1' THEN 15 WHEN 'P2' THEN 60
                  WHEN 'P3' THEN 240 ELSE 480 END AS fr_target_min,
    -- resolution SLA targets by priority (hours)
    CASE priority WHEN 'P1' THEN 4  WHEN 'P2' THEN 8
                  WHEN 'P3' THEN 24 ELSE 72 END     AS res_target_hours
  FROM tickets t
)
SELECT
  ticket_id,
  priority,
  channel,
  agent_id,
  first_response_min,
  resolution_hours,
  fr_target_min,
  res_target_hours,
  first_response_min > fr_target_min     AS fr_breached,
  resolution_hours > res_target_hours    AS res_breached,
  DATE_TRUNC(DATE(created_at), WEEK)     AS week_started
FROM sla;

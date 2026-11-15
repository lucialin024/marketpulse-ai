
-- =========================================
-- QUERY 1: STOCK PERFORMANCE RANKING
-- =========================================

WITH ranked_prices AS (
    SELECT
        s.ticker,
        p.date,
        p.close_price,
        ROW_NUMBER() OVER (
            PARTITION BY s.ticker
            ORDER BY p.date ASC
        ) AS first_rank,
        ROW_NUMBER() OVER (
            PARTITION BY s.ticker
            ORDER BY p.date DESC
        ) AS last_rank
    FROM stock_prices AS p
    JOIN stocks AS s
        ON p.stock_id = s.stock_id
),
performance AS (
    SELECT
        ticker,
        MAX(CASE WHEN first_rank = 1
            THEN close_price END) AS first_price,
        MAX(CASE WHEN last_rank = 1
            THEN close_price END) AS latest_price
    FROM ranked_prices
    GROUP BY ticker
)
SELECT
    ticker,
    ROUND(first_price, 2) AS first_price,
    ROUND(latest_price, 2) AS latest_price,
    ROUND(
        (latest_price / NULLIF(first_price, 0) - 1) * 100,
        2
    ) AS period_return_pct
FROM performance
ORDER BY period_return_pct DESC;


-- =========================================
-- QUERY 2: MOVING AVERAGE ANALYSIS
-- =========================================

WITH averages AS (
    SELECT
        s.ticker,
        p.date,
        p.close_price,

        AVG(p.close_price) OVER (
            PARTITION BY s.ticker
            ORDER BY p.date
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) AS ma_5,

        AVG(p.close_price) OVER (
            PARTITION BY s.ticker
            ORDER BY p.date
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) AS ma_20,

        ROW_NUMBER() OVER (
            PARTITION BY s.ticker
            ORDER BY p.date
        ) AS observation_number

    FROM stock_prices AS p
    JOIN stocks AS s
        ON p.stock_id = s.stock_id
)
SELECT
    ticker,
    date,
    ROUND(close_price, 2) AS close_price,
    ROUND(ma_5, 2) AS moving_avg_5,
    CASE
        WHEN observation_number >= 20
        THEN ROUND(ma_20, 2)
        ELSE NULL
    END AS moving_avg_20
FROM averages
WHERE ticker = 'AAPL'
ORDER BY date DESC
LIMIT 20;


-- =========================================
-- QUERY 3: SIGNIFICANT PRICE MOVEMENTS
-- =========================================

SELECT
    s.ticker,
    p.date,
    ROUND(p.close_price, 2) AS close_price,
    ROUND(p.daily_return * 100, 2)
        AS daily_return_pct,

    CASE
        WHEN p.daily_return >= 0.03
            THEN 'Large Increase'
        WHEN p.daily_return <= -0.03
            THEN 'Large Decrease'
    END AS market_signal

FROM stock_prices AS p
JOIN stocks AS s
    ON p.stock_id = s.stock_id

WHERE ABS(p.daily_return) >= 0.03

ORDER BY p.date DESC, ABS(p.daily_return) DESC
LIMIT 30;


-- =========================================
-- QUERY 4: UNUSUAL TRADING VOLUME
-- =========================================

WITH volume_analysis AS (
    SELECT
        s.ticker,
        p.date,
        p.volume,

        AVG(p.volume) OVER (
            PARTITION BY s.ticker
            ORDER BY p.date
            ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING
        ) AS previous_20_day_avg_volume,

        ROW_NUMBER() OVER (
            PARTITION BY s.ticker
            ORDER BY p.date
        ) AS observation_number

    FROM stock_prices AS p
    JOIN stocks AS s
        ON p.stock_id = s.stock_id
)
SELECT
    ticker,
    date,
    volume,
    ROUND(previous_20_day_avg_volume, 0)
        AS average_volume,
    ROUND(
        volume * 1.0 /
        NULLIF(previous_20_day_avg_volume, 0),
        2
    ) AS volume_ratio

FROM volume_analysis

WHERE observation_number >= 21
    AND volume >= 2 * previous_20_day_avg_volume

ORDER BY date DESC
LIMIT 30;
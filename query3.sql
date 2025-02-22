SELECT COUNT(*) AS auctions_with_4_categories
FROM (
    SELECT ItemID
    FROM ItemCategory
    GROUP BY ItemID
    HAVING COUNT(*) = 4
) AS t;

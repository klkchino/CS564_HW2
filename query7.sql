SELECT COUNT(DISTINCT ic.CategoryName) AS categories_with_bid_over_100
FROM ItemCategory ic
JOIN Bids b ON ic.ItemID = b.ItemID
WHERE b.Amount > 100;

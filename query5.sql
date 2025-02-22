SELECT COUNT(DISTINCT Seller_UserID) AS sellers_over_1000
FROM Items i
JOIN Users u ON i.Seller_UserID = u.UserID
WHERE u.Rating > 1000;

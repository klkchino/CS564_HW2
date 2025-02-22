SELECT COUNT(*) AS seller_and_bidder
FROM (
  SELECT DISTINCT Seller_UserID AS user
  FROM Items
  INTERSECT
  SELECT DISTINCT Bidder_UserID
  FROM Bids
) AS both;

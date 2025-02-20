drop table if exists Item;
CREATE TABLE Items (
    ItemID INT NOT NULL,               
    Name TEXT NOT NULL,               
    Currently INT NOT NULL,
    Buy_Price INT,
    First_Bid INT NOT NULL,    
    Number_of_Bids INT NOT NULL,                            
    Started DATETIME NOT NULL,         
    Ends DATETIME NOT NULL,            
    Description TEXT,                  
    Seller_UserID CHAR(255) NOT NULL,  
    PRIMARY KEY (ItemID),             
    FOREIGN KEY (Seller_UserID) REFERENCES Users(UserID)  
);

drop table if exists Users;
CREATE TABLE Users (
    UserID CHAR(255) NOT NULL UNIQUE,       
    Rating INT NOT NULL,              
    Location TEXT,                    
    Country TEXT,                     
    PRIMARY KEY (UserID)             
);

drop table if exists Bids;
CREATE TABLE Bids (   
    ItemID INT NOT NULL,                  
    Bidder_UserID CHAR(255) NOT NULL,     
    Time DATETIME NOT NULL,                
    Amount INT NOT NULL,                       
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),      
    FOREIGN KEY (Bidder_UserID) REFERENCES Users(UserID),
    PRIMARY KEY (ItemID, Bidder_UserID, Amount)
);

drop table if exists Categories;
CREATE TABLE Categories (
    CategoryID INT NOT NULL,  
    CategoryName CHAR(255) NOT NULL,
    FOREIGN KEY (CategoryID) REFERENCES Items(ItemID),
    PRIMARY KEY (CategoryID, CategoryName)      
);
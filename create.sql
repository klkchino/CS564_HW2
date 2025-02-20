drop table if exists Items;
CREATE TABLE Items (
    ItemID INT NOT NULL,               
    Name TEXT NOT NULL,               
    Currently REAL NOT NULL,
    Buy_Price REAL,
    First_Bid REAL NOT NULL,    
    Number_of_Bids INT NOT NULL,                            
    Started DATETIME NOT NULL,         
    Ends DATETIME NOT NULL,            
    Description TEXT NOT NULL,                  
    Seller_UserID CHAR(255) NOT NULL,  
    PRIMARY KEY (ItemID),             
    FOREIGN KEY (Seller_UserID) REFERENCES Users(UserID)  
);

drop table if exists Users;
CREATE TABLE Users (
    UserID CHAR(255) NOT NULL,       
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
    Amount REAL NOT NULL,                       
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),      
    FOREIGN KEY (Bidder_UserID) REFERENCES Users(UserID),
    PRIMARY KEY (ItemID, Bidder_UserID, Time)
);

drop table if exists Categories;
CREATE TABLE Categories (
    CategoryName CHAR(255) NOT NULL,
    PRIMARY KEY (CategoryName)      
);

drop table if exists ItemCategory;
CREATE TABLE ItemCategory (
    ItemID INT NOT NULL,
    CategoryName CHAR(255) NOT NULL,
    PRIMARY KEY (ItemID, CategoryName),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
    FOREIGN KEY (CategoryName) REFERENCES Categories(CategoryName)
);

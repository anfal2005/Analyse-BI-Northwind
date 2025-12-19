---------------------------------------------------------
-- 1. CREATE DATABASE
---------------------------------------------------------
CREATE DATABASE DataWarehouse;
GO
USE DataWarehouse;
GO

---------------------------------------------------------
-- 2. DIMENSION: CLIENT
---------------------------------------------------------
CREATE TABLE client (
    id_client INT IDENTITY(1,1) PRIMARY KEY,
    customerid NVARCHAR(100),
    fullname VARCHAR(50),
    address NVARCHAR(50),
    country VARCHAR(50),
    company VARCHAR(50)
);

---------------------------------------------------------
-- 3. DIMENSION: EMPLOYEE
---------------------------------------------------------
CREATE TABLE employee (
    id_employee INT IDENTITY(1,1) PRIMARY KEY,
    employeeid INT NOT NULL,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    address NVARCHAR(100),
    country VARCHAR(50),
    homenumber NVARCHAR(100),
    job VARCHAR(50),
    region NVARCHAR(50)
);

---------------------------------------------------------
-- 4. DIMENSION: TEMPS (DATE DIMENSION)
---------------------------------------------------------
CREATE TABLE temps (
    id_date INT IDENTITY(1,1) PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    startdate DATE NOT NULL
);

DECLARE @start DATE = '1952-11-01';
DECLARE @today DATE = CAST(EOMONTH(GETDATE()) AS DATE);  -- fin du mois actuel

WHILE @start <= @today
BEGIN
    INSERT INTO temps(year, month, startdate)
    VALUES (YEAR(@start), MONTH(@start), @start);

    SET @start = DATEADD(MONTH, 1, @start);
END;


---------------------------------------------------------
-- 5. FACT TABLE: ORDER DETAILS (faitcommande)
---------------------------------------------------------
CREATE TABLE faitcommande (
    id INT IDENTITY(1,1) PRIMARY KEY,
	order_id INT NOT NULL,
    customer_id INT,
    employee_id INT NOT NULL,
    date_id INT NOT NULL,

    
    ship_address NVARCHAR(100),
    ship_country VARCHAR(100),
    order_status INT  -- 1 delivered, 0 not delivered
);

---------------------------------------------------------
-- FOREIGN KEYS
---------------------------------------------------------
ALTER TABLE faitcommande
ADD CONSTRAINT fk_client
    FOREIGN KEY (customer_id) REFERENCES client(id_client),
    CONSTRAINT fk_employee
    FOREIGN KEY (employee_id) REFERENCES employee(id_employee),
    CONSTRAINT fk_temps
    FOREIGN KEY (date_id) REFERENCES temps(id_date);



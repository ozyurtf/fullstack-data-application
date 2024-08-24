-- PostalCode table
CREATE TABLE PostalCode ( 
    Zip CHAR(5) PRIMARY KEY, 
    City VARCHAR(30),  
    State VARCHAR(30)
);

-- Prospect table
CREATE TABLE Prospect (
    ProspectID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Street VARCHAR(50),
    ContactDate DATE,
    Phone CHAR(12),
	DOB DATE,
	Gender VARCHAR(20),	
    EmailAddress VARCHAR(50),
    Zip CHAR(5) NOT NULL,
    FOREIGN KEY (Zip) REFERENCES PostalCode(Zip)
);

CREATE INDEX IX_Prospect_Zip ON Prospect(Zip);

-- Customer table
CREATE TABLE Customer (
    CustomerSSN CHAR(11) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Street VARCHAR(50),
    Phone CHAR(12),
	DOB DATE,
	Gender VARCHAR(20),
    EmailAddress VARCHAR(50),
    Zip CHAR(5) NOT NULL,	
    ProspectID INT NOT NULL,
	FOREIGN KEY (Zip) REFERENCES PostalCode(Zip),
    FOREIGN KEY (ProspectID) REFERENCES Prospect(ProspectID)
);

CREATE INDEX IX_Customer_ProspectID ON Customer(ProspectID);

-- ParticipantClaimant table
CREATE TABLE ParticipantClaimant (
    ParticipantSSN CHAR(11) PRIMARY KEY,
    CustomerSSN CHAR(11) NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DOB DATE,
    Gender VARCHAR(20),
    EmailAddress VARCHAR(50),
    Street VARCHAR(50),
    Zip CHAR(5),
    FOREIGN KEY (CustomerSSN) REFERENCES Customer(CustomerSSN),
    FOREIGN KEY (Zip) REFERENCES PostalCode(Zip)
);

CREATE INDEX IX_ParticipantClaimant_CustomerSSN ON ParticipantClaimant(CustomerSSN);
CREATE INDEX IX_ParticipantClaimant_Zip ON ParticipantClaimant(Zip);

-- Policy table
CREATE TABLE Policy (
    PolicyID VARCHAR(50) PRIMARY KEY,
	PolicyName VARCHAR(50),
    MaximumLifeTimeBenefit BIGINT,
    RenewalTerms VARCHAR(50),
    CoPayment INT,
    CoInsuranceRate INT,
    Deductible INT
);

-- Contract table
CREATE TABLE Contract ( 
    ContractNumber VARCHAR(50) PRIMARY KEY,
    ContractType VARCHAR(10),
    GroupNumber VARCHAR(20), 
    EffectiveDate DATE, 
	ExpirationDate DATE, 
    RenewalDate DATE, 
    PolicyID VARCHAR(50) NOT NULL, 
    CustomerSSN CHAR(11) NOT NULL, 
    FOREIGN KEY (PolicyID) REFERENCES Policy(PolicyID),
    FOREIGN KEY (CustomerSSN) REFERENCES Customer(CustomerSSN)
);

CREATE INDEX IX_Contract_PolicyID ON Contract(PolicyID);
CREATE INDEX IX_Contract_CustomerSSN ON Contract(CustomerSSN);

-- CoveredConditions table
CREATE TABLE CoveredConditions (
    PolicyID VARCHAR(50) NOT NULL,
    CoveredCondition VARCHAR(100),
    PRIMARY KEY (PolicyID, CoveredCondition),
    FOREIGN KEY (PolicyID) REFERENCES Policy(PolicyID)
);

CREATE INDEX IX_CoveredConditions_PolicyID ON CoveredConditions(PolicyID);

-- InNetworkProviders table
CREATE TABLE InNetworkProviders (
    PolicyID VARCHAR(50) NOT NULL,
    InNetworkProvider VARCHAR(50),
    PRIMARY KEY (PolicyID, InNetworkProvider),
    FOREIGN KEY (PolicyID) REFERENCES Policy(PolicyID)
);

CREATE INDEX IX_InNetworkProviders_PolicyID ON InNetworkProviders(PolicyID);

-- CoveredBy table
CREATE TABLE CoveredBy (
    ParticipantSSN CHAR(11) NOT NULL,
    ContractNumber VARCHAR(50) NOT NULL,
    PRIMARY KEY (ParticipantSSN, ContractNumber),
    FOREIGN KEY (ParticipantSSN) REFERENCES ParticipantClaimant(ParticipantSSN),
    FOREIGN KEY (ContractNumber) REFERENCES Contract(ContractNumber)
);

CREATE INDEX IX_CoveredBy_ParticipantSSN ON CoveredBy(ParticipantSSN);
CREATE INDEX IX_CoveredBy_ContractNumber ON CoveredBy(ContractNumber);

-- Claim table with partitioning
CREATE TABLE Claim (
    ClaimNumber VARCHAR(20),
    DateOfService DATE,
    DateOfClaim DATE,
    SettlementDate DATE,
    ClaimDescription VARCHAR(200),
    ClaimAmount DECIMAL(10, 2),
    ClaimStatus VARCHAR(30),
    ParticipantSSN CHAR(11) NOT NULL,
    ContractNumber VARCHAR(50) NOT NULL,
    PRIMARY KEY (ClaimNumber, DateOfClaim),
    FOREIGN KEY (ParticipantSSN) REFERENCES ParticipantClaimant(ParticipantSSN),
    FOREIGN KEY (ContractNumber) REFERENCES Contract(ContractNumber)
) PARTITION BY RANGE (DateOfClaim);

-- Create partitions for Claim
CREATE TABLE Claim_p1 PARTITION OF Claim FOR VALUES FROM ('2010-01-01') TO ('2015-01-01');
CREATE TABLE Claim_p2 PARTITION OF Claim FOR VALUES FROM ('2015-01-01') TO ('2020-01-01');
CREATE TABLE Claim_p3 PARTITION OF Claim FOR VALUES FROM ('2020-01-01') TO ('2025-01-01');
CREATE TABLE Claim_p4 PARTITION OF Claim FOR VALUES FROM ('2025-01-01') TO (MAXVALUE);

CREATE INDEX IX_Claim_DateOfClaim ON Claim(DateOfClaim);
CREATE INDEX IX_Claim_ParticipantSSN ON Claim(ParticipantSSN);
CREATE INDEX IX_Claim_ContractNumber ON Claim(ContractNumber);

-- Account table with partitioning
CREATE TABLE Account ( 
    AcctNumber VARCHAR(50),
    CustomerSSN CHAR(11) NOT NULL,
    NoMonthsInactive INT, 
    ActivityStatus VARCHAR(30),
    ActivityStatusDate DATE, 
    AccountEstablishedDate DATE,
	PRIMARY KEY (AcctNumber, AccountEstablishedDate),
    FOREIGN KEY (CustomerSSN) REFERENCES Customer(CustomerSSN)
) PARTITION BY RANGE (AccountEstablishedDate);

-- Create partitions for Account
CREATE TABLE Account_p1 PARTITION OF Account FOR VALUES FROM ('2010-01-01') TO ('2015-01-01');
CREATE TABLE Account_p2 PARTITION OF Account FOR VALUES FROM ('2015-01-01') TO ('2020-01-01');
CREATE TABLE Account_p3 PARTITION OF Account FOR VALUES FROM ('2020-01-01') TO ('2025-01-01');
CREATE TABLE Account_p4 PARTITION OF Account FOR VALUES FROM ('2025-01-01') TO (MAXVALUE);

CREATE INDEX IX_Account_AccountEstablishedDate ON Account(AccountEstablishedDate);
CREATE INDEX IX_Account_CustomerSSN ON Account(CustomerSSN);

-- Operation table
CREATE TABLE Operation ( 
    GeoCode VARCHAR(10) PRIMARY KEY,
    OperationName VARCHAR(50)
);

-- BillingAccount table
CREATE TABLE BillingAccount (
    BAcctNumber VARCHAR(50) PRIMARY KEY,
	AcctNumber VARCHAR(50),
    BillingStreet VARCHAR(50), 
    BillingAptNo INT,
    BillingZip CHAR(5) NOT NULL,
    BillingPhone CHAR(12),
    BillingMethod VARCHAR(50),
    OnlineBillingFlag CHAR(1) DEFAULT 'F',
    CoverageType VARCHAR(50),
    LastInvoiceGenDate DATE,
    LastInvoicePaidDueDate DATE,
    LastInvoicePaidDate DATE,  
    LastBillCount INT DEFAULT 0,
    NextInvoiceGenDate DATE, 
    CardType VARCHAR(50),
    CardNo VARCHAR(30),
    CardExpirationDate DATE,
    BankingAccountType VARCHAR(30),
    BankingAccountNumber VARCHAR(20),
    PaymentAmount DECIMAL(5, 2),
    PaymentDate DATE,
	AccountEstablishedDate DATE NOT NULL, 
    FOREIGN KEY (AcctNumber, AccountEstablishedDate) REFERENCES Account(AcctNumber, AccountEstablishedDate),
    FOREIGN KEY (BillingZip) REFERENCES PostalCode(Zip)
);

CREATE INDEX IX_BillingAccount_AcctNumber ON Account(AcctNumber);
CREATE INDEX IX_BillingAccount_Zip ON BillingAccount(BillingZip);

-- ChronicDiseaseForecast table
CREATE TABLE ChronicDiseaseForecast (
    State VARCHAR(20) PRIMARY KEY,    
    MortalityCountCurrentYear INT,
    MortalityCountNextYear INT, 
    HospitalizationCountCurrentYear INT, 
    HospitalizationCountNextYear INT, 
    MortalityChange DECIMAL(3, 2),
    HospitalizationChange DECIMAL(3, 2),
    PremiumAmountIncreaseRate DECIMAL(3, 2)
);

-- ContractPremium table
CREATE TABLE ContractPremium (
    PremiumCode VARCHAR(50),
    ContractNumber VARCHAR(50) NOT NULL,
    CustomerSSN CHAR(11) NOT NULL,
    PremiumAmount DECIMAL(10, 2),
    PremiumFrequency VARCHAR(20),
    PaymentMethod VARCHAR(50),
    Status VARCHAR(20),
    PRIMARY KEY (PremiumCode, ContractNumber),
    FOREIGN KEY (ContractNumber) REFERENCES Contract(ContractNumber), 
    FOREIGN KEY (CustomerSSN) REFERENCES Customer(CustomerSSN)
);

CREATE INDEX IX_ContractPremium_ContractNumber ON ContractPremium(ContractNumber);
CREATE INDEX IX_ContractPremium_CustomerSSN ON ContractPremium(CustomerSSN);

-- Invoice table with partitioning
CREATE TABLE Invoice (
    InvoiceNumber VARCHAR(20),
    InvoiceDate DATE,
    NoOutstandingInvoices INT DEFAULT 0,
    DueDate DATE,
    PaidDate DATE,
    InvoiceStatus VARCHAR(20),
    BillingPeriod VARCHAR(20),
    CustomerSSN CHAR(11) NOT NULL,
	BAcctNumber VARCHAR(50) NOT NULL,
    ContractNumber VARCHAR(50) NOT NULL,
    PRIMARY KEY (InvoiceNumber, InvoiceDate),
	FOREIGN KEY (BAcctNumber) REFERENCES BillingAccount(BAcctNumber),
    FOREIGN KEY (CustomerSSN) REFERENCES Customer(CustomerSSN),
    FOREIGN KEY (ContractNumber) REFERENCES Contract(ContractNumber)
) PARTITION BY RANGE (InvoiceDate);

-- Create partitions for Invoice
CREATE TABLE Invoice_p1 PARTITION OF Invoice FOR VALUES FROM ('2010-01-01') TO ('2015-01-01');
CREATE TABLE Invoice_p2 PARTITION OF Invoice FOR VALUES FROM ('2015-01-01') TO ('2020-01-01');
CREATE TABLE Invoice_p3 PARTITION OF Invoice FOR VALUES FROM ('2020-01-01') TO ('2025-01-01');
CREATE TABLE Invoice_p4 PARTITION OF Invoice FOR VALUES FROM ('2025-01-01') TO (MAXVALUE);

CREATE INDEX IX_Invoice_InvoiceDate ON Invoice(InvoiceDate);
CREATE INDEX IX_Invoice_BAcctNumber ON Invoice(BAcctNumber);
CREATE INDEX IX_Invoice_CustomerSSN ON Invoice(CustomerSSN);
CREATE INDEX IX_Invoice_ContractNumber ON Invoice(ContractNumber);

-- InvoiceDetail table with partitioning
CREATE TABLE InvoiceDetail (
    InvoiceNumber VARCHAR(20),
    InvoiceDate DATE NOT NULL,
    LineNumber INT,
    LineDescription TEXT,
    LineTotal DECIMAL(6, 2),
    PRIMARY KEY (InvoiceNumber, LineNumber),
    FOREIGN KEY (InvoiceNumber, InvoiceDate) REFERENCES Invoice(InvoiceNumber, InvoiceDate)
) PARTITION BY RANGE (LineNumber);

-- Create partitions for InvoiceDetail
CREATE TABLE InvoiceDetail_p1 PARTITION OF InvoiceDetail FOR VALUES FROM (MINVALUE) TO (20);
CREATE TABLE InvoiceDetail_p2 PARTITION OF InvoiceDetail FOR VALUES FROM (20) TO (60);
CREATE TABLE InvoiceDetail_p3 PARTITION OF InvoiceDetail FOR VALUES FROM (60) TO (100);
CREATE TABLE InvoiceDetail_p4 PARTITION OF InvoiceDetail FOR VALUES FROM (100) TO (MAXVALUE);

CREATE INDEX IX_InvoiceDetail_LineNumber ON InvoiceDetail(LineNumber);

-- Employee table
CREATE TABLE Employee (
    EmpID VARCHAR(20) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DOB DATE,
    Street VARCHAR(100),
    Role VARCHAR(50),
    HiringDate DATE,
    Salary DECIMAL(10, 2),
    Zip CHAR(5) NOT NULL,
    EmployeeType VARCHAR(50),
    FOREIGN KEY (Zip) REFERENCES PostalCode(Zip)
);

CREATE INDEX IX_Employee_Zip ON Employee(Zip);

-- State table
CREATE TABLE State (
    StateCode VARCHAR(20) PRIMARY KEY,
    StateName VARCHAR(50)
);

-- StateCoordinator table
CREATE TABLE StateCoordinator (
    CoordinatorID VARCHAR(20) PRIMARY KEY,
    StateCode VARCHAR(20) NOT NULL,
    FOREIGN KEY (CoordinatorID) REFERENCES Employee(EmpID),
    FOREIGN KEY (StateCode) REFERENCES State(StateCode)
);

CREATE INDEX IX_StateCoordinator_CoordinatorID ON StateCoordinator(CoordinatorID);
CREATE INDEX IX_StateCoordinator_StateCode ON StateCoordinator(StateCode);

-- Region table
CREATE TABLE Region (
    RegionCode VARCHAR(20) PRIMARY KEY,
    RegionName VARCHAR(50),
    StateCode VARCHAR(20) NOT NULL,
    FOREIGN KEY (StateCode) REFERENCES State(StateCode)
);

CREATE INDEX IX_Region_StateCode ON Region(StateCode);

-- RegionalCoordinator table
CREATE TABLE RegionalCoordinator (
    CoordinatorID VARCHAR(20) PRIMARY KEY,
    RegionCode VARCHAR(20) NOT NULL,
    FOREIGN KEY (CoordinatorID) REFERENCES Employee(EmpID),
    FOREIGN KEY (RegionCode) REFERENCES Region(RegionCode)
);

CREATE INDEX IX_RegionalCoordinator_CoordinatorID ON RegionalCoordinator(CoordinatorID);
CREATE INDEX IX_RegionalCoordinator_RegionCode ON RegionalCoordinator(RegionCode);

-- District table
CREATE TABLE District (
    DistrictCode VARCHAR(20) PRIMARY KEY,
    DistrictName VARCHAR(50),
    RegionCode VARCHAR(20) NOT NULL,
    GeoCode VARCHAR(10) NOT NULL,
    FOREIGN KEY (RegionCode) REFERENCES Region(RegionCode),
    FOREIGN KEY (GeoCode) REFERENCES Operation(GeoCode)
);

CREATE INDEX IX_District_RegionCode ON District(RegionCode);
CREATE INDEX IX_District_GeoCode ON District(GeoCode);

-- DistrictCoordinator table
CREATE TABLE DistrictCoordinator (
    CoordinatorID VARCHAR(20) PRIMARY KEY,
    DistrictCode VARCHAR(20) NOT NULL,
    FOREIGN KEY (CoordinatorID) REFERENCES Employee(EmpID),
    FOREIGN KEY (DistrictCode) REFERENCES District(DistrictCode)
);

CREATE INDEX IX_DistrictCoordinator_CoordinatorID ON DistrictCoordinator(CoordinatorID);
CREATE INDEX IX_DistrictCoordinator_DistrictCode ON DistrictCoordinator(DistrictCode);

-- Associate table
CREATE TABLE Associate (
    AssociateID VARCHAR(20) PRIMARY KEY,
    TenureDate DATE,
    FOREIGN KEY (AssociateID) REFERENCES Employee(EmpID)
);

CREATE INDEX IX_Associate_AssociateID ON Associate(AssociateID);

-- CollaborateWith table
CREATE TABLE CollaborateWith ( 
    ProspectID INT NOT NULL,
    AssociateID VARCHAR(20) NOT NULL,
    PRIMARY KEY (ProspectID, AssociateID),
    FOREIGN KEY (ProspectID) REFERENCES Prospect(ProspectID),
    FOREIGN KEY (AssociateID) REFERENCES Associate(AssociateID)
);

CREATE INDEX IX_CollaborateWith_ProspectID ON CollaborateWith(ProspectID);
CREATE INDEX IX_CollaborateWith_AssociateID ON CollaborateWith(AssociateID);

-- ReportsToDistrict table
CREATE TABLE ReportsToDistrict ( 
    DistrictDirectorID VARCHAR(20), 
    AssociateID VARCHAR(20) NOT NULL,
    PRIMARY KEY (DistrictDirectorID, AssociateID),
    FOREIGN KEY (DistrictDirectorID) REFERENCES DistrictCoordinator(CoordinatorID), 
    FOREIGN KEY (AssociateID) REFERENCES Associate(AssociateID)
);

CREATE INDEX IX_ReportsToDistrict_DistrictDirectorID ON ReportsToDistrict(DistrictDirectorID);
CREATE INDEX IX_ReportsToDistrict_AssociateID ON ReportsToDistrict(AssociateID);

-- ReportsToRegion table
CREATE TABLE ReportsToRegion ( 
    RegionDirectorID VARCHAR(20), 
    AssociateID VARCHAR(20) NOT NULL,
    PRIMARY KEY (RegionDirectorID, AssociateID),
    FOREIGN KEY (RegionDirectorID) REFERENCES RegionalCoordinator(CoordinatorID), 
    FOREIGN KEY (AssociateID) REFERENCES Associate(AssociateID)
);

CREATE INDEX IX_ReportsToRegion_RegionDirectorID ON ReportsToRegion(RegionDirectorID);
CREATE INDEX IX_ReportsToRegion_AssociateID ON ReportsToRegion(AssociateID);

-- ReportsToState table
CREATE TABLE ReportsToState ( 
    StateDirectorID VARCHAR(20), 
    AssociateID VARCHAR(20) NOT NULL,
    PRIMARY KEY (StateDirectorID, AssociateID),
    FOREIGN KEY (StateDirectorID) REFERENCES StateCoordinator(CoordinatorID), 
    FOREIGN KEY (AssociateID) REFERENCES Associate(AssociateID)
);

CREATE INDEX IX_ReportsToState_StateDirectorID ON ReportsToState(StateDirectorID);
CREATE INDEX IX_ReportsToState_AssociateID ON ReportsToState(AssociateID);

	
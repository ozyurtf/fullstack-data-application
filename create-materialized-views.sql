-- Materialized view of Invoice
CREATE MATERIALIZED VIEW LastInvoiceDetailsPerCustomer AS
SELECT 
    CustomerSSN,
    MAX(InvoiceDate) as LastInvoiceDate,
    DueDate,
    PaidDate,
    InvoiceStatus,
    NoOutstandingInvoices
FROM Invoice i1
WHERE InvoiceDate = (
    SELECT MAX(InvoiceDate)
    FROM Invoice i2
    WHERE i2.CustomerSSN = i1.CustomerSSN
)
GROUP BY 
    CustomerSSN,
    DueDate,
    PaidDate,
    InvoiceStatus,
    NoOutstandingInvoices
ORDER BY CustomerSSN;


-- Materialized view of Customer + Contract
CREATE MATERIALIZED VIEW CustomerContract AS  
	SELECT  
		Customer.customerssn,
		Customer.firstname, 
		Customer.lastname, 
		Customer.phone, 
		Customer.state,
		
		Contract.contractnumber,
	    Contract.contracttype,
	    Contract.effectivedate,
	    Contract.expirationdate,
	    Contract.renewaldate,
	    Contract.policyid,
		
		ContractPremium.premiumcode, 
		ContractPremium.premiumamount, 
		ContractPremium.premiumfrequency,
		
		ChronicDiseaseForecast.premiumamountincreaserate,
	
		ContractPremium.premiumamount + ContractPremium.premiumamount * ChronicDiseaseForecast.premiumamountincreaserate AS newpremiumamount
		
	FROM ContractPremium
	
	JOIN Contract 
	ON ContractPremium.contractnumber = Contract.contractnumber
	
	JOIN (SELECT * 
		  FROM Customer
		  JOIN PostalCode
		  ON Customer.Zip = PostalCode.Zip) AS Customer
		  
	ON ContractPremium.customerssn = Customer.customerssn
	
	JOIN ChronicDiseaseForecast
	ON Customer.state = ChronicDiseaseForecast.state
	
	ORDER BY Contract.customerssn, Contract.contractnumber;
import React, { useState, useEffect } from 'react';

const Icon = ({ d, viewBox = "0 0 24 24", style }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox={viewBox} fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={style}>
    <path d={d} />
  </svg>
);

const SearchIcon = (props) => (
  <Icon d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19ZM11 19L21 21L19 11" {...props} />
);

const UserIcon = (props) => (
  <Icon d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" {...props} />
);

const CreditCardIcon = (props) => (
  <Icon d="M1 10H23M3 4H21C22.1046 4 23 4.89543 23 6V18C23 19.1046 22.1046 20 21 20H3C1.89543 20 1 19.1046 1 18V6C1 4.89543 1.89543 4 3 4Z" {...props} />
);

const FileTextIcon = (props) => (
  <Icon d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8M14 2L20 8M14 2V8H20M16 13H8M16 17H8M10 9H8" {...props} />
);

const CustomerLookup = () => {
  const [customerssn, setCustomerssn] = useState('');
  const [customerInfo, setCustomerInfo] = useState(null);
  const [accountInfo, setAccountInfo] = useState(null);
  const [lastInvoiceDetailInfo, setLastInvoiceDetailInfo] = useState(null);
  const [customercontractInfo, setCustomerContractInfo] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    document.body.style.backgroundColor = '#f0f4f8';
    return () => {
      document.body.style.backgroundColor = '';
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setCustomerInfo(null);
    setAccountInfo(null);
    setLastInvoiceDetailInfo(null);
    setCustomerContractInfo(null);

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/customerssn/${customerssn}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCustomerInfo(data.customer);
      setAccountInfo(data.account);
      setLastInvoiceDetailInfo(data.lastinvoicedetailpercustomer);
      setCustomerContractInfo(data.customercontract);
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const InfoCard = ({ title, icon, data }) => {
    const hasRenewalDate = data['Renewal Date'] && data['Renewal Date'] !== 'None';

    return (
      <div style={styles.card}>
        <div style={styles.cardHeader}>
          {icon}
          <h2 style={styles.cardTitle}>{title}</h2>
        </div>
        <div style={styles.cardContent}>
          {Object.entries(data).map(([key, value]) => (
            <div key={key} style={styles.infoItem}>
              <span style={styles.label}>{key}:</span>
              <span 
                style={
                  key === 'Premium Amount after Renewal' 
                    ? {...styles.value, ...(hasRenewalDate ? styles.greenHighlight : styles.redHighlight)}
                    : styles.value
                }
              >
                {value}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  };


  return (
    <div style={styles.container}>
      <div style={styles.lookupBox}>
        <h1 style={styles.title}>Customer Lookup</h1>
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputWrapper}>
            <SearchIcon style={styles.searchIcon} />
            <input
              type="text"
              value={customerssn}
              onChange={(e) => setCustomerssn(e.target.value)}
              placeholder="Enter SSN (XXX-XX-XXXX)"
              pattern="\d{3}-\d{2}-\d{4}"
              required
              style={styles.input}
            />
          </div>
          <button 
            type="submit" 
            disabled={isLoading} 
            style={styles.button}
          >
            {isLoading ? 'Searching...' : 'Get Quote'}
          </button>
        </form>
      </div>
      {error && <p style={styles.error}>{error}</p>}
      
      <div style={styles.cardsContainer}>
        {customerInfo && (
          <InfoCard
            title="Customer Information"
            icon={<UserIcon style={styles.cardIcon} />}
            data={{
              Name: `${customerInfo.firstname} ${customerInfo.lastname}`,
              Email: customerInfo.emailaddress,
              Phone: customerInfo.phone,
            }}
          />
        )}

        {accountInfo && (
          <InfoCard
            title="Account Information"
            icon={<CreditCardIcon style={styles.cardIcon} />}
            data={{
              'Account Number': accountInfo.acctnumber,
              Status: accountInfo.activitystatus,
              'Status Date': accountInfo.activitystatusdate,
              'Inactive Months': `${accountInfo.nomonthsinactive} months`,
              'Established Date': accountInfo.accountestablisheddate,
            }}
          />
        )}

        {lastInvoiceDetailInfo && (
          <InfoCard
            title="Last Invoice Information"
            icon={<FileTextIcon style={styles.cardIcon} />}
            data={{
              'Invoice Date': lastInvoiceDetailInfo.lastinvoicedate,
              'Invoice Due Date': lastInvoiceDetailInfo.duedate,
              'Paid Date': lastInvoiceDetailInfo.paiddate,
              'Invoice Status': lastInvoiceDetailInfo.invoicestatus,
              'Outstanding Invoices': lastInvoiceDetailInfo.nooutstandinginvoices,
            }}
          />
        )}


        {customercontractInfo && (
          <InfoCard
            title="Contract Information"
            icon={<FileTextIcon style={styles.cardIcon} />}
            data={{
              'Contract Number': customercontractInfo.contractnumber,
              'Contract Type': customercontractInfo.contracttype,
              'Effective Date': customercontractInfo.effectivedate,
              'Expiration Date': customercontractInfo.expirationdate,
              'Renewal Date': customercontractInfo.renewaldate,
              'Policy ID': customercontractInfo.policyid, 
              'Premium Amount': '$' + customercontractInfo.premiumamount,
              'Premium Frequency': customercontractInfo.premiumfrequency,
              'Premium Amount after Renewal': '$' + customercontractInfo.newpremiumamount
            }}
          />
        )}  
      </div>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: "'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
    maxWidth: '800px',
    margin: '40px auto',
    padding: '30px',
  },
  lookupBox: {
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)',
    padding: '30px',
    marginBottom: '30px',
  },
  title: {
    color: '#2c3e50',
    marginTop: 0,
    marginBottom: '20px',
    fontSize: '32px',
    textAlign: 'center',
    fontWeight: '600',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '15px',
  },
  inputWrapper: {
    position: 'relative',
    width: '100%',
    maxWidth: '400px',
  },
  searchIcon: {
    position: 'absolute',
    left: '12px',
    top: '50%',
    transform: 'translateY(-50%)',
    color: '#95a5a6',
  },
  input: {
    width: '80%',
    padding: '12px 12px 12px 40px',
    fontSize: '16px',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    outline: 'none',
    transition: 'border-color 0.3s',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    color: '#000000',  
    '&::placeholder': {
      color: '#95a5a6',
      opacity: 1,
    }
  },
  button: {
    padding: '12px 24px',
    fontSize: '16px',
    backgroundColor: 'orange',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
    fontWeight: '600',
    width: '100%',
    maxWidth: '400px',
  },
  error: {
    color: '#e74c3c',
    marginBottom: '20px',
    textAlign: 'center',
    fontWeight: '500',
  },
  cardsContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    padding: '20px',
  },
  cardHeader: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '15px',
  },
  cardIcon: {
    marginRight: '10px',
    color: '#3498db',
  },
  cardTitle: {
    margin: 0,
    fontSize: '22px',
    color: '#2c3e50',
    fontWeight: '600',
  },
  cardContent: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
  },
  infoItem: {
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    fontWeight: '500',
    color: '#7f8c8d',
    marginBottom: '5px',
    fontSize: '14px',
  },
  value: {
    color: '#2c3e50',
    fontSize: '16px',
    fontWeight: '500',
  },

  greenHighlight: {
    backgroundColor: '#e6ffe6',
    border: '2px solid #4CAF50',
    borderRadius: '4px',
    padding: '2px 6px',
    display: 'inline-block',
  },
  redHighlight: {
    backgroundColor: '#ffe6e6',
    border: '2px solid #FF0000',
    borderRadius: '4px',
    padding: '2px 6px',
    display: 'inline-block',
  },
};

export default CustomerLookup;
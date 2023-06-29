import './App.css'; // Import the CSS file
import React, { useState } from 'react';
const API_BASE_URL = 'http://127.0.0.1:2929'; // Update with your backend URL

function App() {
  const [email, setEmail] = useState('');
  const [coinName, setCoinName] = useState('');
  const [priceChange, setPriceChange] = useState('');
  const [priceHistory, setPriceHistory] = useState([]);

  const handleSubscribe = async (e) => {
    e.preventDefault();

    const requestBody = {
      email: email,
      coinName: coinName,
      priceChange: parseFloat(priceChange)
    };

    try {
      const response = await fetch(`${API_BASE_URL}/subscribe/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestBody)
        });

      if (response.ok) {
        alert('Subscription successful!');
        setEmail('');
        setCoinName('');
        setPriceChange('');
      } else {
        alert('Failed to subscribe. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    }
  };

  const handleGetPriceHistory = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${API_BASE_URL}/price/?coin_name=${coinName}`);
      if (response.ok) {
        const priceHistory = await response.json();
        setPriceHistory(priceHistory);
      } else {
        alert('Failed to fetch price history. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    }
  };

  return (
    <div>
      <h1>Welcome to Peyk</h1>

      <form onSubmit={handleSubscribe}>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        /><br />

        <label htmlFor="coinName">Coin Name:</label>
        <input
          type="text"
          id="coinName"
          value={coinName}
          onChange={(e) => setCoinName(e.target.value)}
          required
        /><br />

        <label htmlFor="priceChange">Price Change:</label>
        <input
          type="number"
          id="priceChange"
          step="0.01"
          value={priceChange}
          onChange={(e) => setPriceChange(e.target.value)}
          required
        /><br />

        <button type="submit">Subscribe</button>
      </form>

      <h2>Price History</h2>

      <form onSubmit={handleGetPriceHistory}>
        <label htmlFor="coinNameInput">Coin Name:</label>
        <input
          type="text"
          id="coinNameInput"
          value={coinName}
          onChange={(e) => setCoinName(e.target.value)}
          required
        /><br />

        <button type="submit">Get Price History</button>
      </form>

      <div>
        {priceHistory.length === 0 ? (
          <p>No price history data available.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
              {priceHistory.map((record) => (
                <tr key={record.Id}>
                  <td>{record.Timestamp}</td>
                  <td>{record.Price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;

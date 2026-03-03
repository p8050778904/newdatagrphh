import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles } from 'lucide-react';
import SearchBar from './components/SearchBar';
import ChartRenderer from './components/ChartRenderer';
import './styles/App.css';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
    const [chartConfig, setChartConfig] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [lastUpdated, setLastUpdated] = useState('');

    const updateTimestamp = () => {
        const now = new Date();
        const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        setLastUpdated(`Today, ${time}`);
    };

    React.useEffect(() => {
        updateTimestamp();
    }, []);

    const handleSearch = async (query) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await axios.post(`${API_BASE_URL}/query`, { query });
            setChartConfig(response.data);
            updateTimestamp();
        } catch (err) {
            console.error('API Error:', err);
            setError(err.response?.data?.detail || 'Failed to process query. Please check if the backend is running.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-container">
            {/* Minimalist Navbar */}
            <nav className="navbar">
                <div className="nav-left">
                    <div className="logo-box">N</div>
                    <span className="nav-logo-text">Nova Analytics</span>
                </div>
            </nav>

            {/* Overview Header */}
            <section className="overview-section">
                <div className="overview-title">
                    <h1>Analytics Overview</h1>
                </div>
                <div className="update-status">
                    Last updated: {lastUpdated}
                </div>
            </section>

            {/* Search Section */}
            <SearchBar onSearch={handleSearch} isLoading={isLoading} />

            {error && <div className="error-message">{error}</div>}

            {/* Dashboard Content */}
            <main className="dashboard-grid">
                {chartConfig && <ChartRenderer chartConfig={chartConfig} />}

                {/* Secondary Chart (Mock for preview) */}
                {chartConfig && <ChartRenderer chartConfig={{ ...chartConfig, title: "Category Distribution", chart_type: "pie" }} />}

                {!chartConfig && !isLoading && !error && (
                    <div className="loading-container" style={{ gridColumn: '1 / -1' }}>
                        <Sparkles size={48} color="var(--primary)" style={{ opacity: 0.6, marginBottom: '1rem' }} />
                        <p>Ask a question to generate interactive analytics</p>
                    </div>
                )}

                {isLoading && (
                    <div className="loading-container" style={{ gridColumn: '1 / -1' }}>
                        <div className="spinner"></div>
                        <p style={{ marginTop: '1rem' }}>Analyzing query and fetching real-time data...</p>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;

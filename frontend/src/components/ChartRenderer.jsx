import React from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    PieChart, Pie, Cell,
    LineChart, Line
} from 'recharts';

const COLORS = ['#1b3358', '#2e4c7d', '#4566a0', '#6382c4', '#86a1e5', '#cbd5e1'];

const ChartRenderer = ({ chartConfig }) => {
    const { chart_type, x_field, y_field, title, data } = chartConfig;

    if (!data || data.length === 0) {
        return <div className="loading-container">No data available for this query.</div>;
    }

    const renderChart = () => {
        switch (chart_type) {
            case 'bar':
                return (
                    <BarChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                        <XAxis
                            dataKey={x_field}
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                            dy={10}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                        />
                        <Tooltip
                            cursor={{ fill: '#f1f5f9' }}
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Bar dataKey={y_field} fill="#1e3a8a" radius={[4, 4, 0, 0]} barSize={40} />
                    </BarChart>
                );
            case 'pie':
                return (
                    <PieChart>
                        <Pie
                            data={data}
                            dataKey={y_field}
                            nameKey={x_field}
                            cx="50%"
                            cy="50%"
                            innerRadius={70}
                            outerRadius={100}
                            paddingAngle={5}
                        >
                            {data.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                        </Pie>
                        <Tooltip />
                        <Legend iconType="circle" />
                    </PieChart>
                );
            case 'line':
                return (
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                        <XAxis
                            dataKey={x_field}
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                        />
                        <Tooltip />
                        <Line type="monotone" dataKey={y_field} stroke="#1e3a8a" strokeWidth={3} dot={{ r: 4, fill: '#1e3a8a' }} activeDot={{ r: 6 }} />
                    </LineChart>
                );
            default:
                return <div>Unsupported chart type</div>;
        }
    };

    return (
        <div className="chart-card">
            <div className="chart-card-header">
                <div className="chart-info">
                    <h3>{title}</h3>
                    <p>Q3 FY2023 — All Regions</p>
                </div>
            </div>
            <div style={{ width: '100%', height: 320 }}>
                <ResponsiveContainer>{renderChart()}</ResponsiveContainer>
            </div>
        </div>
    );
};

export default ChartRenderer;

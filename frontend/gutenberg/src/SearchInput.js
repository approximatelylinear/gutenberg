import React, { useState } from 'react';

const SearchInput = () => {
    const [searchQuery, setSearchQuery] = useState('');

    const handleInputChange = (e) => {
        setSearchQuery(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:8000/search?query=' + encodeURIComponent(searchQuery) + '&index=' + encodeURIComponent('gutenberg_0'), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                console.log("Response headers:", response.headers);
                return response.json();
            })
            .then(data => {
                // Handle search results
                console.log(data);
            })
            .catch(error => console.error('Error:', error));
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSubmit(e);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="search-container">
            <input
                type="text"
                value={searchQuery}
                onChange={handleInputChange}
                onKeyPress={handleKeyPress}
                placeholder="Enter your search query"
                className="search-input"
            />
            <button type="submit" className="search-button">
                <i className="fas fa-search"></i>
            </button>
        </form>
    );
};

export default SearchInput;

import React from 'react';

const SearchInput = ({ searchQuery, handleSearch, handleInputChange }) => {

    const handleSubmit = (e) => {
        e.preventDefault();
        handleSearch(searchQuery);
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

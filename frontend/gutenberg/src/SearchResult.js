import React, { useState } from 'react';

const SearchResult = ({ title, content, author }) => {
    const [expanded, setExpanded] = useState(false);

    const handleContentClick = () => {
        setExpanded(!expanded);
    };

    return (
        <div className="search-result">
            <h3 onClick={handleContentClick}>{title}</h3>
            <p><em>Author: {author}</em></p>
            {/* <p>{content}</p> */}
            <p><em>Content: </em>{expanded ? `${content.substr(0, 1000)}` : `${content.substr(0, 100)}${content.length > 100 ? '...' : ''}`}</p>

        </div>
    );
};

export default SearchResult;

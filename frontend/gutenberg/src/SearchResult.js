import React, { useState } from 'react';


const SearchExplanation = ({ score, terms }) => {
    return (
        <div className="explanation">
            <hline />
            <span>Score: {score}</span>
            {terms.map((result, index) => (
                <span key={index}>
                    <span style={{ fontSize: 'small' }}>{result.field}:</span>
                    <span style={{ color: `rgba(0, 0, 0, ${Math.max(.25, result.weight)})` }}>{` ${result.term} (${result.weight})`}</span>
                </span>
            ))
            }
            <hline />
        </div>
    );
};


const SearchResult = ({ title, content, author, explanation, score }) => {
    const [expanded, setExpanded] = useState(false);

    const handleContentClick = () => {
        setExpanded(!expanded);
    };

    return (
        <div className="search-result">
            <h3 onClick={handleContentClick}>{title}</h3>
            <p><em>Author: {author}</em></p>
            <p><em>Content: </em>{expanded ? `${content.substr(0, 1000)}` : `${content.substr(0, 100)}${content.length > 100 ? '...' : ''}`}</p>
            {explanation && <SearchExplanation score={score} terms={explanation} />}
        </div>
    );
};

export default SearchResult;

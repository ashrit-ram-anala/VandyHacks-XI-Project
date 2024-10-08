import React from 'react'
import axios from 'axios'
import { useState } from "react";
import "./Search.css"

function Search() {
    const [searchQuery, setSearchQuery] = useState("")

    const handleChange = (event) => {
        setSearchQuery(event.target.value);
    }

    const handleSubmit = async (e) => {
        event.preventDefault()
        console.log(searchQuery)
        try {
            const response = await axios.post('http://localhost:5000/submit', {
                text: searchQuery,
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error submitting the form:', error);
        }

        // api stuff here i guess?
    }
    
    return (
    <>
        <h1 className="header">Stocks and Stuff</h1>
        <form onSubmit={handleSubmit}>
            <label className="tkr">Enter TKR here:</label>
            <input 
            type="text" 
            placeholder="Ex. AAPL, AMZN..." 
            value={searchQuery}
            onChange={handleChange}
            />
            <button type="submit">Search</button>
        </form>


    </>
  )
}

export default Search
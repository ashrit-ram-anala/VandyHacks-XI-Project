import React from 'react'
import axios from 'axios'
import { useState } from "react";
import "./Search.css"

function Search() {
    const [searchQuery, setSearchQuery] = useState("")

    const handleChange = (event) => {
        setSearchQuery(event.target.value); 
    }

    const handleSubmit = (event) => {
        event.preventDefault()
        console.log(searchQuery)

        // api stuff here i guess?
    }
    
    return (
    <>
        <h1 className="header">hello?</h1>
        <form onSubmit={handleSubmit}>
            <label className="tkr">Enter TKR here: </label>
            <br></br>
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
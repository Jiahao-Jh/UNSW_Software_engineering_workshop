import React, { useState } from "react";
import GetAttractions from "./GetAttractions";
import { Nav, Navbar, Container, NavDropdown, NavLink } from "react-bootstrap";

import "./att.css";

function Search() {
  let [data, setData] = useState(null);
  let [print, setPrint] = useState(false);

  function getData(val) {
    setData(val.target.value);
    setPrint(false);
  }
  // style={{ backgroundImage: `url(${background})`, backgroundRepeat: 'no-repeat', backgroundPosition: 'right',  }}
  return (
    <div
      class="container-md"
      className="contin"
      style={{
        backgroundColor: "#3e3e58",
      }}
    >
      <div
        className="background-filled"
        style={{
          backgroundColor: "#3e3e58",
        }}
      >
        {print ? (
          <h1 className="inooup_city">{data}</h1>
        ) : (
          <h1 className="inooup_city">Input the City you interested</h1>
        )}
        
        <p className="commit_lane">
            You can search for City or search by your categories, with input format
          "city,type,type,type"
        </p>

        <p>
        some of the popular options: museums, art_galleries, zoos, casino, beaches, sport, bars
        </p>

        <a className="commit_lane_last" href={`https://opentripmap.io/catalog`}>
          here is all categories you can choose
        </a>


        <div className="background">
          <input className="input" type="text" onChange={getData}></input>
        </div>

        <button
          type="button"
          className="button"
          onClick={() => setPrint(true)}
          style={{
            backgroundColor: "#989898",
          }}
        >
          Start Searching
        </button>


        {
          print && data !== "" &&
          <div>
            <GetAttractions
              className="green_button"
              city={data}
              print={print}
            ></GetAttractions>
          </div>
        }




      </div>
    </div>
  );
}

export default Search;

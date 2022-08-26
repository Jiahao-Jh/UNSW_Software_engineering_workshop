import React, { Component } from "react";
import "./att.css"

class GetAttractions extends Component {
  constructor(props) {
    super(props);
    this.state = {
      city: "",
      attractions_list: [],
      attractions_isLoaded: false,
      
    };
  }

  componentDidMount() {
    const apiKey = "5ae2e3f221c38a28845f05b67a7b7b8de99168bb00a108bc52c750dc";
      let city = "Sydney";


      if (this.props.print) {
        city = this.props.city;
      }

      if (city.split(",").length != 1){
        let type_1 = ""
        let type_2 = ""
        let type_3 = ""
        
        let i = 1
        while (i < city.split(",").length) {
          
          if (i == 1){
            type_1 = city.split(",")[i]
          } else if (i == 2) {
            type_2 = city.split(",")[i]
          } else if (i == 3) {
            type_3 = city.split(",")[i]
          }
          i += 1
        }
  
        this.setState({
          city:city.split(",")[0]
        });
        var city_API =
        "https://api.opentripmap.com/0.1/en/places/geoname?name=" +
        city.split(",")[0] +
        "&apikey=" +
        apiKey;

        console.log(city_API);
        const con_api = fetch(city_API).then((response) => response.json());

        if (type_2 === "") {
          con_api
          .then((cityInfo) => {
            // We can now store account info state on this component
            return fetch(
              // `https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon=${cityInfo.lon}&lat=${cityInfo.lat}&kinds=${type_1}&format=json&limit=15&apikey=${apiKey}`
              `https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon=${cityInfo.lon}&lat=${cityInfo.lat}&kinds=${type_1}&format=json&apikey=${apiKey}`

              );                                                                                                                                              
          })                                                                                                                                          

          .then((res) => res.json())
          .then((transactions) => {
            this.setState({
              attractions_isLoaded: true,
              attractions_list: transactions,
              x_ids: transactions.xid,
            });
          })
          .catch((reqErr) => console.error(reqErr));
        } else if (type_3 === "") {
            con_api
            .then((cityInfo) => {
              // We can now store account info state on this component
              return fetch(
                // `https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon=${cityInfo.lon}&lat=${cityInfo.lat}&kinds=${type_1}%2C${type_2}&format=json&limit=15&apikey=${apiKey}`
                `https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon=${cityInfo.lon}&lat=${cityInfo.lat}&kinds=${type_1}%2C${type_2}&format=json&apikey=${apiKey}`
   
                );                                                                                                                                              
            })                                                                                                                                          

            .then((res) => res.json())
            .then((transactions) => {
              this.setState({
                attractions_isLoaded: true,
                attractions_list: transactions,
                x_ids: transactions.xid,
              });
            })
            .catch((reqErr) => console.error(reqErr));


        } else {
          con_api
          .then((cityInfo) => {
            // We can now store account info state on this component
            return fetch(
              // `https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon=${cityInfo.lon}&lat=${cityInfo.lat}&kinds=${type_1}%2C${type_2}%2C${type_3}&format=json&limit=15&apikey=${apiKey}`
              `https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon=${cityInfo.lon}&lat=${cityInfo.lat}&kinds=${type_1}%2C${type_2}%2C${type_3}&format=json&apikey=${apiKey}`

              );                                                                                                                                              
          })                                                                                                                                          

          .then((res) => res.json())
          .then((transactions) => {
            this.setState({
              attractions_isLoaded: true,
              attractions_list: transactions,
              x_ids: transactions.xid,
            });
          })
          .catch((reqErr) => console.error(reqErr));
        }
        
      } else {


        this.setState({
          city:city
        });
        var city_API =
          "https://api.opentripmap.com/0.1/en/places/geoname?name=" +
          city +
          "&apikey=" +
          apiKey;
  
        console.log(city_API);
        const con_api = fetch(city_API).then((response) => response.json());
  
        con_api
          .then((cityInfo) => {
            // We can now store account info state on this component
            return fetch(
              // `https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon=${cityInfo.lon}&lat=${cityInfo.lat}&kinds=casino%2Ctowers%2Cbeaches%2Cclimbing%2Csurfing&rate=3&format=json&limit=15&apikey=${apiKey}`
              `https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon=${cityInfo.lon}&lat=${cityInfo.lat}&kinds=casino%2Ctowers%2Cbeaches%2Cclimbing%2Csurfing&rate=3&format=json&apikey=${apiKey}`


              );                                                                                                                                              
          })                                                                                                                                          
  
          .then((res) => res.json())
          .then((transactions) => {
            this.setState({
              attractions_isLoaded: true,
              attractions_list: transactions,
              x_ids: transactions.xid,
            });
          })
          .catch((reqErr) => console.error(reqErr));
      }
  }

  render() {

    var {
      city,
      attractions_list,
      attractions_isLoaded,
      
    } = this.state;
    
    console.log(this.props, "props");
    console.log(attractions_list, "sad");

    return (
      <div>
        {/* <input type="text" onChange={(city) => (this.setState({ city }))}>input</input> */}

        {attractions_isLoaded ? (
            
            <table class="table">
            <thead>
              <tr>
                <th className="table_title" scope="col">Tourist Attractions from {city}</th>
                <th className="table_title" scope="col">Attraction Rate</th>
                <th className="table_title" scope="col">Kinds</th>
                <th className="table_title" scope="col">Wikipedia</th>
                <th className="table_title" scope="col">Google Map</th>

              </tr>
            </thead>
            <tbody>

              {attractions_list.sort((a,b)=> a.rate > b.rate ? -1 : 1).slice(0, 15).map((attraction) => (
                

                <tr>

                  <th className="table_word" scope="row">{attraction.name}</th>
                  <td className="table_word">{attraction.rate}</td>
                  <td className="table_word">
                    {attraction.kinds.split(",")[0]}, {attraction.kinds.split(",")[1]}
                  </td>
                  <td className="table_word">
                    {/* <a target="_blank" href={`https://www.wikidata.org/wiki/${attraction.wikidata}`}>Wikipedia</a> */}
                    <a className="link" href={`https://en.wikipedia.org/wiki/${attraction.name}`}>Wikipedia</a>
                  </td>
                  <td className="table_word">
                    <a className="link" href={`https://maps.google.com/?q=${attraction.point.lat},${attraction.point.lon}`}>Google Map</a>
                  </td>


                </tr>
              



              ))}
            </tbody>
          </table>
        ) 
        
        : <p>Loading...</p>}
      </div>
    );
  }
}

export default GetAttractions;


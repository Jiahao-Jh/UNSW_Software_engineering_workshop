import React, { useEffect, useState } from "react";
import { scaleLinear } from "d3-scale";
import {
	ComposableMap,
	Geographies,
	Geography,
	Sphere,
	Graticule,
  ZoomableGroup,
} from "react-simple-maps";
import ReactTooltip from "react-tooltip";
import { Box, Slider, Container } from '@mui/material';
import loader from '../images/loader.gif'

const geoUrl =
  "https://raw.githubusercontent.com/zcreativelabs/react-simple-maps/master/topojson-maps/world-110m.json";


const StringencyMap = () => {
	const [content, setTooltipContent ] = useState("");

  const max_date="2022-04-10"
  const min_date="2020-01-21"

  const max = new Date("2022-04-10").getTime();
  const min = new Date("2020-01-21").getTime();

  const [value,  setValue] = useState(max);

  const [tmp_first, setTmp_first ] = useState({});
	var [tmp, setTmp ] = useState({"isLoad": false,});


	const current = new Date();
	//const date = current.getFullYear()+'-'+String(current.getMonth() + 1) + '-' +String(current.getDate())
  const api_link_first = 'https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/2022-03-21/'+ max_date
	const api_link = 'https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/2020-01-21/'+ max_date

  const step = 86400000;

  const marks = [
    {
      value: min,
      label: min_date,
    },
    {
      value: max,
      label: max_date,
    }
  ]
  function apiStyleDate(value) {
    let d = new Date(value);
    var mm = d.getMonth() + 1;
    if (mm <= 9){
      mm = '0' + mm 
    }
    var dd = d.getDate();
    if (dd <= 9){
      dd = '0' + dd 
    }
    var yy = d.getFullYear();
    var res = yy + '-' + mm + '-' + dd;
    return res;
  };

  function tooltipChangeHandler(value) {
    let custom = { year: "numeric", month: "short", day: "numeric" };
    let q = new Date(value).toLocaleDateString("en-us", custom);
    return q;
  };

	useEffect(() => {
		fetch(api_link_first)
			.then(response  => response.json())
			.then(
				result => setTmp({...result, isLoad: false})
			)
    fetch(api_link)
			.then(response  => response.json())
			.then(
				result => setTmp({...result, isLoad: true}),
        
			)
	}, []);
  
  console.log(tmp)
  console.log(tmp["isLoad"])

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const colorScale = scaleLinear()
	.domain([0.0, 100])
	.range(["#ffe7e3", "#ad1800"]);


  if (value <= new Date("2022-03-21").getTime() && !tmp["isLoad"]){
    return <img className='loader' src={loader} alt="loader" />;
  }

  return (
		<div data-tip="" data-for="Tip"    
      // style={{
      //     position: 'absolute', 
      //     left: '50%', 
      //     top: '50%',
      //     transform: 'translate(-50%, -50%)'
      // }}
      >

        <Container maxWidth="xl" >
          <h3 
          style={{
            marginBottom: "-5px",
            position: "relative",
            top: "30px"
          }}
          >
            COVID-19 Stringency Index, {tooltipChangeHandler(value)}
          </h3>
          <p
          style={{
            marginBottom: "-5px",
            height:"0px",
            position: "relative",
            top: "45px",
          }}
          >
            The stringency index is a composite measure based on nine response indicators including school closures, workplace closures, and travel bans, rescaled to a value from 0 to 100 (100 = strictest).
          </p>
          <p
          style={{
            marginBottom: "100px",
            height:"0px",
            position: "relative",
            top: "67px",
          }}
          >
            If policies vary at the subnational level, the index shows the response level of the strictest subregion.
          </p>
          <ComposableMap
            projectionConfig={{
              rotate: [-10, 0, 0],
              scale: 135
            }}
            width={800}
            height={400}
            // style={{
            //   position: "relative",
            //   top: "90px",
            //   }}
			    >
            <ZoomableGroup zoom={1}>
            <Sphere stroke="#E4E5E6" strokeWidth={0.5} />
            <Graticule stroke="#E4E5E6" strokeWidth={0.5} />
            { "data" in tmp && (
              <Geographies geography={geoUrl}>
                {({ geographies }) =>
                  geographies.map((geo) => {
                    var d = 0
                    if (geo.properties.ISO_A3 in tmp["data"][apiStyleDate(value)]){
                      d = tmp["data"][apiStyleDate(value)][geo.properties.ISO_A3]["stringency"]
                    }
                    
                    
                    return (

                      <Geography
                        key={geo.rsmKey}
                        geography={geo}
                        
                        fill={d ? colorScale(d) : "#F5F4F6"}
                        stroke="#808080"
                        strokeWidth =".1px"
                        onMouseEnter={() => {
                          if (geo.properties.ISO_A3 in tmp["data"][apiStyleDate(value)] && tmp["data"][apiStyleDate(value)][geo.properties.ISO_A3]["stringency"] != null){
                            var result = "Stringency Index: "+tmp["data"][apiStyleDate(value)][geo.properties.ISO_A3]["stringency"]
                          } else{
                            
                            var result = "No data"
                          }
                          setTooltipContent(result);
                        }}
                        onMouseLeave={() => {
                          setTooltipContent("");
                        }}
                        style={{
                          default: { outline: "none" },
                          hover: {
                          fill: "#150",
                          outline: "none"
                          },
                          pressed: {
                          fill: "#150",
                          outline: "none"
                          },
                        }}
                      />
                    );
                  })
                }
              </Geographies>
              
            )}
            </ZoomableGroup>
			    </ComposableMap>   
          <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          // sx={{ width: 1000 }}
        >
          <Slider
          value={value}
          min={min} 
          max={max} 
          size="medium"
          step={step} 
          valueLabelFormat={tooltipChangeHandler}
          onChange={handleChange}
          valueLabelDisplay="auto"
          //getAriaValueText={tooltipChangeHandler}
          marks={marks}
        />
          </Box>    
        </Container>

			<ReactTooltip id="Tip" >{content}</ReactTooltip>


		</div>
	);
};

export default StringencyMap;

import React, { useEffect, useState, memo } from "react";
import { scaleLinear } from "d3-scale";
import {
	ComposableMap,
	Geographies,
	Geography,
	Sphere,
	Graticule,
	ZoomableGroup
} from "react-simple-maps";
import { Container, ButtonGroup, ToggleButton, Modal, Button, Table } from "react-bootstrap";
import { Colorscale } from 'react-colorscales';
import ReactTooltip from "react-tooltip";
import './MapChart.scss'

const geoUrl = "/world-110m.json";

const colorScale = scaleLinear()
	.domain([0.0, 100])
	.range(["#ffedea", "#ff5233"]);

var i = 0;
var cs = [];
while (i <= 100) {
	cs.push(colorScale(i));
	i += 1;
}

const MapChart = () => {
	const [covid, setCovid] = useState([]);
	const [content, setTooltipContent] = useState("");
	const [radioValue, setRadioValue] = useState('1');
	const [showToday, setShowToday] = useState(true);
	const [label, setLabel] = useState("100,000");
	const [show, setShow] = useState(false);
	const [country, setCountry] = useState('');
	const [provincesData, setProvincesData] = useState([]);

	const handleClose = () => {
		setProvincesData([]);
		setShow(false);
	}
	const handleShow = () => setShow(true);

	function fetchCountryData(name) {
		fetch(`https://disease.sh/v3/covid-19/historical/${name}?lastdays=1`)
			.then(res => res.json())
			.then(result => {
				const provinces = result.province;
				const parameter = provinces.join(",");
				fetch(`https://disease.sh/v3/covid-19/historical/${name}/${parameter}?lastdays=1`)
					.then(r => r.json())
					.then(data => {
						var arr = [];
						for (let i = 0; i < data.length; i++) {
							arr.push({
								"province": data[i].province,
								"cases": Object.values(data[i].timeline.cases)[0],
								"deaths": Object.values(data[i].timeline.deaths)[0],
								"recovered": Object.values(data[i].timeline.recovered)[0],
							});
						}
						setProvincesData(arr);
					});
			});
	}

	const radios = [
		{ name: 'Today Cases', value: '1' },
		{ name: 'Total Cases', value: '2' }
	]

	useEffect(() => {
		fetch('https://disease.sh/v3/covid-19/countries')
			.then(res => res.json())
			.then(
				result => {
					setCovid(result);
				}
			)
	}, []);

	return (
		<div data-tip="" data-for="Tip" >
			<h3 className="covid-title">More about Covid-19</h3>
			<Container className="world-map">
				<ButtonGroup className="mb-2">
					{radios.map((radio, idx) => (
						<ToggleButton
							key={idx}
							id={`radio-${idx}`}
							type="radio"
							variant="secondary"
							name="radio"
							value={radio.value}
							checked={radioValue === radio.value}
							onChange={(e) => {
								setRadioValue(e.currentTarget.value);
								if (showToday) {
									setLabel("100,000,000")
								} else {
									setLabel("100,000")
								}
								setShowToday(!showToday);
							}}
						>
							{radio.name}
						</ToggleButton>
					))}
				</ButtonGroup>
				<ComposableMap
					projectionConfig={{
						rotate: [-10, 0, 0],
						scale: 140
					}}
				>
					<ZoomableGroup zoom={1}>
						<Sphere stroke="#E4E5E6" strokeWidth={0.5} />
						<Graticule stroke="#E4E5E6" strokeWidth={0.5} />
						{covid.length > 0 && (
							<Geographies geography={geoUrl}>
								{({ geographies }) =>
									geographies.map((geo) => {
										const d = covid.filter(
											function (el) {
												return el.countryInfo.iso3 === geo.properties.ISO_A3
											}
										);
										return (
											<Geography
												key={geo.rsmKey}
												geography={geo}
												fill={
													showToday ? (d[0] ? colorScale(d[0]["todayCases"] / 1000) : "#F5F4F6") : (d[0] ? colorScale(d[0]["cases"] / 1000000) : "#F5F4F6")
												}
												stroke="#808080"
												strokeWidth=".1px"
												onClick={() => {
													setCountry(geo.properties.NAME);
													fetchCountryData(geo.properties.ISO_A3);
													handleShow();
												}}
												onMouseEnter={() => {
													const NAME = geo.properties.ISO_A3;
													const cases = covid.find(country => country.countryInfo.iso3 === NAME);
													if (cases && showToday) {
														setTooltipContent(cases.country + ": " + cases.todayCases);
													} else if (cases && !showToday) {
														setTooltipContent(cases.country + ": " + cases.cases);
													} else {
														setTooltipContent(geo.properties.NAME + ": No data")
													}
												}}
												onMouseLeave={() => {
													setTooltipContent("");
												}}
												style={{
													default: { outline: "none" },
													hover: {
														stroke: "black",
														strokeWidth: 0.5,
														outline: "none",
													},
													pressed: { outline: "none" },
												}}

											/>
										);
									})
								}
							</Geographies>
						)}
					</ZoomableGroup>
				</ComposableMap>
				<ReactTooltip id="Tip" >{content}</ReactTooltip>
				<div className="color-scale">
					<Colorscale
						colorscale={cs}
						onClick={() => { }}
						width={150}
					/>
					<p className="label-left">0</p>
					<p className="label-right">&gt; {label}</p>
				</div>
				<div className="clear"></div>
				<Modal show={show} onHide={handleClose}>
					<Modal.Header closeButton>
						<Modal.Title>{country} Statistic</Modal.Title>
					</Modal.Header>
					<Modal.Body>
						<Table striped bordered hover>
							<thead>
								<tr>
									<th>State/Province</th>
									<th>Cases</th>
									<th>Deaths</th>
									<th>Recovered</th>
								</tr>
							</thead>
							<tbody>
								{provincesData.map((obj) => {
									return <tr key={obj.province}>
										<td>{obj.province}</td>
										<td>{obj.cases}</td>
										<td>{obj.deaths}</td>
										<td>{obj.recovered}</td>
									</tr>
								})}
							</tbody>
						</Table>
					</Modal.Body>
					<Modal.Footer>
						<Button variant="secondary" onClick={handleClose}>
							Close
						</Button>
					</Modal.Footer>
				</Modal>
			</Container>
		</div>
	);
};

export default MapChart;

import React from 'react';
import { Line } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";
import { Chart, registerables } from 'chart.js';
import { Container, Form, Table } from 'react-bootstrap'
import './ChartGraph.scss'
Chart.register(...registerables);




class ChartGraph extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			error: null,
			isLoaded: false,
			dataLine: {
				labels: [],
				datasets: []
			},
			user_date: '-',
			cases: '-',
			deaths: '-',
			recovered: '-',
			r: null
		}
	}

	change_user_date(event) {
		var user_date = event.target.value;
		console.log(user_date);
		if (user_date === "") {
			this.setState(prevState => ({
				...prevState,
				user_date: "-",
				cases: "-",
				deaths: "-",
				recovered: "-"
			}));
			return;
		}
		user_date = new Date(user_date)
		var dd = String(user_date.getDate()).padStart(2, '0');
		dd = dd.replace(/^0+/, '');
		var mm = String(user_date.getMonth() + 1).padStart(2, '0');
		mm = mm.replace(/^0+/, '')
		var yyyy = user_date.getFullYear().toString().substr(-2);
		user_date = mm + '/' + dd + '/' + yyyy;

		this.setState(prevState => ({
			...prevState,
			user_date: user_date,
			cases: prevState.r.cases[user_date],
			deaths: prevState.r.deaths[user_date],
			recovered: prevState.r.recovered[user_date]
		}));
	}

	componentDidMount() {
		fetch("https://disease.sh/v3/covid-19/historical/all?lastdays=all&allowNull=true")
			.then(res => res.json())
			.then(
				(result) => {
					this.setState(prevState => ({
						isLoaded: true,
						r: result,
						dataLine: {
							...prevState,
							labels: Object.keys(result.cases),
							datasets: [
								{
									label: "cases",
									fill: false,
									lineTension: 0.3,
									backgroundColor: "rgba(225, 204,230, .3)",
									borderColor: "rgb(205, 130, 158)",
									data: Object.values(result.cases)
								},
								{
									label: "deaths",
									fill: false,
									backgroundColor: "rgba(184, 185, 210, .3)",
									borderColor: "rgb(35, 26, 136)",
									data: Object.values(result.deaths)
								},
								{
									label: "recovered",
									fill: false,
									backgroundColor: "rgba(75,192,192,0.2)",
									borderColor: "rgba(75,192,192,1)",
									data: Object.values(result.recovered)
								}
							]
						}
					}))
				},
				(error) => {
					this.setState({
						isLoaded: false
					})
				}
			);
	}

	render() {
		return <div>
			<h3 className='page-title'>Covid-19 Statistic</h3>
			<Container>
				<div className="container">
					<div className="border" />
					<span className="content"></span>
					<div className="border" />
				</div>
				<MDBContainer>
					<Line data={this.state.dataLine} options={{ responsive: true }} />
				</MDBContainer>
				<Form.Label htmlFor="date-label">Search Date</Form.Label>
				<Form.Control
					type="date"
					id="inputDate"
					onChange={(e) => this.change_user_date(e)}
					className="w-25"
				/>
				<Form.Text id="date-form" muted>
					You can check a specific date
				</Form.Text>
				<Table striped bordered hover size='lg'>
					<thead>
						<tr>
							<th>date</th>
							<th>Confirmed Cases</th>
							<th>Deaths</th>
							<th>Recovered</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>{this.state.user_date}</td>
							<td>{this.state.cases}</td>
							<td>{this.state.deaths}</td>
							<td>{this.state.recovered}</td>
						</tr>
					</tbody>
				</Table>
			</Container>
		</div>
	}
}

const ChartPropTypes = {
	// always use prop types!
};

ChartGraph.propTypes = ChartPropTypes;

export default ChartGraph;

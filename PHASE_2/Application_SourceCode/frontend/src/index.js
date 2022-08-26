import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import ChartGraph from './components/ChartGraph/ChartGraph';
import MapChart from './components/MapChart';
import NavigationBar from './components/NavigationBar/NavigationBar';
import StringencyMap from './components/StringencyMap/StringencyMap';
import Article from './components/ArticleSearch/Article'
import IntroComponent from './components/IntroComponent/IntroComponent';
import BottomBar from './components/BottomBar/BottomBar';
import TouristAttractions from "./components/TouristAttraction/SearchBar";

ReactDOM.render(
	<React.StrictMode>
		<NavigationBar />
		<BrowserRouter>
			<Switch>
				<Route exact path="/" >
					<IntroComponent />
					<MapChart />
				</Route>

				<Route path="/article-searching">
					<Article />
				</Route>

				<Route path="/tourist-attractions">
					<TouristAttractions />
				</Route>
				
				<Route path="/covid-statistic">
					<ChartGraph />
				</Route>
				
				<Route path="/covid-stringency-Map">
					<StringencyMap />
					<MapChart />
				</Route>

			</Switch>
		</BrowserRouter>
		<BottomBar />
	</React.StrictMode>,
	document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

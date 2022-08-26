import React from 'react';
import { Nav, Navbar, Container, NavDropdown, NavLink } from 'react-bootstrap'
import PropTypes from 'prop-types';
import styles from './NavigationBar.scss';

const NavigationBar = props => (
	<div>
		<Navbar bg="light" expand="lg">
			<Container fluid>
				<Navbar.Brand href="/">
					<img src="/18.svg" />
					DiseaseTFA
				</Navbar.Brand>
				<Navbar.Toggle aria-controls="navbarScroll" />
				<Navbar.Collapse id="navbarScroll">
					<Nav
						className="me-auto my-2 my-lg-0"
						style={{ maxHeight: '100px' }}
						navbarScroll
					>
						<NavLink href='/article-searching' >Article Searching</NavLink>
						
						<NavLink href='/tourist-attractions' >Tourist Attractions</NavLink>

						<NavDropdown title="Covid" id="navbarScrollingDropdown">
							<NavDropdown.Item href="/covid-statistic">Covid Statistic</NavDropdown.Item>
							<NavDropdown.Item href="/covid-stringency-Map">Covid Stringency Map</NavDropdown.Item>
						</NavDropdown>
						
					</Nav>
				</Navbar.Collapse>
			</Container>
		</Navbar>
	</div>
);

// todo: Unless you need to use lifecycle methods or local state,
// write your component in functional form as above and delete
// this section. 
// class Nav extends React.Component {
//   render() {
//     return <div>This is a component called Nav.</div>;
//   }
// }

const NavPropTypes = {
	// always use prop types!
};

Nav.propTypes = NavPropTypes;

export default NavigationBar;

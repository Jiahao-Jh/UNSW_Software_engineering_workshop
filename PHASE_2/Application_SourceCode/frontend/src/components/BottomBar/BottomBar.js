import React from 'react';
import PropTypes from 'prop-types';
import styles from './BottomBar.scss';



class BottomBar extends React.Component {
  render() {
    return <div className='bottom-bar'>
		<div className='brand'>
			<h4>
				<img src='/18.svg' />
				DiseaseTFA
			</h4>
		</div>
		<div className="about-bar">
			<h4>ABOUT</h4>
			<a href='https://www.unsw.edu.au'>UNSW</a>
			<a href='https://github.com/JackWhoooo/SENG3011_GroupName'>SENG3011</a>
			<a href='https://github.com/JackWhoooo/SENG3011_GroupName'>GroupName</a>
		</div>
	</div>;
  }
}

const BottomBarPropTypes = {
	// always use prop types!
};

BottomBar.propTypes = BottomBarPropTypes;

export default BottomBar;

import React from 'react';
import PropTypes from 'prop-types';
import styles from './IntroComponent.scss';
import { Button } from 'react-bootstrap';

class IntroComponent extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return <div className='intro-page'>
			<img src="/homeimage.png" className='home-image'/>
			<div className='intro-content'>
				<h1>Plan a</h1>
				<h1>safe trip</h1>
				<h1>with DiseaseTFA</h1>
				<br></br>
				<h4>Find out more with Articles and Travel</h4>
				<Button className='intro-button' href='/article-searching'>Article</Button>
				<Button className='intro-button' href='/tourist-attractions'>Travel</Button>
			</div>
		</div>;
	}
}

const IntroComponentPropTypes = {
	// always use prop types!
};

IntroComponent.propTypes = IntroComponentPropTypes;

export default IntroComponent;

import React, {useState} from 'react';
import {Container} from "react-bootstrap";
import './Article.scss'
import axios, { Axios } from 'axios';
import loader from '../images/loader.gif'
import search from '../images/search.png'
import { Card, Button } from 'react-bootstrap';



function ReadMore({children = 100}) {

    const text = children;

    const [isShow, setIsShowLess] = useState(true)
    const result = isShow ? text.slice(0, 100) : text;

    function toggleIsShow() {
        setIsShowLess((!isShow));
    }

    return(
        <p>
            {result}
            <span className="btn btn-link" onClick={toggleIsShow}>
                {isShow ? "Read More" : "Read Less"}
            </span>
        </p>
    )

}

class ArticleSearch extends React.Component {

    /**
     * constructor
     *
     * @object  @props  parent props
     * @object  @state  component state
     */
    constructor(props) {

        super(props);

        this.state = {
            items: [],
            article1:[],
            article2:[],
            article3:[],
            article4:[],
            article5:[],
            article6:[],
            article7:[],
            article8:[],
            article9:[],
            article10:[],
            article11:[],
            isLoaded: false,
            isLoaded1: false,
            isLoaded2: false,
            isLoaded3: false,
            isLoaded4: false,
            isLoaded5: false,
            isLoaded6: false,
            isLoaded7: false,
            isLoaded8: false,
            isLoaded9: false,
            isLoaded10: false,
            isLoaded11: false,
            period_start: '',
            period_end: '',
            location: '',
            key_terms: '',
			results: {},
			loading: false,
			message: '',
        };
        this.cancel = '';
    }

    fetchSearchResults = ( period_start, period_end, location, key_terms ) => {
        var period = `{"start":"${period_start}","end":"${period_end}"}`;
        var keyterms = `["${key_terms}"]`;
        var axios = require('axios');

        var config_curl = {
            method: 'get',
            url: 'https://teamviral-api.herokuapp.com/api/v1/search',
            headers: { 
                'accept': 'application/json',
                'period_of_interest': period,
                'location': location,
                'key_terms': keyterms,
            },
          };

		if( this.cancel ) {
			this.cancel.cancel();
		}
        
		this.cancel = axios.CancelToken.source();

		axios( config_curl, {
			cancelToken: this.cancel.token
		} )
			.then( res => {
				this.setState( {
					results: res.data.articles,
					loading: false
				} )
                console.log(res.data.articles);
			} )
			.catch( error => {
				if ( axios.isCancel(error) || error ) {
					this.setState({
						loading: false,
						message: 'Failed to fetch the data. Please check the network'
					})
				}
                console.log(error);
			} )
	};

    handleOnInputChangePeriodStart = ( event ) => {
		const period_start = event.target.value;
		if ( ! period_start ) {
			this.setState( { period_start, results: {}, message: 'Please fill the period start'} );
		} else {
			this.setState( { period_start, loading: true, message: '' } );
		}
	};

    handleOnInputChangePeriodEnd = ( event ) => {
		const period_end = event.target.value;
		if ( ! period_end ) {
			this.setState( { period_end, results: {}, message: 'Please fill the period end'} );
		} else {
			this.setState( { period_end, loading: true, message: '' } );
		}
	};

    handleOnInputChangeLocation = ( event ) => {
		const location = event.target.value;
		if ( ! location ) {
			this.setState( { location, results: {}, message: 'Please fill the location'} );
		} else {
			this.setState( { location, loading: true, message: '' } );
		}
	};

    handleOnInputChangeKeyTerms = ( event ) => {
		const key_terms = event.target.value;
		if ( ! key_terms ) {
			this.setState( { key_terms, results: {}, message: 'Please fill the key terms'} );
		} else {
			this.setState( { key_terms, loading: true, message: '' } );
		}
	};

    renderSearchResults = () => {
		const { results } = this.state;

		if ( Object.keys( results ).length && results.length ) {
			return (
				<div className="results-container">
                    <div className="header2">Total Results: { results.length }</div>
					{ results.map( result => {
						return (
							<div key={ result.articleId } className="result-item">
                                <li className='headline' style={{fontWeight: 'bold'}}>
                                    {result.headline}   
                                </li>
                                <p className='headline2'>Published on {result.dateOfPublication}</p>
                                <Container className="mt-5 p-5 shadow rounded">
                                    <div style={{whiteSpace: "pre-wrap"}}>
                                        <ReadMore>
                                            {result.mainText}
                                        </ReadMore>     
                                    </div>
                                    <Card style={{ width: '18rem' }}>
                                        <Card.Body>
                                            <Card.Title style={{fontWeight: 'bold'}}>Reports Summary</Card.Title>
                                            { result.reports.map( report => {
                                                return (
                                                    <div key={ report.reportId } className="report-card">
                                                        
                                                        <Card.Title>Date: {report.eventDate.substring(0,10)} </Card.Title>
                                                            <Card.Subtitle className="mb-2 text-muted">Diseases</Card.Subtitle>
                                                            { report.diseases.map( disease => {
                                                                return (
                                                                    <Card.Text key={ disease } className="result-item">
                                                                        <li>{disease}</li>
                                                                    </Card.Text>
                                                                )
                                                            } ) }
                                                            <Card.Subtitle className="mb-2 text-muted">Locations</Card.Subtitle>
                                                            { report.locations.map( location => {
                                                                return (
                                                                    <Card.Text key={ location } className="result-item">
                                                                        <li>{location}</li>
                                                                    </Card.Text>
                                                                )
                                                            } ) }
                                                            <Card.Subtitle className="mb-2 text-muted">Syndromes</Card.Subtitle>
                                                            { report.syndromes.map( syndrome => {
                                                                return (
                                                                    <Card.Text key={ syndrome } className="result-item">
                                                                        <li>{syndrome}</li>
                                                                    </Card.Text>
                                                                )
                                                            } ) }
                                                       
                                                    </div>
                                                )
                                            } ) }
                                        </Card.Body>
                                    </Card>
                                </Container>
							</div>
						)
					} ) }

				</div>
			)
		} else if ( results.length == 0) {
            return (<h1>No Result Found. Please Check Your Input</h1>)
        }
	};

    /**
     * componentDidMount
     *
     * Fetch json array of objects from given url and update state.
     */
    componentDidMount() {
        
        fetch('https://teamviral-api.herokuapp.com/api/v1/articles/dump')
            .then(res => res.json())
            .then(json => {
                this.setState({
                    items: json,
                    isLoaded: true, 
                })
            
            fetch('https://teamviral-api.herokuapp.com/api/v1/articles/' + json.articles[0].articleId)
                .then(res => res.json())
                .then(json => {
                    this.setState({
                        article1: json,
                        isLoaded1: true,
                    })
                    console.log(json);
                }).catch((err) => {
                    console.log(err);
                })
            fetch('https://teamviral-api.herokuapp.com/api/v1/articles/' + json.articles[1].articleId)
                .then(res => res.json())
                .then(json => {
                    this.setState({
                        article2: json,
                        isLoaded2: true,
                    })
                    console.log(json);
                }).catch((err) => {
                    console.log(err);
                })
            fetch('https://teamviral-api.herokuapp.com/api/v1/articles/' + json.articles[2].articleId)
                .then(res => res.json())
                .then(json => {
                    this.setState({
                        article3: json,
                        isLoaded3: true,
                    })
                    console.log(json);
                }).catch((err) => {
                    console.log(err);
                })

            }).catch((err) => {
                console.log(err);
            });

        //const articleId = this.state.items.articles[0].articleId
        //a4fd819e-2f69-490e-b1f3-4b479e425c84
        

        
        
    };

    /**
     * render
     *
     * Render UI
     */
    render() {
        const { period_start, period_end, location, key_terms, results, message} = this.state;
        //waiting for fetching all articles
        const { isLoaded, items } = this.state;
        
        
        if (!isLoaded)
            return <img className='loader' src={loader} alt="loader" />;
        
        
        // waiting for fetching article1
        const { isLoaded3 } = this.state;
        const { article1, article2, article3, article4, article5, article6, article7, article8, article9, article10 } = this.state;

        if (!isLoaded3)
            return <img className='loader' src={loader} alt="loader" />;


        return (
            <div className="Article">
                <div className='search-bar' style={{ backgroundImage: `url(${search})`, backgroundRepeat: 'no-repeat', backgroundPosition: 'right', }}> 
                    <div className='background-filled' style={{ height: '10px'}}>  </div>
                    <div className="header1">
                            Please enter the following fields to find articles
                    </div>
                    {/*	Search Table*/}
                    <label className="search-label" htmlFor="search-input">
                        <div className='search-name'>Start Date</div>
                        <input className="search-period-start" 
                            type="text"
                            name="period_start"
                            value={ period_start }
                            id="search-input"
                            placeholder="e.g. 2009-09-23"
                            onChange={this.handleOnInputChangePeriodStart}
                        />
                        <div className='search-name'>End Date</div>
                        <input className="search-period-end" 
                            type="text"
                            name="period_end"
                            value={ period_end }
                            id="search-input"
                            placeholder="e.g. 2021-09-24"
                            onChange={this.handleOnInputChangePeriodEnd}
                        />
                        <div className='search-name'>Location</div>
                        <input className="search-location"
                            type="text"
                            name="location"
                            value={ location }
                            id="search-input"
                            placeholder="e.g. India"
                            onChange={this.handleOnInputChangeLocation}
                        />
                        <div className='search-name'>Key Terms</div>
                        <input className="search-key-terms"
                            type="text"
                            name="key_terms"
                            value={ key_terms }
                            id="search-input"
                            placeholder="e.g. nipah virus"
                            onChange={this.handleOnInputChangeKeyTerms}
                        />
                        <i className="fa fa-search search-icon" aria-hidden="true"/>
                    </label>
                    <div className='background-filled' style={{ height: '10px'}}> </div>
                    <Button className='search-button' onClick={() => this.fetchSearchResults(period_start, period_end, location, key_terms)}>
                    Search
                    </Button>   
                    {/*	Error Message*/}
                    {message && <p className="message">{ message }</p>}
                </div>
                    {(() => {
                        if (results.length === undefined) {
                            return (
                                <div style={{ backgroundColor: '#fafafa'}}>{/* Recommended Articles*/}
                                    <div className="header2">
                                        Recommended Articles of Outbreak
                                    </div>
                                    
                                    <li className='headline' style={{fontWeight: 'bold'}}>
                                        {items.articles[0].headline}   
                                    </li>   
                                    <p className='headline2'>Published on {items.articles[0].dateOfPublication}</p>
                                    <Container className="mt-5 p-5 shadow rounded">
                                        <div style={{whiteSpace: "pre-wrap"}}>
                                            <ReadMore>
                                                {article1.article.mainText}
                                            </ReadMore>     
                                        </div>
                                        <Card style={{ width: '18rem' }}>
                                            <Card.Body>
                                                <Card.Title style={{fontWeight: 'bold'}}>Reports Summary</Card.Title>
                                                { article1.article.reports.map( report => {
                                                    return (
                                                        <div key={ report.reportId } className="report-card">
                                                            
                                                            <Card.Title>Date: {report.eventDate.substring(0,10)} </Card.Title>
                                                                <Card.Subtitle className="mb-2 text-muted">Diseases</Card.Subtitle>
                                                                { report.diseases.map( disease => {
                                                                    return (
                                                                        <Card.Text key={ disease } className="result-item">
                                                                            <li>{disease}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                                <Card.Subtitle className="mb-2 text-muted">Locations</Card.Subtitle>
                                                                { report.locations.map( location => {
                                                                    return (
                                                                        <Card.Text key={ location } className="result-item">
                                                                            <li>{location}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                                <Card.Subtitle className="mb-2 text-muted">Syndromes</Card.Subtitle>
                                                                { report.syndromes.map( syndrome => {
                                                                    return (
                                                                        <Card.Text key={ syndrome } className="result-item">
                                                                            <li>{syndrome}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                        
                                                        </div>
                                                    )
                                                } ) }
                                            </Card.Body>
                                        </Card>
                                    </Container>


                                    <li className='headline' style={{fontWeight: 'bold'}}>
                                        {items.articles[1].headline}   
                                    </li>   
                                    <p className='headline2'>Published on {items.articles[1].dateOfPublication}</p>
                                    <Container className="mt-5 p-5 shadow rounded">
                                        <div style={{whiteSpace: "pre-wrap"}}>
                                            <ReadMore>
                                                {article2.article.mainText}
                                            </ReadMore>     
                                        </div>
                                        <Card style={{ width: '18rem' }}>
                                            <Card.Body>
                                                <Card.Title style={{fontWeight: 'bold'}}>Reports Summary</Card.Title>
                                                { article2.article.reports.map( report => {
                                                    return (
                                                        <div key={ report.reportId } className="report-card">
                                                            
                                                            <Card.Title>Date: {report.eventDate.substring(0,10)} </Card.Title>
                                                                <Card.Subtitle className="mb-2 text-muted">Diseases</Card.Subtitle>
                                                                { report.diseases.map( disease => {
                                                                    return (
                                                                        <Card.Text key={ disease } className="result-item">
                                                                            <li>{disease}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                                <Card.Subtitle className="mb-2 text-muted">Locations</Card.Subtitle>
                                                                { report.locations.map( location => {
                                                                    return (
                                                                        <Card.Text key={ location } className="result-item">
                                                                            <li>{location}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                                <Card.Subtitle className="mb-2 text-muted">Syndromes</Card.Subtitle>
                                                                { report.syndromes.map( syndrome => {
                                                                    return (
                                                                        <Card.Text key={ syndrome } className="result-item">
                                                                            <li>{syndrome}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                        
                                                        </div>
                                                    )
                                                } ) }
                                            </Card.Body>
                                        </Card>
                                    </Container>


                                    <li className='headline' style={{fontWeight: 'bold'}}>
                                        {items.articles[2].headline}   
                                    </li>   
                                    <p className='headline2'>Published on {items.articles[2].dateOfPublication}</p>
                                    <Container className="mt-5 p-5 shadow rounded">
                                        <div style={{whiteSpace: "pre-wrap"}}>
                                            <ReadMore>
                                                {article3.article.mainText}
                                            </ReadMore>     
                                        </div>
                                        <Card style={{ width: '18rem' }}>
                                            <Card.Body>
                                                <Card.Title style={{fontWeight: 'bold'}}>Reports Summary</Card.Title>
                                                { article3.article.reports.map( report => {
                                                    return (
                                                        <div key={ report.reportId } className="report-card">
                                                            
                                                            <Card.Title>Date: {report.eventDate.substring(0,10)} </Card.Title>
                                                                <Card.Subtitle className="mb-2 text-muted">Diseases</Card.Subtitle>
                                                                { report.diseases.map( disease => {
                                                                    return (
                                                                        <Card.Text key={ disease } className="result-item">
                                                                            <li>{disease}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                                <Card.Subtitle className="mb-2 text-muted">Locations</Card.Subtitle>
                                                                { report.locations.map( location => {
                                                                    return (
                                                                        <Card.Text key={ location } className="result-item">
                                                                            <li>{location}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                                <Card.Subtitle className="mb-2 text-muted">Syndromes</Card.Subtitle>
                                                                { report.syndromes.map( syndrome => {
                                                                    return (
                                                                        <Card.Text key={ syndrome } className="result-item">
                                                                            <li>{syndrome}</li>
                                                                        </Card.Text>
                                                                    )
                                                                } ) }
                                                        
                                                        </div>
                                                    )
                                                } ) }
                                            </Card.Body>
                                        </Card>
                                    </Container>


                                    
                                </div>
                            )
                        } else {
                            return (
                                <div style={{ backgroundColor: '#fafafa'}}>{/*	Result*/}
                                    { this.renderSearchResults() }
                                </div>
                            )
                        }
                    })()}
  

                    {/* reference link*/}
                    <div className="header3" style={{ backgroundColor: '#fafafa'}}>
                        This page is using the API from team 'Viral': <a href="https://teamviral-api.herokuapp.com/docs/#" target="_blank">{" "}https://teamviral-api.herokuapp.com/docs/#/</a>
                    </div>
                
            </div>
        );

    }


}

export default ArticleSearch;
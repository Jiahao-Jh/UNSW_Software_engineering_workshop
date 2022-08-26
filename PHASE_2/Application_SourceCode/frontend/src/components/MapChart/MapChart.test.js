import React from 'react';
import { shallow, render, mount } from 'enzyme';
import MapChart from './MapChart';

describe('MapChart', () => {
  let props;
  let shallowMapChart;
  let renderedMapChart;
  let mountedMapChart;

  const shallowTestComponent = () => {
    if (!shallowMapChart) {
      shallowMapChart = shallow(<MapChart {...props} />);
    }
    return shallowMapChart;
  };

  const renderTestComponent = () => {
    if (!renderedMapChart) {
      renderedMapChart = render(<MapChart {...props} />);
    }
    return renderedMapChart;
  };

  const mountTestComponent = () => {
    if (!mountedMapChart) {
      mountedMapChart = mount(<MapChart {...props} />);
    }
    return mountedMapChart;
  };  

  beforeEach(() => {
    props = {};
    shallowMapChart = undefined;
    renderedMapChart = undefined;
    mountedMapChart = undefined;
  });

  // Shallow / unit tests begin here
 
  // Render / mount / integration tests begin here
  
});

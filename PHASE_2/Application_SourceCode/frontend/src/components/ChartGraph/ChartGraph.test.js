import React from 'react';
import { shallow, render, mount } from 'enzyme';
import Chart from './Chart';

describe('Chart', () => {
  let props;
  let shallowChart;
  let renderedChart;
  let mountedChart;

  const shallowTestComponent = () => {
    if (!shallowChart) {
      shallowChart = shallow(<Chart {...props} />);
    }
    return shallowChart;
  };

  const renderTestComponent = () => {
    if (!renderedChart) {
      renderedChart = render(<Chart {...props} />);
    }
    return renderedChart;
  };

  const mountTestComponent = () => {
    if (!mountedChart) {
      mountedChart = mount(<Chart {...props} />);
    }
    return mountedChart;
  };  

  beforeEach(() => {
    props = {};
    shallowChart = undefined;
    renderedChart = undefined;
    mountedChart = undefined;
  });

  // Shallow / unit tests begin here
 
  // Render / mount / integration tests begin here
  
});

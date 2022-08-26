import React from 'react';
import { shallow, render, mount } from 'enzyme';
import BottomBar from './BottomBar';

describe('BottomBar', () => {
  let props;
  let shallowBottomBar;
  let renderedBottomBar;
  let mountedBottomBar;

  const shallowTestComponent = () => {
    if (!shallowBottomBar) {
      shallowBottomBar = shallow(<BottomBar {...props} />);
    }
    return shallowBottomBar;
  };

  const renderTestComponent = () => {
    if (!renderedBottomBar) {
      renderedBottomBar = render(<BottomBar {...props} />);
    }
    return renderedBottomBar;
  };

  const mountTestComponent = () => {
    if (!mountedBottomBar) {
      mountedBottomBar = mount(<BottomBar {...props} />);
    }
    return mountedBottomBar;
  };  

  beforeEach(() => {
    props = {};
    shallowBottomBar = undefined;
    renderedBottomBar = undefined;
    mountedBottomBar = undefined;
  });

  // Shallow / unit tests begin here
 
  // Render / mount / integration tests begin here
  
});

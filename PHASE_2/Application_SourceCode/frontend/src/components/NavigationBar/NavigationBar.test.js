import React from 'react';
import { shallow, render, mount } from 'enzyme';
import NavigationBar from './NavigationBar';

describe('NavigationBar', () => {
  let props;
  let shallowNavigationBar;
  let renderedNavigationBar;
  let mountedNavigationBar;

  const shallowTestComponent = () => {
    if (!shallowNavigationBar) {
      shallowNavigationBar = shallow(<NavigationBar {...props} />);
    }
    return shallowNavigationBar;
  };

  const renderTestComponent = () => {
    if (!renderedNavigationBar) {
      renderedNavigationBar = render(<NavigationBar {...props} />);
    }
    return renderedNavigationBar;
  };

  const mountTestComponent = () => {
    if (!mountedNavigationBar) {
      mountedNavigationBar = mount(<NavigationBar {...props} />);
    }
    return mountedNavigationBar;
  };  

  beforeEach(() => {
    props = {};
    shallowNavigationBar = undefined;
    renderedNavigationBar = undefined;
    mountedNavigationBar = undefined;
  });

  // Shallow / unit tests begin here
 
  // Render / mount / integration tests begin here
  
});

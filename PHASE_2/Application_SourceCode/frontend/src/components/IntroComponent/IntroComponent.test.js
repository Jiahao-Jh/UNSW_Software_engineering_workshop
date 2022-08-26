import React from 'react';
import { shallow, render, mount } from 'enzyme';
import IntroComponent from './IntroComponent';

describe('IntroComponent', () => {
  let props;
  let shallowIntroComponent;
  let renderedIntroComponent;
  let mountedIntroComponent;

  const shallowTestComponent = () => {
    if (!shallowIntroComponent) {
      shallowIntroComponent = shallow(<IntroComponent {...props} />);
    }
    return shallowIntroComponent;
  };

  const renderTestComponent = () => {
    if (!renderedIntroComponent) {
      renderedIntroComponent = render(<IntroComponent {...props} />);
    }
    return renderedIntroComponent;
  };

  const mountTestComponent = () => {
    if (!mountedIntroComponent) {
      mountedIntroComponent = mount(<IntroComponent {...props} />);
    }
    return mountedIntroComponent;
  };  

  beforeEach(() => {
    props = {};
    shallowIntroComponent = undefined;
    renderedIntroComponent = undefined;
    mountedIntroComponent = undefined;
  });

  // Shallow / unit tests begin here
 
  // Render / mount / integration tests begin here
  
});

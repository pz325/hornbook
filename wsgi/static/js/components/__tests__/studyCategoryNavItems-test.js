var React = require('react');
var ReactDOM = require('react-dom');
var ReactBootstrap = require('react-bootstrap');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');

const StudyCategoryNavItems = require('../studyCategoryNavItems');

describe('StudyCategoryNavItems', () => {
    const categories = [{'category': 'a', 'display': 'a-display'},
        {'category': 'b', 'display': 'b-display'},
        {'category': 'c', 'display': 'c-display'}
    ];

    var selectedCategory = null;
    var navItemClickHandler = function(category) {
        selectedCategory = category;
    };

    it('shows correct number of nav items', () => {
        // render in the document
        var studyCategoryNavItems = TestUtils.renderIntoDocument(
            <StudyCategoryNavItems categories={categories} navItemClickHandler={navItemClickHandler} />
        );

        var navItems = TestUtils.scryRenderedDOMComponentsWithTag(studyCategoryNavItems, 'li');
        expect(navItems.length).toBe(categories.length);
    });
    
    it('props.navItemClickHandler is called when nav item is clicked', () => {
        // render in the document
        var studyCategoryNavItems = TestUtils.renderIntoDocument(
            <StudyCategoryNavItems categories={categories} navItemClickHandler={navItemClickHandler} />
        );

        var navItems = TestUtils.scryRenderedDOMComponentsWithTag(studyCategoryNavItems, 'li');
        var index = Math.floor(Math.random() * categories.length);

        TestUtils.Simulate.click(ReactDOM.findDOMNode(navItems[index]).firstChild);
        expect(selectedCategory).toBe(categories[index].category);
    });
});

var React = require('react');
var ReactDOM = require('react-dom');
var ReactBootstrap = require('react-bootstrap');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');

const StudyCategoryNavItems = require('../studyCategoryNavItems');

describe('StudyCategoryNavItems', () => {
    const categories = [
        {
            "url": "http://localhost:8000/api/study/category/4",
            "user": "xinrong",
            "card": {
                "url": "http://localhost:8000/api/study/card/2",
                "font_size": "han_character_small"
            },
            "id": 4,
            "display": "认字",
            "num_retired": 5
        },
        {
            "url": "http://localhost:8000/api/study/category/5",
            "user": "xinrong",
            "card": {
                "url": "http://localhost:8000/api/study/card/1",
                "font_size": "han_character"
            },
            "id": 5,
            "display": "write_hanzi",
            "num_retired": 10
        },
        {
            "url": "http://localhost:8000/api/study/category/6",
            "user": "xinrong",
            "card": {
                "url": "http://localhost:8000/api/study/card/1",
                "font_size": "han_character"
            },
            "id": 6,
            "display": "read_hanzi",
            "num_retired": 10
        }]

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
        expect(selectedCategory.id).toBe(categories[index].id);
    });
});

var React = require('react');
var ReactDOM = require('react-dom');
var ReactBootstrap = require('react-bootstrap');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');

const BadgeList = require('../badgeList');

describe('BadgeList', () => {
    const contents = ['aa', 'bb', 'cc'];

    it('shows correct number of badges', () => {
        // render in the document
        var badgeList = TestUtils.renderIntoDocument(
            <BadgeList contents={contents} />
        );

        var badgeNodes = ReactDOM.findDOMNode(badgeList).childNodes;
        expect(badgeNodes.length).toBe(contents.length);
    });
    it('each badge shows correct content', () => {
        // render in the document
        var badgeList = TestUtils.renderIntoDocument(
            <BadgeList contents={contents} />
        );

        var badgeNodes = ReactDOM.findDOMNode(badgeList).childNodes;
        for (var i = 0; i < contents.length; ++i)
        {
            expect(badgeNodes[i].textContent).toBe(contents[i]);
        }
    });
});

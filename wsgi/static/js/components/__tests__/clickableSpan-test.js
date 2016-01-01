var React = require('react');
var ReactDOM = require('react-dom');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');

const ClickableSpan = require('../clickableSpan');

describe('ClickableSpan', () => {
    const contents = 'test';
    var clicked = false;
    var clickHandler = function(){
        clicked = true;
    };
    const fontClass = 'font-class';

    it('shows the set content', () => {
        // render in the document
        var clickableSpan = TestUtils.renderIntoDocument(
            <ClickableSpan content={contents} clickHandler={clickHandler} fontClass={fontClass} />
        );

        var spanNode = ReactDOM.findDOMNode(clickableSpan);
        expect(spanNode.textContent).toBe(contents);
    });
    it('has the correct font class', () => {
        // render in the document
        var clickableSpan = TestUtils.renderIntoDocument(
            <ClickableSpan content={contents} clickHandler={clickHandler} fontClass={fontClass} />
        );
        var spanNode = ReactDOM.findDOMNode(clickableSpan).firstChild;
        expect(spanNode.attributes.getNamedItem("class").value).toBe(fontClass);
    });
    it('invokes the set click handler', () => {
        // render in the document
        var clickableSpan = TestUtils.renderIntoDocument(
            <ClickableSpan content={contents} clickHandler={clickHandler} fontClass={fontClass} />
        );
        var spanNode = ReactDOM.findDOMNode(clickableSpan).firstChild;
        TestUtils.Simulate.click(spanNode);
        expect(clicked).toBe(true);
    });
});
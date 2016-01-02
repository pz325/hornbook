var React = require('react');
var ReactDOM = require('react-dom');
var ReactBootstrap = require('react-bootstrap');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');

/**
  example expanded DOM

    <div data-reactid=".0">
        <span class="label label-warning" data-reactid=".0.0">
            <span data-reactid=".0.0.0">New: </span>
            <span data-reactid=".0.0.1">30</span>
        </span>
        <span class="label label-info" data-reactid=".0.1">
            <span data-reactid=".0.1.0">Studying: </span>
            <span data-reactid=".0.1.1">20</span>
        </span>
        <span class="label label-success" data-reactid=".0.2">
            <span data-reactid=".0.2.0">Grasped: </span>
            <span data-reactid=".0.2.1">50</span>
        </span>
    </div>
*/
const StatLabels = require('../statLabels');

describe('StatLabels', () => {
    const statNew = 30;
    const statStudying = 20;
    const statGrasped = 50;
    const stats = {
        'new': statNew,
        'studying': statStudying,
        'grasped': statGrasped
    };

    it('has three labels', () => {
        // render StatLabels in the document
        var statLabels = TestUtils.renderIntoDocument(
            <StatLabels stats={stats} />
        );

        var labelDOMs = TestUtils.scryRenderedDOMComponentsWithClass(statLabels, 'label');
        expect(labelDOMs.length).toBe(3);
    });

    it('the first label is New', () => {
        // render StatLabels in the document
        var statLabels = TestUtils.renderIntoDocument(
            <StatLabels stats={stats} />
        );

        var labelDOMs = TestUtils.scryRenderedDOMComponentsWithClass(statLabels, 'label');
        var newLabelNode = ReactDOM.findDOMNode(labelDOMs[0]);
        var newSpanNode = newLabelNode.firstChild;
        expect(newSpanNode.textContent).toBe('New: ');
    });
    it('the second label is Studying', () => {
        // render StatLabels in the document
        var statLabels = TestUtils.renderIntoDocument(
            <StatLabels stats={stats} />
        );

        var labelDOMs = TestUtils.scryRenderedDOMComponentsWithClass(statLabels, 'label');
        var newLabelNode = ReactDOM.findDOMNode(labelDOMs[1]);
        var newSpanNode = newLabelNode.firstChild;
        expect(newSpanNode.textContent).toBe('Studying: ');
    });
    it('the last label is Grasped', () => {
        // render StatLabels in the document
        var statLabels = TestUtils.renderIntoDocument(
            <StatLabels stats={stats} />
        );

        var labelDOMs = TestUtils.scryRenderedDOMComponentsWithClass(statLabels, 'label');
        var newLabelNode = ReactDOM.findDOMNode(labelDOMs[2]);
        var newSpanNode = newLabelNode.firstChild;
        expect(newSpanNode.textContent).toBe('Grasped: ');
    });
    it('the value of the New label is statNew', () => {
        // render StatLabels in the document
        var statLabels = TestUtils.renderIntoDocument(
            <StatLabels stats={stats} />
        );

        var labelDOMs = TestUtils.scryRenderedDOMComponentsWithClass(statLabels, 'label');
        var newLabelNode = ReactDOM.findDOMNode(labelDOMs[0]);
        var newSpanNode = newLabelNode.lastChild;
        expect(newSpanNode.textContent).toBe(statNew.toString()); 
    });
    it('the value of the Studying label is statStudying', () => {
        // render StatLabels in the document
        var statLabels = TestUtils.renderIntoDocument(
            <StatLabels stats={stats} />
        );

        var labelDOMs = TestUtils.scryRenderedDOMComponentsWithClass(statLabels, 'label');
        var newLabelNode = ReactDOM.findDOMNode(labelDOMs[1]);
        var newSpanNode = newLabelNode.lastChild;
        expect(newSpanNode.textContent).toBe(statStudying.toString()); 
    });
    it('the value of the Grasped label is statGrasped', () => {
        // render StatLabels in the document
        var statLabels = TestUtils.renderIntoDocument(
            <StatLabels stats={stats} />
        );

        var labelDOMs = TestUtils.scryRenderedDOMComponentsWithClass(statLabels, 'label');
        var newLabelNode = ReactDOM.findDOMNode(labelDOMs[2]);
        var newSpanNode = newLabelNode.lastChild;
        expect(newSpanNode.textContent).toBe(statGrasped.toString()); 
    });
});

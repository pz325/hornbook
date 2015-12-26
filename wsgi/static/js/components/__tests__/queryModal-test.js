var React = require('react');
var ReactDOM = require('react-dom');
var ReactBootstrap = require('react-bootstrap');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');

/**
  example expanded DOM
    
*/
const QueryModal = require('../queryModal');

describe('QueryModal', () => {
    const header = 'header';
    const contents = 'contents'
    var noClicked = false;
    var yesClicked = false;
    var funcNo = function() {
        noClicked = true;
    };
    var funcYes = function() {
        yesClicked = true;
    };
    it('does not render when props.show is false', ()=>{
        // render StatLabels in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={false} header={header} contents={contents} no={funcNo} yes={funcYes} />
        );
        var notFound = ReactDOM.findDOMNode(queryModal.refs.title);
        expect(notFound).toNotExist();
    });
    it('renders when props.show is true', () => {
        // render StatLabels in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} header={header} contents={contents} no={funcNo} yes={funcYes} />
        );
        var found = ReactDOM.findDOMNode(queryModal.refs.title);
        expect(found).toExist();
    });
    it('header is "header"', () => {
        // render StatLabels in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} header={header} contents={contents} no={funcNo} yes={funcYes} />
        );
        var headerNode = ReactDOM.findDOMNode(queryModal.refs.title);
        expect(headerNode.textContent).toBe(header); 
    });
    it('contents is "contents"', () => {
        // render StatLabels in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} header={header} contents={contents} no={funcNo} yes={funcYes} />
        );
        var bodyNode = ReactDOM.findDOMNode(queryModal.refs.body);
        expect(bodyNode.textContent).toBe(contents); 
    });
    it('calls props.yes when button Save clicked', () => {    
        // render StatLabels in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} header={header} contents={contents} no={funcNo} yes={funcYes} />
        );
        var buttonSaveNode = ReactDOM.findDOMNode(queryModal.refs.buttonSave);
        TestUtils.Simulate.click(buttonSaveNode);
        expect(yesClicked).toBe(true);
    });
    it('calls props.no when button No clicked', () => {
        // render StatLabels in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} header={header} contents={contents} no={funcNo} yes={funcYes} />
        );
        var buttonNoNode = ReactDOM.findDOMNode(queryModal.refs.buttonNo);
        TestUtils.Simulate.click(buttonNoNode);
        expect(noClicked).toBe(true);
    });
});
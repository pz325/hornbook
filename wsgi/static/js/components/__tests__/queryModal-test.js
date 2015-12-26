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
    const title = 'title';
    const body = 'body'
    var noClicked = false;
    var yesClicked = false;
    var funcNo = function() {
        noClicked = true;
    };
    var funcYes = function() {
        yesClicked = true;
    };
    it('does not render when props.show is false', ()=>{
        // render in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={false} title={title} body={body} no={funcNo} yes={funcYes} />
        );
        var notFound = ReactDOM.findDOMNode(queryModal.refs.title);
        expect(notFound).toNotExist();
    });
    it('renders when props.show is true', () => {
        // render in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} title={title} body={body} no={funcNo} yes={funcYes} />
        );
        var found = ReactDOM.findDOMNode(queryModal.refs.title);
        expect(found).toExist();
    });
    it('title is "title"', () => {
        // render in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} title={title} body={body} no={funcNo} yes={funcYes} />
        );
        var titleNode = ReactDOM.findDOMNode(queryModal.refs.title);
        expect(titleNode.textContent).toBe(title); 
    });
    it('body is "body"', () => {
        // render in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} title={title} body={body} no={funcNo} yes={funcYes} />
        );
        var bodyNode = ReactDOM.findDOMNode(queryModal.refs.body);
        expect(bodyNode.textContent).toBe(body); 
    });
    it('calls props.yes when button Save clicked', () => {    
        // render in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} title={title} body={body} no={funcNo} yes={funcYes} />
        );
        var buttonSaveNode = ReactDOM.findDOMNode(queryModal.refs.buttonSave);
        TestUtils.Simulate.click(buttonSaveNode);
        expect(yesClicked).toBe(true);
    });
    it('calls props.no when button No clicked', () => {
        // render in the document
        var queryModal = TestUtils.renderIntoDocument(
            <QueryModal show={true} title={title} body={body} no={funcNo} yes={funcYes} />
        );
        var buttonNoNode = ReactDOM.findDOMNode(queryModal.refs.buttonNo);
        TestUtils.Simulate.click(buttonNoNode);
        expect(noClicked).toBe(true);
    });
});
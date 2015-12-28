var React = require('react');
var ReactDOM = require('react-dom');
var ReactBootstrap = require('react-bootstrap');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');
var jquery = require('jquery');

var StudyPanel = require('../studyPanel');

describe('NewContentForm', () => {
    const hanzis = ['a', 'b', 'c', 'd'];
    const stats = {
        'new': 10,
        'studying': 20,
        'grasped': 30
    };
    var knowns = [];
    var unknowns = [];
    var sessionDoneHandler = function(k, u) {
        knowns = jquery.extend(true, [], k);
        unknowns = jquery.extend(true, [], u);
    };
    var newContents = [];
    var toSave = null;
    var newContentAddedHandler = function(n, s){
        newcontents = jquery.extend(true, [], n);
        toSave = s;
    };

    it('shows the first hanzi from props.hanzis', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );

        var spanHanzi = studyPanel.refs.StudyPanel_clickableSpan;
        expect(ReactDOM.findDOMNode(spanHanzi).textContent).toBe(hanzis[0]);

        // var input = newContentForm.refs.NewContentForm_inputNewContent;
        // input.getInputDOMNode().value = 'not empty';
        // TestUtils.Simulate.change(input.getInputDOMNode());

        // var buttonAdd = newContentForm.refs.NewContentForm_buttonAdd;
        // TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAdd));
                
        // var found = ReactDOM.findDOMNode(newContentForm.refs.NewContentForm_queryModal.refs.title);
        // expect(found).toExist();
    });
});
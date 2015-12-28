var React = require('react');
var ReactDOM = require('react-dom');
var ReactBootstrap = require('react-bootstrap');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');
var jquery = require('jquery');

var StatLabels = require('../statLabels');
var NewContentForm = require('../newContentForm');


describe('NewContentForm', () => {
    var newContentArray = [];
    var toSave = null;
    var addNewContents = function(a, save) {
        toSave = save;
        newContentArray = jquery.extend(true, [], a);
    };
    const stats = {
        'new': 10,
        'studying': 20,
        'grasped': 30
    };

    const statLabels = <StatLabels stats={stats} />;

    it('shows a modal to query to save to server when buttonAdd is clicked and the value of input is not empty', () => {
        // render StatLabels in the document
        var newContentForm = TestUtils.renderIntoDocument(
            <NewContentForm statLabels={statLabels} addNewContents={addNewContents}/>
        );

        var input = newContentForm.refs.NewContentForm_inputNewContent;
        input.getInputDOMNode().value = 'not empty';
        TestUtils.Simulate.change(input.getInputDOMNode());

        var buttonAdd = newContentForm.refs.NewContentForm_buttonAdd;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAdd));
                
        var found = ReactDOM.findDOMNode(newContentForm.refs.NewContentForm_queryModal.refs.title);
        expect(found).toExist();
    });
    it('does not show the modal when buttonAdd is clicked and the value of input is empty', () => {
        // render StatLabels in the document
        var newContentForm = TestUtils.renderIntoDocument(
            <NewContentForm statLabels={statLabels} addNewContents={addNewContents}/>
        );

        var input = newContentForm.refs.NewContentForm_inputNewContent;
        expect(input.getInputDOMNode().value).toBe('');

        var buttonAdd = newContentForm.refs.NewContentForm_buttonAdd;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAdd));

        var notFound = ReactDOM.findDOMNode(newContentForm.refs.NewContentForm_queryModal.refs.title);
        expect(notFound).toNotExist();
    });
    it('state.rawNewContents is updated while the value of input updated', () => {
        // render StatLabels in the document
        var newContentForm = TestUtils.renderIntoDocument(
            <NewContentForm statLabels={statLabels} addNewContents={addNewContents}/>
        );

        const rawNewContents = 'new contents';
        var input = newContentForm.refs.NewContentForm_inputNewContent;
        input.getInputDOMNode().value = rawNewContents;
        TestUtils.Simulate.change(input.getInputDOMNode());

        expect(newContentForm.state.rawNewContents).toBe(rawNewContents);
    });
    it('calls props.addNewContents method with save=true when modal\'s Save button clicked', () => {
        // render StatLabels in the document
        var newContentForm = TestUtils.renderIntoDocument(
            <NewContentForm statLabels={statLabels} addNewContents={addNewContents}/>
        );

        var input = newContentForm.refs.NewContentForm_inputNewContent;
        input.getInputDOMNode().value = 'not empty';
        TestUtils.Simulate.change(input.getInputDOMNode());

        var buttonAdd = newContentForm.refs.NewContentForm_buttonAdd;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAdd));

        var buttonSave = newContentForm.refs.NewContentForm_queryModal.refs.buttonSave;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonSave));

        expect(toSave).toBe(true);
    });
    it('calls props.addNewContents method with save=false when modal\'s No button clicked', () => {
        // render StatLabels in the document
        var newContentForm = TestUtils.renderIntoDocument(
            <NewContentForm statLabels={statLabels} addNewContents={addNewContents}/>
        );

        var input = newContentForm.refs.NewContentForm_inputNewContent;
        input.getInputDOMNode().value = 'not empty';
        TestUtils.Simulate.change(input.getInputDOMNode());

        var buttonAdd = newContentForm.refs.NewContentForm_buttonAdd;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAdd));

        var buttonNo = newContentForm.refs.NewContentForm_queryModal.refs.buttonNo;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonNo));

        expect(toSave).toBe(false);
    });
    it('calls props.addNewContents method with newContentArray is correctly set', () => {
        // render StatLabels in the document
        var newContentForm = TestUtils.renderIntoDocument(
            <NewContentForm statLabels={statLabels} addNewContents={addNewContents}/>
        );

        const rawNewContents = 'new contents';
        var input = newContentForm.refs.NewContentForm_inputNewContent;
        input.getInputDOMNode().value = rawNewContents;
        TestUtils.Simulate.change(input.getInputDOMNode());

        var buttonAdd = newContentForm.refs.NewContentForm_buttonAdd;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAdd));

        var buttonSave = newContentForm.refs.NewContentForm_queryModal.refs.buttonSave;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonSave));

        expect(newContentArray).toInclude('new');
        expect(newContentArray).toInclude('contents');
    });
});
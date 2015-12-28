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
    });
    
    it('state.hanziIndex starts with 0', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );
        expect(studyPanel.state.hanziIndex).toBe(0);
    });

    it('state.unknowns starts as empty array', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );
        expect(studyPanel.state.unknowns.length).toBe(0);
    });

    it('state.knowns starts as empty array', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );
        expect(studyPanel.state.knowns.length).toBe(0);
    });

    it('has buttonAddToKnown when props.recapMode is false', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );

        var buttonAddToKnown = studyPanel.refs.StudyPanel_buttonAddToUnknown;
        expect(buttonAddToKnown).toExist();
    });

    it('does not have buttonAddToKnown when props.recapMode is true', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={true}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );
        var notFound = studyPanel.refs.StudyPanel_buttonAddToUnknown;
        expect(notFound).toNotExist();
    });

    it('shows the 2nd hanzi when clickableSpan is clicked', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );

        var clickableSpan = studyPanel.refs.StudyPanel_clickableSpan;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(clickableSpan).firstChild);

        expect(ReactDOM.findDOMNode(clickableSpan).textContent).toBe(hanzis[1]);
    });

    it('1st hanzi is added to state.knowns when clickableSpan is clicked', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );

        var clickableSpan = studyPanel.refs.StudyPanel_clickableSpan;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(clickableSpan).firstChild);

        expect(studyPanel.state.knowns).toInclude(hanzis[0]);
    });

    it('shows the 2nd hanzi when buttonAddToKnown is clicked', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );

        var buttonAddToKnown = studyPanel.refs.StudyPanel_buttonAddToUnknown;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAddToKnown));

        var clickableSpan = studyPanel.refs.StudyPanel_clickableSpan;
        expect(ReactDOM.findDOMNode(clickableSpan).textContent).toBe(hanzis[1]);
    });

    it('1st hanzi is added to state.unknowns when buttonAddToKnown is clicked', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );

        var buttonAddToKnown = studyPanel.refs.StudyPanel_buttonAddToUnknown;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAddToKnown));

        expect(studyPanel.state.unknowns).toInclude(hanzis[0]);
    });

    it('calls props.sessionDoneHandler and state.knowns and state.unknowns are correct when clickableSpan is clicked at the last hanzi', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );

        studyPanel.state.hanziIndex = hanzis.length - 1;
        studyPanel.state.knowns.push(hanzis[0]);
        studyPanel.state.knowns.push(hanzis[2]);
        studyPanel.state.unknowns.push(hanzis[1]);

        var clickableSpan = studyPanel.refs.StudyPanel_clickableSpan;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(clickableSpan).firstChild);

        expect(knowns).toInclude(hanzis[0]);
        expect(knowns).toInclude(hanzis[2]);
        expect(knowns).toInclude(hanzis[3]);
        expect(unknowns).toInclude(hanzis[1]);
    });

    it('calls props.sessionDoneHandler and state.knowns and state.unknowns are correct when buttonAddToKnown is clicked at the last hanzi', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );

        studyPanel.state.hanziIndex = hanzis.length - 1;
        studyPanel.state.knowns.push(hanzis[0]);
        studyPanel.state.knowns.push(hanzis[2]);
        studyPanel.state.unknowns.push(hanzis[1]);

        var buttonAddToKnown = studyPanel.refs.StudyPanel_buttonAddToUnknown;
        TestUtils.Simulate.click(ReactDOM.findDOMNode(buttonAddToKnown));

        expect(knowns).toInclude(hanzis[0]);
        expect(knowns).toInclude(hanzis[2]);
        expect(unknowns).toInclude(hanzis[3]);
        expect(unknowns).toInclude(hanzis[1]);
    });

    it('props.newContentAddedHandler is called', () => {
        // render StudyPanel in the document
        var studyPanel = TestUtils.renderIntoDocument(
            <StudyPanel hanzis={hanzis} stats={stats}
                recapMode={false}
                sessionDoneHandler={sessionDoneHandler}
                newContentAddedHandler={newContentAddedHandler} />
        );
    });
});
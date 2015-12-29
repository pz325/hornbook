var React = require('react');
var ReactDOM = require('react-dom');
var ReactBootstrap = require('react-bootstrap');
var TestUtils = require('react-addons-test-utils');
var expect = require('expect');

const UserNavDropdown = require('../userNavDropdown');

describe('UserNavDropdown', () => {
    const username = 'user';

    var logInHandlerCalled = false;
    var logInHandler = function() {
        logInHandlerCalled = true;
    };

    var logOutHandlerCalled = false;
    var logOutHandler = function() {
        logOutHandlerCalled = true;
    };

    var settingsHandlerCalled = false;
    var settingsHandler = function() {
        settingsHandlerCalled = true;
    };

    var registerHandlerCalled = false;
    var registerHandler = function() {
        registerHandlerCalled = true;
    };

    it('shows logOut menu item when props.username is set', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown username={username} />
        );

        var menuItemLogOut = userNavDropdown.refs.UserNavDropdown_menuItemLogOut;
        expect(menuItemLogOut).toExist();
    });

    it('shows settings menu item when props.username is set', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown username={username} />
        );
        var menuItemSettings = userNavDropdown.refs.UserNavDropdown_menuItemSettings;
        expect(menuItemSettings).toExist();
    });
    it('shows username when props.username is set', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown username={username} />
        );

        var navDropDownNode = ReactDOM.findDOMNode(userNavDropdown);
        var usernameSpan = navDropDownNode.firstChild.firstChild.firstChild.firstChild;
        expect(usernameSpan.textContent).toBe(username);
    });

    it('shows logIn menu item when props.username is not set', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown />
        );
        var menuItemLogIn = userNavDropdown.refs.UserNavDropdown_menuItemLogIn;
        expect(menuItemLogIn).toExist();
    });
    it('shows register menu item when props.username is not set', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown />
        );
        var menuItemRegister = userNavDropdown.refs.UserNavDropdown_menuItemRegister;
        expect(menuItemRegister).toExist();
    });
    it('props.logInHandler can be called', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown logInHandler={logInHandler} />
        );
        var menuItemLogIn = userNavDropdown.refs.UserNavDropdown_menuItemLogIn;
        const anchor = TestUtils.findRenderedDOMComponentWithTag(menuItemLogIn, 'A');
        TestUtils.Simulate.click(anchor);

        expect(logInHandlerCalled).toBe(true);
    });
    it('props.logOutHandler can be called', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown username={username} logOutHandler={logOutHandler} />
        );
        var menuItemLogOut = userNavDropdown.refs.UserNavDropdown_menuItemLogOut;
        const anchor = TestUtils.findRenderedDOMComponentWithTag(menuItemLogOut, 'A');
        TestUtils.Simulate.click(anchor);

        expect(logOutHandlerCalled).toBe(true);
    });
    it('props.settingsHandler can be called', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown username={username} settingsHandler={settingsHandler} />
        );
        var menuItemSettings = userNavDropdown.refs.UserNavDropdown_menuItemSettings;
        const anchor = TestUtils.findRenderedDOMComponentWithTag(menuItemSettings, 'A');
        TestUtils.Simulate.click(anchor);

        expect(settingsHandlerCalled).toBe(true);
    });
    it('props.registerHandler can be called', () => {
        // render in the document
        var userNavDropdown = TestUtils.renderIntoDocument(
            <UserNavDropdown registerHandler={registerHandler} />
        );
        var menuItemRegister = userNavDropdown.refs.UserNavDropdown_menuItemRegister;
        const anchor = TestUtils.findRenderedDOMComponentWithTag(menuItemRegister, 'A');
        TestUtils.Simulate.click(anchor);

        expect(registerHandlerCalled).toBe(true);
    });
});

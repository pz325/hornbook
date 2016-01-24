"use strict";

var React = require('react');
var Nav = require('react-bootstrap').Nav;
var NavDropdown = require('react-bootstrap').NavDropdown;
var MenuItem = require('react-bootstrap').MenuItem;
var Glyphicon = require('react-bootstrap').Glyphicon;


var UserNavDropdown = React.createClass({
    propTypes:{
        username: React.PropTypes.string,
        logInHandler: React.PropTypes.func,
        logOutHandler: React.PropTypes.func,
        settingsHandler: React.PropTypes.func,
        registerHandler: React.PropTypes.func
    },

    render: function() {
        var userNavItems;
        if (this.props.username) {
            userNavItems = (
                <NavDropdown title={this.props.username} id="nav-user-dropdown">
                    <MenuItem ref='UserNavDropdown_menuItemSettings' onClick={this.props.settingsHandler}><Glyphicon glyph="wrench"/>Settings</MenuItem>
                    <MenuItem ref='UserNavDropdown_menuItemLogOut' onClick={this.props.logOutHandler}><Glyphicon glyph="log-out"/>Log out</MenuItem>
                </NavDropdown> 
            );
        } else {
            userNavItems = (
                <NavDropdown title='unregistered user' id="nav-user-dropdown">
                    <MenuItem ref='UserNavDropdown_menuItemRegister' onClick={this.props.registerHandler}><Glyphicon glyph="plus"/>Register</MenuItem>
                    <MenuItem ref='UserNavDropdown_menuItemLogIn' onClick={this.props.logInHandler}><Glyphicon glyph="log-in"/>Log in</MenuItem>
                </NavDropdown>
            );
        }

        return (
            //<div>
                <Nav pullRight>
                    {userNavItems}
                </Nav>
            //</div>
        );
    }
});

module.exports = UserNavDropdown;

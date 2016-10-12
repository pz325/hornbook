"use strict";

var React = require('react');
var Navbar = require('react-bootstrap').Navbar;
var Nav = require('react-bootstrap').Nav;
var NavItem = require('react-bootstrap').NavItem;
var NavDropdown = require('react-bootstrap').NavDropdown;
var MenuItem = require('react-bootstrap').MenuItem;
var Glyphicon = require('react-bootstrap').Glyphicon;

var StudyCategoryNavItems = require('./studyCategoryNavItems');
var UserNavDropdown = require('./userNavDropdown');


var HornbookNavbar = React.createClass({
    propTypes:{
        categories: React.PropTypes.array.isRequired,   // array of {'category': , 'display': }
        username: React.PropTypes.string,
        navItemClickHandler: React.PropTypes.func
    },

    login: function() {
        window.location.href = '/accounts/login/';
    },

    logout: function() {
        window.location.href = '/accounts/logout/';
    },

    render: function() {
        var component = this;

        return (
            <div>
                <Navbar>
                    <Navbar.Header>
                        <Navbar.Brand>
                            <a href="#">Horn Book</a>
                        </Navbar.Brand>
                        <Navbar.Toggle />
                    </Navbar.Header>
                    <Navbar.Collapse>
                        <StudyCategoryNavItems 
                            ref='HornbookNavBar_studyCategoryNavItems' 
                            categories={this.props.categories} 
                            navItemClickHandler={this.props.navItemClickHandler} />
                        <Nav>
                            <NavItem href="#"><Glyphicon glyph="plus"/></NavItem>
                        </Nav>
                        <UserNavDropdown 
                            ref='HornbookNavbar_userNavDropdown' 
                            username={this.props.username} 
                            logInHandler={this.login} 
                            logOutHandler={this.logout} />
                    </Navbar.Collapse>
                    
                </Navbar>
            </div>
        );
    }
});

module.exports = HornbookNavbar;

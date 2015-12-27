"use strict";

var React = require('react');
var Navbar = require('react-bootstrap').Navbar;
var Nav = require('react-bootstrap').Nav;
var NavItem = require('react-bootstrap').NavItem;
var NavDropdown = require('react-bootstrap').NavDropdown;
var MenuItem = require('react-bootstrap').MenuItem;
var Glyphicon = require('react-bootstrap').Glyphicon;


const HornbookNavbar = React.createClass({
    propTypes:{
        categories: React.PropTypes.array.isRequired,
        loggedIn: React.PropTypes.bool.isRequired,
        username: React.PropTypes.string
    },

    handleCategoryNavItemClick: function(category) {
        this.props.studyCategory(category);
    },

    render: function() {
        var component = this;
        var categoryNavItems = this.props.categories.map(function(category) {
            return (
                <li key={category}><a href='#' onClick={component.handleCategoryNavItemClick.bind(component, category)}>{category}</a></li>
            );
        });

        var userNavItems;
        if (this.props.loggedIn) {
            userNavItems = (
                <NavDropdown title={this.props.username} id="nav-user-dropdown">
                    <MenuItem><Glyphicon glyph="wrench"/>Settings</MenuItem>
                    <MenuItem><Glyphicon glyph="log-out"/>Log out</MenuItem>
                </NavDropdown> 
            );
        } else {
            userNavItems = (
                <NavDropdown id="nav-user-dropdown">
                    <MenuItem><Glyphicon glyph="plus"/>Register</MenuItem>
                    <MenuItem><Glyphicon glyph="log-in"/>Log in</MenuItem>
                </NavDropdown>
            );
        }

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
                        <Nav>
                            {categoryNavItems}
                            <NavItem href="#"><Glyphicon glyph="plus"/></NavItem>
                        </Nav>
                        <Nav pullRight>
                            {userNavItems}
                        </Nav>
                    </Navbar.Collapse>
                    
                </Navbar>
            </div>
        );
    }
});

module.exports = HornbookNavbar;

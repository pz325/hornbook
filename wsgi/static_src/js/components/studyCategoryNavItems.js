"use strict";

var React = require('react');
var Nav = require('react-bootstrap').Nav;


var StudyCategoryNavItems = React.createClass({
    propTypes:{
        categories: React.PropTypes.array.isRequired,    // array of {'category': , 'display': }
        navItemClickHandler: React.PropTypes.func
    },

    navItemClickHandler: function(category) {
        this.props.navItemClickHandler(category);
    },

    render: function() {
        var component = this;
        var categoryNavItems = this.props.categories.map(function(category) {
            var ref = 'StudyCategoryNavItems_navItem' + category.id;
            return (
                <li ref = {ref} key={category.id}>
                    <a href='#' onClick={component.navItemClickHandler.bind(null, category)}>
                    {category.display}
                    </a>
                </li>
            );
        });

        return (
            <div>        
                <Nav>
                    {categoryNavItems}
                </Nav>
            </div>
        );
    }
});

module.exports = StudyCategoryNavItems;

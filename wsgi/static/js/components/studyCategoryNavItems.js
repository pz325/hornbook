"use strict";

var React = require('react');
var Nav = require('react-bootstrap').Nav;


const StudyCategoryNavItems = React.createClass({
    propTypes:{
        categories: React.PropTypes.array.isRequired,    // array of {'category': , 'display': }
        navItemClickHandler: React.PropTypes.func
    },

    render: function() {
        var component = this;
        var categoryNavItems = this.props.categories.map(function(category) {
            const ref = 'StudyCategoryNavItems_navItem' + category;
            return (
                <li ref = {ref} key={category.category}>
                    <a href='#' onClick={component.props.navItemClickHandler.bind(component, category.category)}>
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

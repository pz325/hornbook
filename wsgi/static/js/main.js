$ = jQuery = require('jquery');

var React = require('react');
var ReactDOM = require('react-dom');
var NavBar = require('./components/navBar');

var StudyPage = require('./components/studyPage');


const username = $("#app").attr("data-username");
const loggedIn = $("#app").attr("data-loggedIn") === 'True';

var App = React.createClass({
    getInitialState: function() {
        return {
            'category': 'read_hanzi',
        };
    },

    studyCategory: function(category) {
        console.log(category);
    },

    render: function() {
        const categories = ['read_hanzi', 'write_hanzi', 'chinese_poem'];
        return (
            <div>
                <NavBar categories={categories} loggedIn={loggedIn} username={username} studyCategory={this.studyCategory}/>
                <StudyPage category={this.state.category} />
            </div>
        );
    }
});

ReactDOM.render(<App />, document.getElementById('app'));

//+ Jonas Raoni Soares Silva
//@ http://jsfromhell.com/array/shuffle [v1.0]
var shuffle = function(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var API_LEITNER_RECORD_URL = "/api/study/hanzi_study_record/leitner_record";
var API_PROGRESS_URL = "/api/study/hanzi_study_record/progress";

var StatComponent = React.createClass({
    render: function() {
        return (
            <div>
                <ReactBootstrap.Label bsStyle='warning'>New: {this.props.stats.new}</ReactBootstrap.Label>
                <ReactBootstrap.Label bsStyle='info'>Studying: {this.props.stats.studying}</ReactBootstrap.Label>
                <ReactBootstrap.Label bsStyle='success'>grasped: {this.props.stats.grasped}</ReactBootstrap.Label>
            </div>
        );
    }
});

var NewContentComponent = React.createClass({
    render: function() {
        const addButton = <ReactBootstrap.Button bsStyle="info"><ReactBootstrap.Glyphicon glyph="plus"/></ReactBootstrap.Button>;
        const stats = <StatComponent stats={this.props.stats} />;
        return (
            <div>
                <hr/>
                <div className="stat">
                    <ReactBootstrap.Input type="text" placeholder="new content" ref="new_content" 
                        addonBefore={stats}
                        buttonAfter={addButton}/>                
                </div>
            </div>
        );
    }
});

var StudyComponent = React.createClass({
    // main study component  
    getInitialState: function() {
        return {
            'hanziIndex': 0,
            'unknowns': [],
            'knowns': []
        };
    },
    componentDidMount: function() {
        var oldState = this.state;
        this.setState(oldState);
    },
    addToKnowns: function() {
        this.updateProgress(true);
    },
    addToUnknowns: function() {
        this.updateProgress(false);
    },
    updateProgress: function(addToKnowns) {
        var oldState = this.state;
        if (addToKnowns) {
            oldState.knowns.push(this.props.hanzis[oldState.hanziIndex]);            
        } else {
            oldState.unknowns.push(this.props.hanzis[oldState.hanziIndex]);            
        }
        
        oldState.hanziIndex += 1;
        if (oldState.hanziIndex < this.props.hanzis.length) {
            this.setState(oldState);
        } else {
            if (!this.props.recapMode) {
                this.commitResult();
            }
            var hanzisToRecap = this.props.recapMode ? 
                shuffle(this.props.hanzis):
                shuffle(this.state.unknowns);
            oldState.hanziIndex = 0;
            oldState.unknowns = [];
            // recap
            this.props.recap(hanzisToRecap);
        }
    },
    commitResult: function() {
        // commit to server
        var result = {
            "grasped_hanzi": this.state.knowns,
            "new_hanzi": this.state.unknowns
        };
        console.log(result);
        $.ajax({
            type: "POST",
            url: API_LEITNER_RECORD_URL,
            data: {
                grasped_hanzi: JSON.stringify(this.state.knowns), 
                new_hanzi: JSON.stringify(this.state.unknowns)
            },
            //data: data,
            dataType: "json",
            success: function(resp) {
                console.log(resp); }
        });
    },
    getAddToRecapButton: function() {
        if (!this.props.recapMode) {
            return (<ReactBootstrap.Button bsStyle="info" onClick={this.addToUnknowns}>Add To Recap</ReactBootstrap.Button>);
        } else {
            return 'Recap mode';
        }
    },
    render: function() {
        var unknownBadges = this.state.unknowns.map(function(unknown){
            return (<ReactBootstrap.Badge>{unknown}</ReactBootstrap.Badge>)
        });
        var hanzi = '';
        if (this.props.hanzis) {
            hanzi = this.props.hanzis[this.state.hanziIndex];
        } 
        return (
            <div>
                <ReactBootstrap.ProgressBar max={this.props.hanzis.length} now={this.state.hanziIndex+1} bsStyle="success" label="%(now)s of %(max)s" />
                <div>
                    <span className="han_character" onClick={this.addToKnowns}>{hanzi}</span>
                </div>
                    {this.getAddToRecapButton()}
                <div>
                    {unknownBadges}
                </div>
                <hr/>
                {this.state.count}
            </div>
        );
    }
});



var HornbookComponent = React.createClass({
    getInitialState: function() {
        return {
            'hanzis': [],
            'stats': {},
            'recapMode': false
        };
    },
    recap: function(newHanzis) {
        var oldState = this.state;
        oldState.hanzis = newHanzis;
        oldState.recapMode = true;
        this.setState(oldState);
    },
    componentDidMount: function() {
        var component = this;
        $.when($.get(API_LEITNER_RECORD_URL), $.get(API_PROGRESS_URL))
        .done(function(leitnerRecordResp, progressResp){
            var hanzis = leitnerRecordResp[0].map(function(studyRecord) {
                    return studyRecord['hanzi']
                });
            component.setState({
                'hanzis': hanzis,
                'stats': progressResp[0]
            });
        });
    },
    render: function() {
        return (
            <div>
                <NewContentComponent stats={this.state.stats}/>
                <StudyComponent hanzis={this.state.hanzis} recap={this.recap} recapMode={this.state.recapMode}/>
            </div>
        );
    }
});


ReactDOM.render(
    <HornbookComponent />,
    document.getElementById('content')
);
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

var StudyAPI = (function() {
    const API_LEITNER_RECORD_URL = "/api/study/hanzi_study_record/leitner_record";
    const API_PROGRESS_URL = "/api/study/hanzi_study_record/progress";
    
    var getLeitnerRecord = function(category) {
        return $.ajax({
            type: 'GET',
            url: API_LEITNER_RECORD_URL,
            data: {
                category: category
            }
        });
    };

    var getProgress = function(category) {
        return $.ajax({
            type: 'GET',
            url: API_PROGRESS_URL,
            data: {
                category: category
            }
        })
    }

    /*
     * @param knowns an array
     * @param unknowns an array
     * @return $.ajax()
     */
    var updateLeitnerRecord = function(knowns, unknowns, category) {
        return $.ajax({
            type: "POST",
            url: API_LEITNER_RECORD_URL,
            data: {
                category: category,
                grasped_hanzi: JSON.stringify(knowns), 
                new_hanzi: JSON.stringify(unknowns)
            },
            //data: data,
            dataType: "json",
            success: function(resp) {
                console.log(resp); }
            });
    };

    return {
        updateLeitnerRecord: updateLeitnerRecord,
        getLeitnerRecord, getLeitnerRecord,
        getProgress, getProgress
    };
})();


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
    getInitialState() {
        return {
            'rawNewContents': "",
            'showModal': false,
            'newContents': []
        };
    },
    handleNewContentsInputChange(event) {
        var oldState = this.state;
        oldState.rawNewContents = event.target.value;
        oldState.newContents = this.refs.newContents.getValue().match(/\S+/g);
        this.setState(oldState);
    },
    handleAddButtonClick() {
        if (this.state.newContents.length > 0) {
            this.show();
        }
    },
    show() {
        var oldState = this.state;
        oldState.showModal = true;
        this.setState(oldState);
    },
    close() {
        var oldState = this.state;
        oldState.showModal = false;
        this.setState(oldState);
    },
    reset() {
        var oldState = this.state;
        oldState.rawNewContents = "";
        oldState.newContents = [];
        oldState.showModal = false;
        this.setState(oldState);
    },
    closeWithoutSavingToServer() {
        this.close();
        this.props.recap(this.state.newContents);
        this.reset();
    },
    saveNewContentToServer(){
        this.closeWithoutSavingToServer();
        StudyAPI.updateLeitnerRecord([], this.state.newContents, this.props.category);
        this.reset();
    },
    render: function() {
        const addButton = <ReactBootstrap.Button bsStyle="info" onClick={this.handleAddButtonClick}><ReactBootstrap.Glyphicon glyph="plus"/></ReactBootstrap.Button>;
        const stats = <StatComponent stats={this.props.stats} />;
        const newContents = this.state.newContents ? this.state.newContents.join() : "";

        return (
            <div>
                <hr/>
                <div className="stat">
                    <ReactBootstrap.Input 
                        type="text"
                        value={this.state.rawNewContents}
                        placeholder="new content. space to separate" 
                        ref="newContents" 
                        onChange={this.handleNewContentsInputChange}
                        addonBefore={stats}
                        buttonAfter={addButton}
                        help={"new contents: " + newContents}/>                
                </div>
                <ReactBootstrap.Modal show={this.state.showModal} onHide={this.closeWithoutSavingToServer}>
                    <ReactBootstrap.Modal.Header closeButton>
                        <ReactBootstrap.Modal.Title>Save the following new contents to server</ReactBootstrap.Modal.Title>
                    </ReactBootstrap.Modal.Header>
                    <ReactBootstrap.Modal.Body>
                        <div>
                            {newContents}
                        </div>
                    </ReactBootstrap.Modal.Body>
                    <ReactBootstrap.Modal.Footer>
                        <ReactBootstrap.ButtonToolbar>
                            <ReactBootstrap.Button bsStyle="info" onClick={this.saveNewContentToServer}>Save</ReactBootstrap.Button>
                            <ReactBootstrap.Button onClick={this.closeWithoutSavingToServer}>No</ReactBootstrap.Button>
                        </ReactBootstrap.ButtonToolbar>
                    </ReactBootstrap.Modal.Footer>
                </ReactBootstrap.Modal>
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
        StudyAPI.updateLeitnerRecord(this.state.knowns, this.state.unknowns, this.props.category);
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


var CATEGORY='read_hanzi';

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
        $.when(StudyAPI.getLeitnerRecord(CATEGORY), StudyAPI.getProgress(CATEGORY))
        .done(function(leitnerRecordResp, progressResp){
            console.log(leitnerRecordResp);
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
                <NewContentComponent stats={this.state.stats} recap={this.recap} category={CATEGORY} />
                <StudyComponent hanzis={this.state.hanzis} recap={this.recap} recapMode={this.state.recapMode} category={CATEGORY} />
            </div>
        );
    }
});


ReactDOM.render(
    <HornbookComponent />,
    document.getElementById('content')
);
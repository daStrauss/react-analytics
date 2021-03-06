var Comment = React.createClass({
  render: function() {
    var rawMarkup = marked(this.props.children.toString(), {sanitize: true});
    return (
      <div className="comment">
        <h2 className="commentAuthor">
          {this.props.author}
        </h2>
        <span dangerouslySetInnerHTML={{__html: rawMarkup}} />
      </div>
    );
  }
});

var CommentList = React.createClass({
  render: function() {
    var commentNodes = this.props.data.map(function (comment) {
      return (
        <Comment author={comment.author}>
          {comment.text}
        </Comment>
      );
    });
    return (
      <div className="commentList">
      {commentNodes}
      </div>
    );
  }
});
var CommentForm = React.createClass({
  handleSubmit: function(e) {
    console.log(e)
    e.preventDefault(); //what is e -- and what does it represent?
    var author = React.findDOMNode(this.refs.author).value.trim();
    var text = React.findDOMNode(this.refs.text).value.trim();
    if (!text || !author) {
      return;
      // presumably this this will take no action if either
      // text or author are missing. Of course no one is notified
      // in that case
    }
    this.props.onCommentSubmit({author: author, text: text});
    React.findDOMNode(this.refs.author).value = '';
    React.findDOMNode(this.refs.text).value = '';
    console.log(author);
    analytics.track('Sent Comment', {
      zog: 'foo' 
    });

    return;
  }, // also: why a comma here and not a semicolon?
  render: function() {
    return (
      <form className="commentForm" onSubmit={this.handleSubmit}>
      <input type="text" placeholder="your name" ref="author"/>
      <input type="text" placeholder="Say something..."  ref="text"/>
      <input type="submit" value="Post" />
      </form>
    );
  }
});

var data = [
  {author: "Dave S", text: "this is a comment"},
  {author: "Dave A", text: "this is *another* comment"}
];

var CommentBox = React.createClass({
  getInitialState: function() {
    return {data: []};
  },
  loadCommentsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleCommentSubmit: function(comment) {
    // the next three lines effectively replace & update the
    // internal comments.data state 
    var comments = this.state.data;
    var newComments = comments.concat([comment]);
    this.setState({data: newComments});
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: comment,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
    // setInterval(this.loadCommentsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="commentBox">
        <h1>Comments</h1>
        <CommentList data = {this.state.data} />
        <CommentForm onCommentSubmit={this.handleCommentSubmit}/>
      </div>
    );
  }
});
React.render(
  <CommentBox url="http://localhost:3000/comments.json" pollInterval={2000} />,
  document.getElementById('content')
);
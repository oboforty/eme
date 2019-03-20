

class ChatGroup {
  constructor(client) {
    this.client = client;

    this.username = null;

    this.$msg = document.getElementById('chat-messages');
  }

  request_register(username) {

    this.client.request('Chat:register', {
      username: username,
    }).then((resp) => {

      this.username = username;

      for (let msg of resp.history) {
        this.$msg.innerHTML += "<br/>"+msg;
      }
    });
  }

  new_user({username}) {
    this.$msg.innerHTML += "<br/>New user: <b>"+username+"</b>";
  }

  request_message(msg) {

    this.client.request('Chat:message', {
      msg: msg,
    }).then(function() {

    });
  }

  new_message({username, msg}) {
    this.$msg.innerHTML += "<br/>"+username+": "+msg;
  }
}
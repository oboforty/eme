

// Setup client groups
client.groups.Chat = new ChatGroup(client);


// Connect to client

client.connect('ws://127.0.0.1:3000', () => {
  document.getElementById('chat-debug').innerHTML = 'Connected!';

  let username = prompt("Give me a username:");
  client.groups.Chat.request_register(username);

  document.getElementById('chat-input').addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();

      let msg = this.value;
      this.value = "";

      client.groups.Chat.request_message(msg);
    }
  });

});


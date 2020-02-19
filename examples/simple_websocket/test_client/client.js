// websocket client to communicate with game server

let client = new (function(){
  this.groups = {};
  this.model = {};
  this.subscribed = {};
  this.reoccuring = {};
  this.ws = null;
  this.log_style = "color: purple";
  this.address = null;
  this.c_msid = 1;
  this.trying = false;
  this.request = function(route, params) {
    if (!params && typeof route !== 'string') {
        var params = route;
    } else {
        if (!params) params = {};
        params.route = route;
    }

    if (!params.route)
        console.error("No route defined for request: ", params);

    params.msid = this.c_msid++;
    console.log(`%c<${route} (${params.msid})`, client.log_style, params);

    var rwsString = JSON.stringify(params);
    try {
      this.ws.send(rwsString);
      return new DeferredResponse(route, params.msid);
    } catch(e){
      console.error(e);
      client.reconnect();
    }
  };

  this.on = function(route, callback) {
    this.reoccuring[route] = callback;
  };

  this.connect = function(serveraddress, callback) {
    this.address = serveraddress;

    this.ws = new WebSocket(serveraddress);
    this.ws.onopen = function(event) {
      console.log("%cConnected to websocket", client.log_style);
      callback();
    };
    this.ws.onerror = function(event) {
      console.error(event);
    };
    this.ws.onclose = function(event) {
      console.log("%cDisconnected from websocket", client.log_style);

      if (client.disconnected)
        client.disconnected();
      //client.reconnect();
    };
    this.ws.onmessage = function(event) {
      var rws = JSON.parse(event.data);

      try {
        var gmarr = rws.route.split(':');
        var group = client.groups[gmarr[0]] || this;
        var msid = rws.msid || rws.route;
        console.log('%c>'+rws.route+`(${msid})`, "color:purple", rws);

        try {
            var params = Object.assign({}, rws);
            delete params.route;
        } catch(e) {
            var params = rws;
        }

        if (params.params)
            params = params.params;

        if (client.subscribed[msid]) {
            // events handled by request().then(...)
            client.subscribed[msid].apply(group, [params]);
            delete client.subscribed[msid];
        }

        if (client.reoccuring[msid]) {
            // events handled by client.on(...)
            client.reoccuring[msid].apply(group, [params]);
        }

        var action = group[gmarr[1]];

        if (action) {
            // events handled by groups
            action.apply(group, [params]);
        }
      } catch (e) {
        console.error(e);

        //client.reconnect();
      }
    }
  };
  this.reconnect = function() {
    if (!client.trying) {
      client.tryReconnect();
    }
  };
  this.tryReconnect = function() {

    if (client.ws.readyState !== client.ws.OPEN) {
      client.trying = true;

      console.log("%cTrying to reconnect..", client.log_style)
      client.connect(client.address, function(){
        client.trying = false;
        console.log("%cReconnect successful", client.log_style);
      });

      setTimeout(client.tryReconnect, 4000);
    } else {
      //console.log("Reconnect successful");
    }
  }
})();


var DeferredResponse = function(route, msid) {
    this.then = function(callback) {
        client.subscribed[msid] = callback;
    }
};
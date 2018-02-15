// log display function
function append(text) {
  // document.getElementById("websocket_events").insertAdjacentHTML('beforeend', "<li>" + text + ";</li>");
  console.log(text);
} 

// websocket global variable
var websocket = null;

function wsrobot_connected() {
  var connected = false;
  if (websocket!=null)
    console.log("websocket.readyState: "+websocket.readyState)
  if (websocket!=null && websocket.readyState==1) {
    connected = true;
  }
  console.log("connected: "+connected)
  return connected;
}

function wsrobot_init(ip, port) {
    var url = "ws://"+ip+":"+port+"/websocketserver";
    console.log(url);
    websocket = new WebSocket(url);

    websocket.onmessage = function(event){
      console.log("message received: "+event.data);
      v = event.data.split('_');
      if (v[0]=='display') {
          if (v[1]=='text') {
              document.getElementById("text").innerHTML = v[2];
          }
          else if (v[1]=='image')  {
              document.getElementById("image").src = v[2];
              console.log('image: '+v[2]);
          }
          else if (v[1]=='button') {

            var b = document.createElement("input");
            //Assign different attributes to the element. 
            b.type = "button";
            b.value = v[3]; 
            b.name = v[2]; 
            b.id = v[2]; 
            b.onclick = function(event) { button_fn(event) };
            var bdiv = document.getElementById("buttons");
            bdiv.appendChild(b);
          }
        }
        else if (v[0]=='remove') {
            if (v[1]=='buttons') {
                var bdiv = document.getElementById("buttons");
                var fc = bdiv.firstChild;
                while( fc ) {
                    bdiv.removeChild( fc );
                    fc = bdiv.firstChild;
                }

            }
        }
        else if (v[0]=='reload') {
            location.reload();
        }
    } 

    websocket.onopen = function(){
      append("connection received");
      document.getElementById("status").innerHTML = "<font color='green'>o</font>";

    } 

    websocket.onclose = function(){
      append("connection closed");
      document.getElementById("status").innerHTML = "<font color='red'>o</font>";
    }

    websocket.onerror = function(){
      append("!!!connection error!!!");
    }

}
 
function wsrobot_quit() {
    websocket.close();
    websocket = null;
}

function wsrobot_send(data) {
  if (websocket!=null)
    websocket.send(data);
}


function button_fn(event) {
  var bsrc = event.srcElement || event.originalTarget
  console.log('websocket button '+bsrc.id)
  wsrobot_send(bsrc.id);
}



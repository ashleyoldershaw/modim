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
          if (v[1]=='text')
              document.getElementById(v[1]+'_'+v[2]).innerHTML = v[3];
          else if (v[1]=='image')
              document.getElementById(v[1]+'_'+v[2]).src = v[3];
          else if (v[1]=='pdf')
              document.getElementById(v[1]+'_'+v[2]).src = v[3];
          else if (v[1]=='button') {
            var b = document.createElement("input");
            //Assign different attributes to the element. 

            if (v[3].substr(0,3)=='img') {
                b.type = "image";
                b.src = v[3];
            }
            else {
                b.type = "button";
                b.value = v[3]; 
            }

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
        else if (v[0]=='url') {
            console.log('load url: '+v[1])
            window.location.assign(v[1])
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



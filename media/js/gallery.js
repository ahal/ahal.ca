var request;

function displaySets() {
 
  if (window.XMLHttpRequest) { // Mozilla, Safari, ...
    request = new XMLHttpRequest();
  } else if (window.ActiveXObject) { // IE
    try {
      request = new ActiveXObject("Msxml2.XMLHTTP");
    }
    catch (e) {
      try {
        request= new ActiveXObject("Microsoft.XMLHTTP");
      }
      catch (e) {}
    }
  }
  window.alert(request);

  if (!request) {
    return false;
  }
  request.onreadystatechange = onFinish;
  request.open('GET', 'http://k0s.org');
  request.send();
}
  
function onFinish() {
  if (request.readyState === 4) {
    window.alert(request.status);
    if (request.status === 200) {
      alert(request.responseText);
    }
  }
}

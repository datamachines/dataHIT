JSONEditor.defaults.theme = 'foundation5';
JSONEditor.defaults.iconlib = 'fontawesome4';

// Initialize the editor
var editor = new JSONEditor(document.getElementById('editor_holder'),{
  ajax: true, // Enable fetching schemas via ajax
  schema: {
    $ref: "static/schemas/analyticbehavior.json",
    format: "grid"
  },
  startval: start_data
});

document.getElementById('save').addEventListener('click',function() {
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       console.log("Plan saved");
    }
  };
  req.open('POST', "saverec", true);
  req.setRequestHeader("Content-Type", "application/json");
  recDoc = {
    datarec: editor.getValue(),
    recID: document.getElementById('recID').innerHTML
  }
  req.send(JSON.stringify(recDoc));
});

// When data changes
editor.on('change',function() {
  var errors = editor.validate();
  var indicator = document.getElementById('valid_indicator');
  if(errors.length) {
    indicator.className = 'label alert';
    indicator.textContent = 'not valid';
  }
  else {
    indicator.className = 'label success';
    indicator.textContent = 'valid';
  }
});

// When the editor is ready
editor.on('ready',function() {
//  setToDefault();
  console.log("start data: " + JSON.stringify(start_data))
});

/* Defunct
function setToDefault(){
  // Now the api methods will be available
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       console.log(req.responseText);
       editor.setValue(JSON.parse(req.responseText));
       editor.validate();
       console.log("Plan reset to default data");
    }
  };
  req.open('GET', "static/schemas/projectPlan-default.json", true);
  req.send();
}
*/

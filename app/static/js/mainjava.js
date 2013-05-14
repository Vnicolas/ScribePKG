$(document).ready(function() 
    { 
        $("#myTable").tablesorter();
        $("#Table2").tablesorter();
    } 
);
jQuery.ajaxSettings.traditional = true;
  $(document).ready(function(){
    $("input#save").click(function(){
      $("#block").css('visibility','visible');
      $("#loader").css('visibility','visible');
      $.getJSON($SCRIPT_ROOT + '/_savefile', {
      code: editor.getValue(),
      path: $("#dossier").text()
      }, function(data){
        $("#block").css('visibility','hidden');
        $("#loader").css('visibility','hidden');
        alert('Texte enregistré');
      });
    });
  });

$SCRIPT_ROOT = "";

jQuery.ajaxSettings.traditional = true;
  $(document).ready(function(){
    $("select").change(function(){
      $.getJSON($SCRIPT_ROOT + '/_getprofiles', {
      lgrp: $("select#Listegrp").val()
      }, function(data){
        var soft = data.profile;
        var text = document.getElementById('installed2');
        $('#addall').css('visibility','visible');
        $('.boutonadd').css('visibility','visible');
        $("#myTable input:checkbox").removeAttr('disabled');
        text.innerHTML='';
        for(var i= 0; i < soft.length; i++)
        {
          text.innerHTML ="<tr><td class='nomlogiciel'><label><span>" 
          + soft[i-1] 
          + "</span></label></td></tr>" 
          + "<tr><td class='nomlogiciel'><label><span>" 
          + soft[i] 
          + "</span></label></td></td>";
        };
      });
    });
  });

jQuery.ajaxSettings.traditional = true;
$(document).ready(function(){
var add = document.getElementsByClassName('boutonadd');
var text = document.getElementById('installed2');
$(add).click(function(){
var logiciel = $("#myTable input:checked").next('span').text();
var log= logiciel.split(" ");
  for(var i=1; i<log.length; i++){
    text.innerHTML = text.innerHTML 
    +"<tr><td style='background-color:#4BB5C1;' class='nomlogiciel'><label><input type='checkbox' name='choixsupp' ><span>" 
    + " " 
    + log[i]
    + "</span></label></td></tr>";
}
          $("#myTable input:checked").removeAttr("checked").attr('disabled', 'disabled');
          $("#addall input:checked").removeAttr("checked");
          $('.boutonsupp').css('visibility','visible');
          $('#allsupp').css('visibility','visible');
    });
  });

jQuery.ajaxSettings.traditional = true;
$(document).ready(function(){
var supp = document.getElementsByClassName('boutonsupp');
var text = document.getElementById('installed2');
$(supp).click(function(){
var logicielsupp = $("#Table2 input:checked").next('span').text();
var logsupp = logicielsupp.split(" ");
for(var i=1; i<logsupp.length; i++){
  $("#"+logsupp[i]+"").removeAttr('disabled');
}
$("#allsupp input:checked").removeAttr("checked");
$("#Table2 input:checked").closest('tr').remove();
});
});

function suppcocher(etat) {
  var inputs = document.getElementById('Table2').getElementsByTagName('input');
  for(i = 0; i < inputs.length; i++) {
    if(inputs[i].type == 'checkbox')
      inputs[i].checked = etat;
  }
}

function addcocher(etat) {
  var inputs = document.getElementById('myTable').getElementsByTagName('input');
  for(i = 0; i < inputs.length; i++) {
    if((inputs[i].type == 'checkbox' && inputs[i].disabled == false))
      inputs[i].checked = etat;
  }
}

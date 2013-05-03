$(document).ready(function() 
    { 
        $("#myTable").tablesorter();
        $("#myTable2").tablesorter();
        $("#myTable3").tablesorter();
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
        text.innerHTML='';
        var n=0;
        for(var i= 0; i < soft.length; i++)
        {
          text.innerHTML ="<tr><td class='nomlogiciel'><input type='checkbox' id=''><span>" + soft[i-1] + "</span></td></tr>" + "<tr><td class='nomlogiciel'><input type='checkbox' id=''><span>" + soft[i] + "</span></td></td>";
        };
      });
    });
  });


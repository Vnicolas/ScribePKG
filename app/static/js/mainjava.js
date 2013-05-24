$(document).ready(function() 
    { 
        $("#myTable").tablesorter();
        $("#Table2").tablesorter();

// surbrillance GROUPE

        var span1 = document.getElementById('results').getElementsByTagName('span1');
        $(span1).mouseover(function(){
        $('#Listegrp').addClass("run-animation");
      });

        $(span1).mouseout(function(){
        $('#Listegrp').removeClass("run-animation");
      });

// surbrillance RÉPERTOIRE

        var span2 = document.getElementById('results').getElementsByTagName('span2');
        $(span2).mouseover(function(){
        $('#logiciels').addClass("run-animation");
      });

        $(span2).mouseout(function(){
        $('#logiciels').removeClass("run-animation");
      });

// surbrillance APPLIQUER

        var span3 = document.getElementById('results').getElementsByTagName('span3');
        $(span3).mouseover(function(){
        $('.appliquer').addClass("run-animation");
      });

        $(span3).mouseout(function(){
        $('.appliquer').removeClass("run-animation");
      });
       
    } 

);

// Sauvegarde de l'édition des fichiers xml

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

// Retoune les groupes présents dans le dossier /profile

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
        $('.boutonsupp').css('visibility','visible');
        $('#allsupp').css('visibility','visible');
        $("#myTable input:checkbox").removeAttr('disabled');
        text.innerHTML='';
        for(var i= 0; i < soft.length ; i++)
        {
          text.innerHTML= text.innerHTML +"<tr><td class='nomlogiciel'><label class='prime'><span style='font-style: italic;'>"
          + " "
          + soft[i]
          + "</span></label><input class='boutonsupplogiciel'  type='submit' value='Supprimer'></td></tr>";
        };
      });
    });
  });

// Ajoute les logiciels sélectionnés

jQuery.ajaxSettings.traditional = true;
$(document).ready(function(){
var add = document.getElementsByClassName('boutonadd');
var text = document.getElementById('installed2');
$(add).click(function(){
var installed = $("#installed2 span").text();
var install= installed.split(" ");
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
    $(".appliquer").css('visibility','visible');
    });
  });

// Supprime les logiciels sélectionnés

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
$(".appliquer").css('visibility','visible');
$("#Table2 input:checked").closest('tr').remove();
  

});
});

// Coche tout dans "logiciels installés"

function suppcocher(etat) {
  var inputs = document.getElementById('Table2').getElementsByTagName('input');
  for(i = 0; i < inputs.length; i++) {
    if(inputs[i].type == 'checkbox')
      inputs[i].checked = etat;
  }
}

// Coche tout dans "Répertoire"

function addcocher(etat) {
  var inputs = document.getElementById('myTable').getElementsByTagName('input');
  for(i = 0; i < inputs.length; i++) {
    if((inputs[i].type == 'checkbox' && inputs[i].disabled == false))
      inputs[i].checked = etat;
  }
}

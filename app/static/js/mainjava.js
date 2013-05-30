$(document).ready(function()
{
  $("#myTable").tablesorter();
  $("#Table2").tablesorter(); 
});

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

  jQuery.ajaxSettings.traditional = true;
  $(document).ready(function(){
    $("#dl").click(function(){
      $("#block").css('visibility','visible');
      $("#loader").css('visibility','visible');
      $.getJSON($SCRIPT_ROOT + '/_dl', {
      xmlfile: $("#dossier").text()
      }, function(data){
        $("#block").css('visibility','hidden');
        $("#loader").css('visibility','hidden');
        alert('Fichier telechargé !');
      });
    });
  });

$SCRIPT_ROOT = "";

// Retoune les groupes présents dans le dossier /profile

jQuery.ajaxSettings.traditional = true;
  $(document).ready(function(){
    $("select").change(function()
    {
      $.getJSON($SCRIPT_ROOT + '/_getprofiles', 
      {
        lgrp: $("select#Listegrp").val()
      }, 
      function(data)
      {
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
          text.innerHTML= text.innerHTML +"<tr><td class='nomlogiciel'><label class='prime'><input type='checkbox' name='choixsupp' ><span style='font-style: italic;'>"
          + " "
          + soft[i]
          + "</span></label></td></tr>";
        };
        var pres = $("#Table2 span").text();
        var present = pres.split(" ");
        var listeapp = $("#myTable span").text();
        var logapp = listeapp.split(" ");
        for (var h=1 in logapp)
        {
          for (var k=1 in present) 
          {
            if (present[k]==logapp[h]) 
            {
              $("#"+logapp[h]+"").attr('disabled', 'disabled')
            };
          };
        };
      });
    });
  });

// Ajoute les logiciels sélectionnés

jQuery.ajaxSettings.traditional = true;
$(document).ready(function()
{
  var add = document.getElementsByClassName('boutonadd');
  var text = document.getElementById('installed2');
  $(add).click(function()
    {
      $.getJSON($SCRIPT_ROOT + '/_setprofile',
        {
          ids: $("#installed2 span").text() + $("#myTable input:checked").next('span').text(),
          grp: $("select#Listegrp").val()
        },
        function(data)
        {
          var installed = $("#installed2 span").text();
          var install= installed.split(" ");
          var logiciel = $("#myTable input:checked").next('span').text();
          var log= logiciel.split(" ");
          for(var i=1; i<log.length; i++)
          {
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
});

// Supprime les logiciels sélectionnés

jQuery.ajaxSettings.traditional = true;
$(document).ready(function()
{
  var supp = document.getElementsByClassName('boutonsupp');
  var text = document.getElementById('installed2');
  $(supp).click(function()
    {
      $.getJSON($SCRIPT_ROOT + '/_setprofile', 
        {
          ids: $("#installed2 :input:not(:checked) + span").text(),
          grp: $("select#Listegrp").val()
        },
        function(data)
        {
          var logicielsupp = $("#Table2 input:checked").next('span').text();
          var logsupp = logicielsupp.split(" ");
          for(var i=1; i<logsupp.length; i++)
            {
              $("#"+logsupp[i]+"").removeAttr('disabled');
            }
            $("#allsupp input:checked").attr('disabled', 'disabled');
            $(".appliquer").css('visibility','visible');
            $("#Table2 input:checked").closest('tr').remove();
          });
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

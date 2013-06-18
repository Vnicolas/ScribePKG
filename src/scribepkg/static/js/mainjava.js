jQuery.ajaxSettings.traditional = true;


$(document).ready(function()
{
  $("#myTable").tablesorter();
  $('.down').tipsy({ gravity: 'w'});
  $('#vuediteur').tipsy({ gravity: 'n'});
});

// Sauvegarde de l'édition des fichiers xml

  $(document).ready(function(){
    $("input#save").click(function(){
      $.getJSON($SCRIPT_ROOT + '/_savefile', {
      code: editor.getValue(),
      path: $("#dossier").text()
      }, function(data){
        jNotify('Fichier enregistré.',
            {
              autoHide : true, // added in v2.0
              TimeShown : 4000,
              HorizontalPosition : 'right',
              VerticalPosition : 'top',
              ShowOverlay : false
            });
      });
    });
  });


 // Notification de téléchargement

  $(document).ready(function(){
    $("#dl").click(function(){
      var logicieldl = $("#dossier").attr("name");
      jNotify('Le téléchargement de <strong>'+logicieldl+'</strong> a débuté,<br> vous serez prévenue une fois ce dernier terminé.',
            {
              autoHide : true, // added in v2.0
              TimeShown : 4000,
              HorizontalPosition : 'right',
              VerticalPosition : 'center',
              ShowOverlay : false
            });
      $.getJSON($SCRIPT_ROOT + '/_dl', {
      xmlfile: $("#dossier").text()
      }, function(data){
        jSuccess('<strong>'+logicieldl+'</strong> téléchargé.<br> L\'installateur est désormais présent sur le serveur.',
            {
              autoHide : false,
              HorizontalPosition : 'center',
              VerticalPosition : 'top',
              ShowOverlay : true
            });
      });
    });
  });


// Retourne les groupes présents dans le dossier /profile

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
        $('.boutonaddall').css('visibility','visible');
        $('.boutonadd').css('visibility','visible');
        $('.boutonsupp').css('visibility','visible');
        $('#allsupp').css('visibility','visible');
        $("#myTable input:checkbox").removeAttr('disabled');
        text.innerHTML='';
        // Création d'une ligne dans le tableau pour chaque logiciel installés
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
        for (var h=1 in logapp) // Désactive les checkbox des logiciels dans l'encadré "Répertoire"
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
          var groupe = $("select#Listegrp").val();
          for(var i=1; i<log.length; i++)
          {
            text.innerHTML = text.innerHTML 
            +"<tr><td style='background-color:#4BB5C1;' class='nomlogiciel'><label><input type='checkbox' name='choixsupp' ><span>" 
            + " " 
            + log[i]
            + "</span></label></td></tr>";
            if (log.length == 2){
            jSuccess('Le logiciel <strong>'+log[i]+'</strong> a été ajouté dans le groupe \"<strong>'+groupe+'</strong>\"',
            {
              autoHide : true,
              TimeShown : 3000, // en milisecondes
              HorizontalPosition : 'right',
              VerticalPosition : 'top',
              ShowOverlay : false
            });}
            if (log.length > 2){
            jSuccess('Les logiciels ont été ajouté dans le groupe \"<strong>'+groupe+'</strong>\"',
            {
              autoHide : true, 
              TimeShown : 3000, // en milisecondes
              HorizontalPosition : 'right',
              VerticalPosition : 'top',
              ShowOverlay : false
            });}
          }
          
          $("#myTable input:checked").removeAttr("checked").attr('disabled', 'disabled');
          $("#addall input:checked").removeAttr("checked");
        });
    });
});

// Ajoute à tous les groupes

$(document).ready(function()
{
  var addall = document.getElementsByClassName('boutonaddall');
  var text = document.getElementById('installed2');
  $(addall).click(function()
    {
      $.getJSON($SCRIPT_ROOT + '/_setallprofile',
        {
          softs: $("#myTable input:checked").next('span').text(),
          allgroups : $("select#Listegrp option").text()
        },
        function(data)
        {
          var softs = data.profile;
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
              if (log.length == 2)
                {
                  jSuccess('Le logiciel <strong>'+log[i]+'</strong> a été ajouté dans <strong>tous les groupes</strong>\"',
                {
                  autoHide : true,
                  TimeShown : 3000, // en milisecondes
                  HorizontalPosition : 'right',
                  VerticalPosition : 'top',
                  ShowOverlay : false
                });
                }
                if (log.length > 2)
                {
                  jSuccess('Les logiciels ont été ajouté dans <strong>tous les groupes</strong>\"',
                    {
                      autoHide : true,
                      TimeShown : 3000, // en milisecondes
                      HorizontalPosition : 'right',
                      VerticalPosition : 'top',
                      ShowOverlay : false
                    });
                }
              }
              $("#myTable input:checked").removeAttr("checked").attr('disabled', 'disabled');
              $("#addall input:checked").removeAttr("checked");
            });
});
});


// Supprime les logiciels sélectionnés

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
          var groupe = $("select#Listegrp").val();
          for(var i=1; i<logsupp.length; i++)
            {
              $("#"+logsupp[i]+"").removeAttr('disabled');
              
            if (logsupp.length == 2){
            jNotify('Le logiciel <strong>'+logsupp[i]+'</strong> a été supprimé du groupe \"<strong>'+groupe+'</strong>\"',
            {
              autoHide : true, // added in v2.0
              TimeShown : 3000,
              HorizontalPosition : 'right',
              VerticalPosition : 'center',
              ShowOverlay : false
            });}
            if (logsupp.length > 2){
            jNotify('Les logiciels ont été supprimé du groupe \"<strong>'+groupe+'</strong>\"',
            {
              autoHide : true, // added in v2.0
              TimeShown : 3000,
              HorizontalPosition : 'right',
              VerticalPosition : 'center',
              ShowOverlay : false
            });}
            }

            $("#allsupp input:checked").removeAttr("checked");
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

  $(document).ready(function(){
  $("label#newxml").click(function(){
    editor.setValue("");
    editor.gotoLine(1);
    var options = {
      buttons: {
      confirm: {
        text: 'Ok',
        className: 'blue',
        action: function(e) {
          $('#dossier').html('/home/wpkg/packages/' + e.input + '.xml');
          Apprise('close');
          var fichier = e.input;
          editor.setValue("");
          var editeurTopPosition = jQuery('#editeur').offset().top;
          jQuery('html, body').animate({scrollTop:editeurTopPosition}, 'slow');
        }
        },
      },
  input: true,
};
Apprise('Nom du fichier :', options);

 });
});
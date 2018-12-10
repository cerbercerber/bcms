

function dispModal(idcours) { 

       // var idcours=event.idcours;
    //if (event.popup) {
        
      //  if(event.isinmoodle)
      
       $('#modalResa').load('/bo/administratifedtresa/'+idcours);    
       $('#modalResa').modal('show');
        return false;
    
}

function dispImp()
{
    console.log("imp");
    $("#modalResaimp").modal('show');
}


function dropresize(newevent)
{
   
       
    var datedebut=newevent.start.format('YYYY-MM-DD HH:mm');
    var datefin=newevent.end.format('YYYY-MM-DD HH:mm');
    var momentdeb=moment(datedebut);
    var momentfin=moment(datefin);
    
    if (momentdeb.isBefore() || momentfin.isBefore()) 
    {
        dispImp();
         $('#calendart').fullCalendar('refetchEvents');
    }
    else
    {    
    $.post('/bo/administratifedtresa/'+newevent.idcours,
     {dndresize:"oui",
     datedebut:datedebut,
     datefin:datefin},function(data){
                   
        //console.log(data);
        if(data.error!="success")
        {         
            $("#pmessage").html(data.error);          
            $("#modalerror").modal('show');
            
        }
        else
        {
        //oTable.ajax.reload();
        //$('#myModal').modal('hide');       
        }
        $('#calendart').fullCalendar('refetchEvents');
         
    });
    }
}




//DOCUMENT READY
$("document").ready(function(e)
{


/*enregistrer formset*/
$(".enrformset").on('click',function(e){
    var submitname=$(this).attr("nom");
    //console.log(submitname);
    $('#groupesdt_form').append('<input type="hidden" value="Enregistrer"  name="'+submitname+'" />');
    $('#groupesdt_form').submit();
});

/*enregistrer formset list*/
$(".enrformsetlist").on('click',function(e){
    var submitname=$(this).attr("nom");
    var prefix=$(this).attr("prefix");
    //console.log(submitname);
    $('#groupesdt_form').append('<input type="hidden" value="Enregistrer"  name="'+submitname+'" />');
    $('#groupesdt_form').append('<input type="hidden" name="prefix"  value="'+prefix+'" />');
    $('#groupesdt_form').submit();
});


/*enregistrer inf*/
$(".enrinf").on('click',function(e){
    var submitname=$(this).attr("nom");
    //console.log(submitname);
    $('#groupesdt_form').append('<input type="hidden" value="Enregistrer"  name="'+submitname+'" />');
    $('#groupesdt_form').submit();
});


/*add fawesome icon */
$('a').each(function(e){
    var content=$(this).html().toLowerCase();
    //console.log(content);
    if (content.indexOf("supprimer")!=-1)
    $(this).html('<i class="fas fa-times-circle text-danger"></i> '+content);
    else if (content.indexOf("ajouter")!=-1)
    $(this).html('<i class="fas fa-plus-circle text-success"></i> '+content);
     else if (content.indexOf("détail")!=-1)
    $(this).html('<i class="fas fa-info-circle text-warning"></i> '+content);
     else if (content.indexOf("enregistrer")!=-1)
    $(this).html('<i class="fas fa-check-circle text-success"></i> '+content);
     else if (content.indexOf("retour")!=-1)
    $(this).html('<i class="fas fa-arrow-circle-left text-info"></i> '+content);
     else if (content.indexOf("annuler")!=-1)
    $(this).html('<i class="fas fa-arrow-circle-left text-info"></i> '+content);
});
$('input[type=submit]').each(function(e){
    var content=$(this).val().toLowerCase();
    //console.log(content);
    if (content.indexOf("supprimer")!=-1)
    {
        if ($(this).is(":visible"))
                $(this).before('<i class="fas fa-times-circle text-danger"></i> ');
    }
    else if (content.indexOf("ajouter")!=-1)
    $(this).before('<i style="margin-right:-13px;vertical-align:middle;" class="fas fa-plus-circle text-success"></i> ');
     else if (content.indexOf("détail")!=-1)
    $(this).before('<i style="margin-right:-13px;vertical-align:middle;" class="fas fa-info-circle text-warning"></i> ');    
    else if (content.indexOf("enregistrer")!=-1)
    $(this).before('<i style="margin-right:-13px;vertical-align:middle;" class="fas fa-check-circle text-success"></i> ');
});




/* supression auto liste elements*/
$(".supplist").on('click',function(u){
    
    if ($(this).closest('tr').find(':checkbox').prop('checked'))
        $(this).closest('tr').find(':checkbox').prop('checked', false);
    else
        $(this).closest('tr').find(':checkbox').prop('checked', true);
        
    $("#supplisteall").click();
});

//asterisk requiered
/*
$('input[required]').each(function(index){
var id =$(this).attr("id");
$('label[for='+  id  +']').html($('label[for='+  id  +']').html()+ '<span class="text-danger"> * </span>');
});
*/

//autcomplete
 $.ui.autocomplete.prototype._renderItem = function (ul, item) {
            item.label = item.label.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + $.ui.autocomplete.escapeRegex(this.term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), 
            "<span style='white-space:nowrap;background-color:lemonchiffon'><strong>$1</strong></span>"
            );
            return $("<li></li>")
                    .data("item.autocomplete", item)
                    .append("<a>" + item.label + "</a>")
                    .appendTo(ul);
        };
 $.widget( "custom.catcomplete", $.ui.autocomplete, {
      _create: function() {
        this._super();
        this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
      },
      _renderMenu: function( ul, items ) {
        var that = this,
          currentCategory = "";
        $.each( items, function( index, item ) {
          var li;
          if ( item.category != currentCategory ) {
            ul.append( "<li class='ui-autocomplete-category'><div class='text-center text-dark bg-light rounded'>" + item.category + "</div></li>" );
            currentCategory = item.category;
          }
          li = that._renderItemData( ul, item);
          if ( item.category ) {
            li.attr( "aria-label", item.category + " : " + item.label );
            li.attr( "style", "white-space:nowrap" );           
          }
        });
      }
    });
    
$( "#searchall" ).catcomplete({
      position: { my : "right top", at: "right bottom" },    
      source: function( request, response ) {
        $.ajax( {
          url: "/bo/search",
          type: "POST",
          data: {
            term: request.term
          },
          success: function( data ) {
            response( data );
          }
        } );
      },
      delay:0,
      minLength: 1,
      select: function( event, ui ) {
      window.location.href = ui.item.url;
      }
    } );

//LIST
var oTable=$('#calendartable').DataTable( {
    "ajax": {
        "url": "/bo/administratifedt/ls",
        "type": "POST",
        "data": {
        modele: $("#admmod").val(),
        oid: $("#admoid").val(),
        start: function(d){ if ($('#calendart').fullCalendar( 'getView')) return $('#calendart').fullCalendar( 'getView').start;return null; },
        end: function(d){ if ($('#calendart').fullCalendar( 'getView')) return $('#calendart').fullCalendar( 'getView').end;return null; }
   
        },
        
    },
    "columns": [
        // { "data": "idcours" },
         { "data": "title" },
         { "data": "start" },
         { "data": "end" },
        { data: 'idcours', render: function (data, type, row) {
                return '<a href="/bo/administratif/cours/'+data+'"><i class="fas fa-info-circle text-warning"></i>&nbsp;détails</a>';
        } }
          
     ],
      "paging":   false,
       "ordering": true,
       "info":     false,
       "searching": false
    } );
    
    
    
//CALENDAR 
$('#calendart').fullCalendar({
    events: 
    {
        url: "/bo/administratifedt/ca",
        type: 'POST',
        data: {
          modele: $("#admmod").val(),
          oid: $("#admoid").val(),
        },       
        color: 'blue',   // a non-ajax option
        textColor: 'black' // a non-ajax option
    },
    editable:true,
    eventDrop:function(ancienevent, delta, revertFunc)  { 

        dropresize(ancienevent);
        oTable.ajax.reload();
    },
    eventResize:function(ancienevent, delta, revertFunc)  { 

        dropresize(ancienevent);
        oTable.ajax.reload();
    },
    
    eventClick : function(event) 
    {
        console.log("modif event event :");
        console.log(event);
        if (event.start.isBefore() || event.end.isBefore())
             dispImp();
        else
            dispModal(event.idcours);
    },
     dayClick : function(date, jsEvent, view) 
    {
        console.log("ajout event date :");
        console.log(date);
        //select de l'heure
        var heureminuteclic=date.format('HH:mm');  
        if (date.isBefore())
            dispImp();
        else
            dispModal(0);
    },
    header: {
        left: 'prev,next,month,agendaWeek,agendaDay',
        /*center: 'title',*/
        right:'title',
        //left: 'month,agendaWeek,agendaDay',
      },
    defaultView: 'month',
    allDaySlot : false,
    displayEventEnd:true,
    minTime : "07:00:00",
    maxTime : "21:00:00",
    height:'auto',
    locale: 'fr',
    //clic sur la crois suppression
    eventRender: function(event, element) {
        element.append( "<a href='#' class='btn closeon'><i class='fas fa-times-circle text-danger'></i></a>" );
        element.find(".closeon").click(function(e) {          
            e.preventDefault();
           // console.log(event.idcours);
           var idcours=event.idcours;
            $.post('/bo/administratifedtsuppresa/'+idcours,function(data){   
                $('#calendart').fullCalendar('refetchEvents');
                oTable.ajax.reload();
                // $('#calendar').fullCalendar('removeEvents',event._id);
            });
            return false;
            
         
        });
    },
   loading: function (bool) { 
                    if (bool) 
                    {
                    $("#panelcalendar").css({"visibility": "hidden"});
                    $('#loading').show();
                    }
                    
                else if (!bool)
                      {
                      //loading
                      $('#loading').hide();
                      $("#panelcalendar").css({"visibility": "visible"});
                      //heading calendar
                      $("#panelheadingcalendar").replaceWith($(".fc-toolbar"));                      
                      $(".fc-button").attr('class',"btn btn-link");
                      $(".fc-left .fc-button-group button").each(function(e){
                         var arialabel=$(this).attr("aria-label");
                         if (arialabel!="next" && arialabel!="prev")
                         {
                            $(this).html($(this).html().replace('<i class="fas fa-arrow-circle-down"></i> ',""));
                            $(this).html('<i class="fas fa-arrow-circle-down"></i> '+ $(this).html());   
                        }       
                      });  
                      //ad liste button  
                      $("#listcal").remove();
                      if($("#calendart").is(":visible"))                    
                        $(".fc-left .fc-button-group").append("<a href='#' id='listcal' class='btn btn-link' mode='liste'><i class='fas fa-arrow-circle-down'></i> Liste</a>");  
                      else
                        $(".fc-left .fc-button-group").append("<a href='#' id='listcal' class='btn btn-link' mode='cal'><i class='fas fa-arrow-circle-down'></i> Calendrier</a>");                     
                      //hide disp calendar
                      $("#listcal").on('click', function(e)
                         {
                            e.preventDefault();
                            var mode=$(this).attr("mode");
                            if (mode == "liste") {$(this).attr("mode","cal");$(this).html("<i class='fas fa-arrow-circle-down'></i> Calendrier"); $("#calendartablediv").show();$("#calendart").hide();}
                            else /*if (mode == "cal")*/  {$(this).attr("mode","liste");$(this).html("<i class='fas fa-arrow-circle-down'></i> Liste"); $("#calendartablediv").hide();$("#calendart").show();}
                         });
                         oTable.ajax.reload();
                      //reload table avec Dates
                     /* $(".fc-left button[aria-label='next']").on('click', function(e)
                         {
                            //console.log("click left button");                      
                            oTable.ajax.reload();
                          });
                          
                     */
                      $(".fc-right").find('h2').replaceWith(function() {
                            return '<h2 style="font-size:1rem;padding-top:6px">' + $(this).text() + '</span></h2>';
                            });
                      }
                      }
    
    
    });  
    



//RENDER TAB
 $('a[href="#tabcalendar"]').on('shown.bs.tab', function (e) {
      
        $('#calendart').fullCalendar('render');
         $('#calendart').fullCalendar('refetchEvents');
    });  

//PERIODE DATEPICKER 
/*
$("input[name*='datedebut'],input[name*='datefin'] ").datepicker({
      showAnim: 'clip',
      //dateFormat: 'dd-mm-yy',
      numberOfMonths: 3,
      showButtonPanel: false
    });*/
 
$("input[name*='datedebut'],input[name*='datefin'] ").datetimepicker({
        format: "dd/mm/yyyy hh:ii", autoclose:true,language:'fr',minuteStep:15
    });

/* SUBMIT FORM  ON CLICK SUPPRIMER*/
$(".supp").on('click',function(e){
//alert("supp");
    var checkboxtoclick="#"+$(this).attr("checkboxtosupp");
   // console.log(checkboxtoclick);
    $(checkboxtoclick).prop('checked', true);
    
    var buttonenregistrer="#"+$(this).attr("buttontoclick");
    $(buttonenregistrer).click();   
});

$(".supplistfs").on('click',function(e){
//alert("supplistfs");
    var checkboxtoclick="#"+$(this).attr("checkboxtosupp");
    // console.log(checkboxtoclick);
    $(checkboxtoclick).prop('checked', true);
    
    var buttonenregistrer=$(this).attr("buttontoclick");
    var prefix=$(this).attr("prefix");
    //$("#groupesdt_form").append('<input type="hidden" name="prefix" value="'+prefix+'" />');
    $('a[nom='+buttonenregistrer+'][prefix='+prefix+']').click();
    //$(buttonenregistrer).click();   
});

/* SUBMIT FORM  ON CLICK SUPPRIMER couleur*/
$(".supp").hover(function(e){
   // alert("ok");
   $(".supp").parent().parent().removeClass("bg-info");
 $(this).parent().parent().addClass("bg-light");
 }, function() {
    $(this).parent().parent().removeClass('bg-light');
});

/*HIDE DELETE BOX INLINEFORMSET */
$("input[type='checkbox'][name*='DELETE']").prop('checked', false);
$("input[type='checkbox'][name*='DELETE']").hide();


/* CONVERTIT SELECT EN SELECT2*/
 $('select').select2({width: '100%', theme: "classic"});
 /*SELECT2 INVALID*/
 $(".is-invalid").parent().find(".select2-container").addClass("is-invalid");
 
 /* SUBMIT FILTER */
$(".filter").on('change',function(e){
    $("#formdelgroupe").submit();
});
 
 //changer le nom en tableau des multi voir eleve
 /*$('select').each(function(e){
    var name=$(this).attr("name");
    var ismulti=$(this).attr("multiple");
    if (ismulti=='multiple')
    {
        var newname=name+"[]";
        $(this).attr("name",newname);
    }
    //console.log(name+" " +ismulti);
     
 });*/
 

// ENREGISTREMENT DERNIER TAB SELECTINONE
 $('#tabmodif a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            // save the latest tab; use cookies if you like 'em better:
            localStorage.setItem('tabmodiflastTab', $(this).attr('href'));
        });

        // go to the latest tab, if it exists:
        var lastTab = localStorage.getItem('tabmodiflastTab');
       // console.log(lastTab);
        if (lastTab) {
            //alert(lastTab);
            if ($('#tabmodif [href="' + lastTab + '"]').length)
                $('#tabmodif [href="' + lastTab + '"]').tab('show');
            else
                $('#tabmodif [href="#tab1"]').tab('show');
        }
        else
            {
            //alert('ok');
             $('#tabmodif [href="#tab1"]').tab('show');
            }

//datatble
$(".dt").DataTable( {
        "paging":   false,
        "ordering": true,
        "info":     false,
        "oLanguage": {
      "sSearch": ""
    }
    });
 
 
 /*search*/
$("input[type=search]").each(function(e){

$(this).attr("placeholder","Rechercher");
$(this).attr("class","form-control");
});
//$('.dataTables_filter input').attr("placeholder", "Rechercher");   


/*
var i =0;
$("#groupesdt th").each(function(e){

    console.log($(this).hasClass("filterchamp"));

    if  ($(this).hasClass("filterchamp"))
    {
     console.log("ok champ à filtrer index "+i);    
    }
    i++;    
});*/
    
    /*
    valcode=$("#selcode").val();
        valentr=$("#selentr").val();
        //alert(valcode);
        //alert(valentr);
        if(valcode=="-1")
            valcode="";
        if(valentr=="-1")
            valentr="";
            tableresa.columns( 5 ).search( valcode ).draw();        
            tableresa.columns( 7 ).search( valentr ).draw();
            */
    


 $(".dt").each(function(e)
 {
 
    //changement place search
     var id=$(this).attr("id");   
     var namefiltertomove="#"+id+"_filter";
     var newfilterid="#"+id+"_newfilter";   
     var hh=$(namefiltertomove); 
     $(newfilterid).replaceWith(hh);
     
     //hide display add form
     console.log(id);
    var nameadd="#"+id+"_add";
    var nameform="#"+id+"_form"; 
    var namelist="#"+id+"_list"; 
   // var nameretour="#"+id+"_retour"; 
    var checkboxall="#"+id+"_delall:checkbox"; 
    var allcheck="."+id+"_del"; 
    //ajouter
   /*  $(nameadd).on('click',function(e){
         //alert("ok");
         $(nameform).show();
         $(namelist).hide();
     });*/
     //retour
  /*    $(nameretour).on('click',function(e){
         $(nameform).hide();
         $(namelist).show();
     });*/
     
     $(checkboxall).click(function(e) 
     {
     var c = this.checked;
     $(allcheck).prop('checked',c);
     });
    
 });
 //fin each
 //check all checkobx
 $(".dt :checkbox").change(function() {
$(this).closest("tr").find("td").toggleClass("bg-warning", this.checked);
});
 
 //click row select cheeckbox
$('.dt tr:not(.h').click(function(event) {
    if (event.target.type !== 'checkbox') {
      $(':checkbox', this).trigger('click');
    }
});
    

 
});

    
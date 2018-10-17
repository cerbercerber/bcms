

function dispModal(idcours) { 
    //if (event.popup) {
        
      //  if(event.isinmoodle)
      
       $('#modalResa').load('/bo/administratifedtresa/'+idcours);    
       $('#modalResa').modal('show');
        return false;
    
}


function dropresize(ancienevent)
{
    //date periode
    /*var pdeb= moment($("input[name='datedebut']").val(),"DD/MM/YY");
    var pfin= moment($("input[name='datefin']").val(),"DD/MM/YY");  
    
    console.log(pdeb);
    console.log(pfin);
    //if(date<now || modifpossible=="non" || date>pfin || date<pdeb)
     var now = moment();
        if(ancienevent.start<now || ancienevent.start<pdeb || ancienevent.start>pfin )
                {
            $("#modalerrordep").modal('show');
            $('#calendar').fullCalendar('refetchEvents');
                }
        else*/
            {
     var datedebut=ancienevent.start.format('YYYY-MM-DD HH:mm');
    var datefin=ancienevent.end.format('YYYY-MM-DD HH:mm');

    
    //console.log(ancienevent);
    //var dateres=
    $.post('/bo/administratifedtresa/'+ancienevent.idcours,
     {dndresize:"oui",
     datedebut:datedebut,
     datefin:datefin},function(data){
        
      
        //var tdata = jQuery.parseJSON(data);
        console.log(data);
        if(data.error!="success")
        {
            //console.log("ok");
            $("#pmessage").html(data.error);
            //$('#myModal').modal('hide');
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

//asterisk requiered
/*
$('input[required]').each(function(index){
var id =$(this).attr("id");
$('label[for='+  id  +']').html($('label[for='+  id  +']').html()+ '<span class="text-danger"> * </span>');
});
*/

//autcomplete
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


//CALENDAR 
$('#calendart').fullCalendar({
    events: 
    {
        url: "/bo/administratifedt",
        type: 'POST',
        data: {
          modele: $("#admmod").val(),
          oid: $("#admoid").val()
        },       
        color: 'blue',   // a non-ajax option
        textColor: 'black' // a non-ajax option
    },
    editable:true,
    eventDrop:function(ancienevent, delta, revertFunc)  { 

        dropresize(ancienevent);
    },
    eventResize:function(ancienevent, delta, revertFunc)  { 

        dropresize(ancienevent);
    },
    
    eventClick : function(event) 
    {
        console.log("modif event event :");
        console.log(event);
        dispModal(event.idcours);
    },
     dayClick : function(date, jsEvent, view) 
    {
        console.log("ajout event date :");
        console.log(date);
        //select de l'heure
        var heureminuteclic=date.format('HH:mm');  
        dispModal(0);
    },
    header: {
        left: 'prev,next today',
        center: 'title',
        right: 'agendaWeek,agendaDay'
      },
    defaultView: 'agendaWeek',
    allDaySlot : false,
    displayEventEnd:true,
    minTime : "07:00:00",
    maxTime : "21:00:00",
    height:'auto',
    locale: 'fr',
   loading: function (bool) { 
                    if (bool) 
                    {
                    $("#panelcalendar").css({"visibility": "hidden"});
                    $('#loading').show();
                    }
                    
                else if (!bool)
                      {
                      $('#loading').hide();
                      $("#panelcalendar").css({"visibility": "visible"});
                      //heading calendar
                        $("#panelheadingcalendar").replaceWith($(".fc-toolbar"));                      
                        $(".fc-button").attr('class',"btn btn-link");

            
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
    var checkboxtoclick="#"+$(this).attr("checkboxtosupp");
    $(checkboxtoclick).click();
    
    var buttonenregistrer="#"+$(this).attr("buttontoclick");
    $(buttonenregistrer).click();   
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
$("input[type='checkbox'][name*='DELETE']").hide();


/* CONVERTIT SELECT EN SELECT2*/
 $('select').select2({width: '100%', theme: "classic"});
 
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
        "info":     false
    });
    


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

    
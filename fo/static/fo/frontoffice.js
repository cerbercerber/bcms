$("document").ready(function(e)
{
$('#calendarel').fullCalendar({
    events: 
    {
        url: "eleveedt",
        type: 'POST',
        data: {
          modele: $("#admmod").val(),
          oid: $("#admoid").val()
        },       
        color: 'blue',   // a non-ajax option
        textColor: 'black' // a non-ajax option
    },
    editable:false,
     header: {
        left: 'prev,next today',
        center: 'title',
        right: 'agendaWeek,agendaDay,month'
      },
    defaultView: 'month',
    allDaySlot : false,
    displayEventEnd:true,
    minTime : "07:00:00",
    maxTime : "21:00:00",
    height:'auto',
    locale: 'fr',
    loading: function (bool) {               
                    if (!bool)
                      {                                     
                        $(".fc-button").attr('class',"btn btn-link");           
                      }
                      }
});
});
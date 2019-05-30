var lat;
var long;

//GET THE MAP
function initMap(lat, long, loc) {
    var city = {
        lat: lat,
        lng: long
    };
    var map = new google.maps.Map(
        document.getElementById('map'), {
            zoom: 11,
            center: city,
        });
    var contentString = 
    '<div id="content">'+ '<div id="siteNotice">'+ '</div>'+ '<h1 id="firstHeading" class="firstHeading">'+ loc +'</h1>' + '</div>'

    var infowindow = new google.maps.InfoWindow({
        content: contentString
        });
    var marker = new google.maps.Marker({
        position: city,
        map: map
    });
    marker.addListener('click', function() {
        infowindow.open(map, marker);
      });
}

//DISPLAY THE MAP
function display_map(){
    $("#map").show();
}

//AJAX
function call_ajax(){
    $.ajax({
        url: '/search',
        data: $('form').serialize(),
        type: 'POST',
        success: function (response) {
        $(".mb-0").html(response);
        },
        error: function (error) {
        console.log(error);
        },
    });
}
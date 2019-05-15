//$(function() { $(':submit').on('click', function() { var usr_query = document.getElementById('search').value; if (usr_query !== "") { document.write("Vous avez saisi :" + usr_query); loading(); ajaxPost(usr_query, data_treat); } }); })
var lat;
var long;

function initMap(lat, long, loc) {
    var city = {
        lat: lat,
        lng: long
    };
    var map = new google.maps.Map(
        document.getElementById('map'), {
            zoom: 10,
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
function display_map(){
    $("#map").show();
}
$(function() { $(':submit').on('click', function() { var usr_query = document.getElementById('search').value; if (usr_query !== "") { document.write("Vous avez saisi :" + usr_query); loading(); ajaxPost(usr_query, data_treat); } }); });
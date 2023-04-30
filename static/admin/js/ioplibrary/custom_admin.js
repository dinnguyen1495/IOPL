// function get_preview() {
//   let file = $('#id_cover').prop('files');
//   let tmp_path = URL.createObjectURL(files[0]);

//   $.ajax({
//     success: function () {
//       update_preview_cover(tmp_path);
//     }
//   });
// }

// function update_preview_cover(file) {
//   $('#cover-img').html(
//     "<img src=\"" + file + "\" width=\"150\">"
//   );
// }

$("#id_cover").change(function(event) {
	let tmppath = URL.createObjectURL(event.target.files[0]);
	$("#cover-img").find("img").attr('src', tmppath);
});
$("#id_cover").change(function(event) {
	let tmppath = URL.createObjectURL(event.target.files[0]);
	$("#cover-img").find("img").attr('src', tmppath);
});
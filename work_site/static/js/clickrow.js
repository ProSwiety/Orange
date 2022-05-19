function rowClicked(){
   var inputs = this.getElementsByTagName("input");
   var checkboxes = [].filter.call(inputs,function(input){
      return input.type == "checkbox" && input.name == "delete";
   });
   this.classList.toggle("active");
   if(checkboxes[0]) checkboxes[0].checked = this.classList.contains("active")

}
window.addEventListener("load",function(){
   var table = document.getElementById("sortable");
   var rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
   for(var i=0; i<rows.length; i++){
      rows[i].addEventListener("click",rowClicked);
   }
});
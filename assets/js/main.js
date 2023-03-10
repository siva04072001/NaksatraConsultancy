// add hovered class to selected list item
let list = document.querySelectorAll(".desk-navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".desk-navigation");
let main = document.querySelector(".main");
let hidetitle=document.querySelector(".logo-title");


toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
  hidetitle.classList.toggle("active");
};




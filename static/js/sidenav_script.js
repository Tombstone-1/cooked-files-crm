const body = document.querySelector('body'),
      sidebar = body.querySelector('nav'),
      toggle = body.querySelector(".toggle"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");

/* === sidenav close toggler === */
toggle.addEventListener("click" , () =>{
    sidebar.classList.toggle("close");
})

/* === hard coded theme/ on page load === */
body.classList.toggle("light");
modeText.innerHTML = "Go Dark";

/* === theme toggler === */
modeSwitch.addEventListener("click" , () =>{
    
    if(body.classList.contains("light")){
        body.classList.remove("light");
        body.classList.add("dark")
        modeText.innerText = "Go Light";
        localStorage.setItem("theme", "dark");
    }else{
        body.classList.remove("dark");
        body.classList.add("light")
        modeText.innerText = "Go Dark";
        localStorage.setItem("theme", "light")
        
    }
});

// function to make theme permanent through out pages, even on reload
window.onload = checkTheme();

function checkTheme() {
    const localStorageTheme = localStorage.getItem("theme");

    if (localStorageTheme !== null && localStorageTheme == "dark") {
        // set body theme to localstorage
        body.className = localStorageTheme;
        modeText.innerHTML = "Go Light";

    }
}
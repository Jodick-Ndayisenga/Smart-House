
function set_on(pin)
{
    
    var commande_XHR = new XMLHttpRequest();
    var action = "/?led" + pin +"=on";
    commande_XHR.open("GET", action, true);
    commande_XHR.send();
               }
function set_off(pin)
{
    var commande_XHR = new XMLHttpRequest();
    var action = "/?led" + pin +"=off";
    commande_XHR.open("GET", action, true);
    commande_XHR.send();
               }           
               
/*
function fct_Avancer() {
    var commande_XHR = new XMLHttpRequest();
    commande_XHR.open("GET", "/?btAvancer=1", true);
    commande_XHR.send();
               }
function fct_Stop() {
    var commande_XHR = new XMLHttpRequest();
    commande_XHR.open("GET", "/?btStop=1", true);
    commande_XHR.send();
               }      
function fct_Reculer() {
    var commande_XHR = new XMLHttpRequest();
    commande_XHR.open("GET", "/?btReculer=1", true);
    commande_XHR.send();
               }      
function fct_Droite() {
    var commande_XHR = new XMLHttpRequest();
    commande_XHR.open("GET", "/?btDroite=1", true);
    commande_XHR.send();
               }      
function fct_Gauche() {
    var commande_XHR = new XMLHttpRequest();
    commande_XHR.open("GET", "/?btGauche=1", true);
    commande_XHR.send();
               }     
               
function fct_vitesseT() {
    document.getElementById("id_affichage_vitesseT").innerHTML = document.getElementById("id_vitesseT").value;
     
    var commande_XHR = new XMLHttpRequest();
    commande_XHR.open("GET", "/?vitesseT="+document.getElementById("id_vitesseT").value, true);
    commande_XHR.send();
                }   

function fct_vitesseR() {
    document.getElementById("id_affichage_vitesseR").innerHTML = document.getElementById("id_vitesseR").value;
                 
    var commande_XHR = new XMLHttpRequest();
    commande_XHR.open("GET", "/?vitesseR="+document.getElementById("id_vitesseR").value, true);
    commande_XHR.send();
                }     


function fct_tourelle() {
    var commande_XHR = new XMLHttpRequest();
    commande_XHR.open("GET", "/?tourelle="+document.getElementById("id_tourelle").value, true);
    commande_XHR.send();
                }   

*/
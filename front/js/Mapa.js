//Creamos el mapa
const map = L.map('map', { zoomControl:false }).setView([36.72,3.05],6);

L.control.zoom({ position:'topright' }).addTo(map);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    attribution:'© OpenStreetMap'
}).addTo(map);



//Aqui para sacar la ubicacion del usuario que la esta usando
if(navigator.geolocation){

    navigator.geolocation.getCurrentPosition(function(pos){

        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        console.log("Mi ubicación:",lat,lng);

        map.setView([lat,lng],14);

        const myIcon = L.divIcon({
            className:"",
            html:`
                <div style="
                    width:18px;
                    height:18px;
                    border-radius:50%;
                    background:#0EA5A5;
                    border:3px solid white;
                    box-shadow:0 0 0 5px rgba(14,165,165,.25);
                "></div>
            `,
            iconSize:[18,18],
            iconAnchor:[9,9]
        });

        L.marker([lat,lng],{icon:myIcon})
        .addTo(map)
        .bindPopup("<b>Tu ubicación</b>")
        .openPopup();

    });

}


/* ─────────────────────────────
   CREAR ICONO TÉCNICO
───────────────────────────── */

function createTechIcon(tech){

    const name = tech.name || "Técnico";
    const initial = name.charAt(0).toUpperCase();

    const photo = tech.image_url;

    let innerHTML="";

    if(photo && photo.trim() !== ""){
        innerHTML = `<img src="${photo}" style="width:100%;height:100%;object-fit:cover;">`
    }else{
        innerHTML = `
            <span style="
                font-weight:800;
                color:#0EA5A5;
                font-size:16px;
            ">${initial}</span>
        `
    }

    const html = `
        <div style="width:52px;height:62px;text-align:center">

            <div style="
                width:48px;
                height:48px;
                border-radius:50%;
                overflow:hidden;
                border:3px solid #0EA5A5;
                background:#F0FAFA;
                display:flex;
                align-items:center;
                justify-content:center;
                box-shadow:0 4px 10px rgba(0,0,0,.15);
            ">
                ${innerHTML}
            </div>

            <div style="
                width:0;
                height:0;
                border-left:7px solid transparent;
                border-right:7px solid transparent;
                border-top:10px solid white;
                margin:auto;
            "></div>

        </div>
    `;

    return L.divIcon({
        className:"",
        html:html,
        iconSize:[52,62],
        iconAnchor:[26,62],
        popupAnchor:[0,-60]
    });

}
//Creamos dinamicamente los circulos de los usuarios
function createPopup(tech){

    const name = tech.name || "Técnico";
    const category = tech.category_name || "";
    const zone = `${tech.city || ""} ${tech.wilaya || ""}`;

    return `
        <div style="padding:10px">

            <b>${name}</b><br>

            <span style="color:#888;font-size:12px">
                ${category}
            </span>

            <br><br>

            <span style="font-size:12px">
                ${zone}
            </span>

            <br><br>

            <button 
                style="
                    width:100%;
                    height:32px;
                    border:none;
                    background:#0C8F8F;
                    color:white;
                    border-radius:8px;
                    cursor:pointer;
                "
                onclick="location.href='technician_info.html?id=${tech.id}'"
            >
                Ver perfil
            </button>

        </div>
    `
}

//Hacer una promesa para cargar los tecnicos
async function loadTechnicians(){

    try{

        const res = await fetch("http://127.0.0.1:5000/api/v1/technicians/");

        const data = await res.json();

        console.log("Técnicos:",data);

        data.forEach(tech => {

            if(tech.latitude == null || tech.longitude == null){
                return;
            }

            const lat = parseFloat(tech.latitude);
            const lng = parseFloat(tech.longitude);

            const icon = createTechIcon(tech);

            const marker = L.marker([lat,lng],{icon})
            .addTo(map);

            marker.bindPopup(createPopup(tech));

        });

    }catch(err){

        console.error("Error cargando técnicos:",err);

    }

}

loadTechnicians();
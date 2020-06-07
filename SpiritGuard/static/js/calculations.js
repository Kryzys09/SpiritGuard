let WATER_IN_BLOOD = 0.806;
let METABOLISM = {
    'M': 0.015,
    'F': 0.017
};
let BODY_WATER = {
    'M': 0.58,
    'F': 0.49
};
let MIL_TO_GRAM = 0.789;

class Alcohol {
    constructor(name, volume, percentage){
        this.name = name;
        this.volume = volume;
        this.percentage = percentage;
    }
}

function addAlcohol(){
    let name = document.getElementById("new-alc-name").value;
    let volume = parseFloat(document.getElementById("new-alc-volume").value);
    let percentage = parseFloat(document.getElementById("new-alc-percentage").value);
    if(!Number.isNaN(volume) && !Number.isNaN(percentage) && percentage <= 1 && percentage > 0 && volume > 0){
        let tr = document.createElement("tr");
        let tdName = document.createElement("td");
        if(name != null)
            tdName.innerText = name;
        tdName.classList.add("alc-name");
        let tdVolume = document.createElement("td");
        tdVolume.innerText = volume;
        tdVolume.classList.add("alc-volume");
        let tdPercentage = document.createElement("td");
        tdPercentage.innerText = percentage;
        tdPercentage.classList.add("alc-percentage");
        let tdButton = document.createElement("td");
        let aButton = document.createElement("a");
        aButton.classList.add("btn-floating", "waves-effect", "waves-light", "red");
        let iButton = document.createElement("i");
        iButton.classList.add("fa", "fa-times");
        aButton.append(iButton);
        tdButton.append(aButton);
        tr.append(tdName, tdVolume, tdPercentage, tdButton);
        document.getElementById('new-alc-tbody').append(tr);
        aButton.onclick = dropAlcohol;
        console.log('new row appended')
    }else {
        alert('incorrect volume or pecentage')
    }
}

function dropAlcohol(event){
    event.target.parentElement.parentElement.parentElement.remove()
}

function getBAC(){
    let gender = document.getElementById("gender-select").value;
    let weight = parseFloat(document.getElementById("weight-input").value);
    let date = document.getElementById("date-input").value;
    let time = document.getElementById("time-input").value;

    if(Number.isNaN(weight)) {
        alert("Incorrect weight provided")
        return
    }

    let nameNodes = document.getElementsByClassName("alc-name");
    let volumeNodes = document.getElementsByClassName("alc-volume");
    let percentageNodes = document.getElementsByClassName("alc-percentage");

    let alcohols = [];

    for(let i=0; i<nameNodes.length; i++){
        alcohols.push(new Alcohol(nameNodes[i].innerText, parseInt(volumeNodes[i].innerText), parseFloat(percentageNodes[i].innerText)))
    }

    let now = new Date();
    let ds = date.split("-");
    let ts = time.split(":");
    let start = new Date(ds[2], parseInt(ds[1])-1, ds[0], ts[0], ts[1]);
    if(now >= start) {
        let hours = dateDiffInHours(start, now)
        console.log(hours)
        console.log("alcohols: ", alcohols);
        let bac = calculateBAC(gender, alcohols, weight, hours)
        console.log("BAC: ", bac)
        let soberingTime = calculateSoberingTime(gender, bac)
        document.getElementById('bac-score').innerText = bac.toFixed(3)
        let stString = soberingTime.toString().split(" GMT")[0]
        document.getElementById('sober-when').innerText = stString
    }else{
        alert("incorrect start date provided")
    }
}

function getMaxBAC(){
    let gender = document.getElementById("gender-select-to-drink").value;
    let weight = parseFloat(document.getElementById("weight-input-to-drink").value);
    let startDate = document.getElementById("date-input-start").value;
    let startTime = document.getElementById("time-input-start").value;
    let endDate = document.getElementById("date-input-end").value;
    let endTime = document.getElementById("time-input-end").value;
    let startBAC = parseFloat(document.getElementById("start-bac").value);
    let endBAC = parseFloat(document.getElementById("end-bac").value);

    if(Number.isNaN(weight) || Number.isNaN(startBAC) || Number.isNaN(endBAC)) {
        alert("Incorrect numbers provided")
        return
    }

    let startDs = startDate.split("-");
    let startTs = startTime.split(":");
    let start = new Date(startDs[2], parseInt(startDs[1])-1, startDs[0], startTs[0], startTs[1]);
    let endDs = endDate.split("-");
    let endTs = endTime.split(":");
    let end = new Date(endDs[2], parseInt(endDs[1])-1, endDs[0], endTs[0], endTs[1]);

    if(Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())){
        alert('Incorrect Dates!')
        return
    }

    let mai = calculateMaxAlcoholIntake(gender, end, start, startBAC, endBAC);

    document.getElementById('max-alcohol-intake').innerText = mai.toFixed(3);

    let drinks = calculateWhichAlcohols(gender, weight, mai, classicAlcohols);

    document.getElementById('beer-to-drink').innerText = drinks['beer'];
    document.getElementById('wine-to-drink').innerText = drinks['wine'];
    document.getElementById('vodka-to-drink').innerText = drinks['vodka'];

    console.log("MAI: ", mai)
    console.log("DRINKS: ", drinks)
}

function getBMI(){
    let weight = parseFloat(document.getElementById("weight-input-to-bmi").value);
    let height = parseFloat(document.getElementById("height-input-to-bmi").value)

    if(Number.isNaN(weight) || Number.isNaN(height)) {
        alert("Incorrect width or height")
        return
    }

    let bmi = calculateBMI(weight, height)

    document.getElementById('bmi').innerText = bmi.toFixed(2)

    let interpret = document.getElementById('bmi-interpret')
    if(bmi < 19.5){
        interpret.innerText = "You're underweight"
    }else if(bmi < 25){
        interpret.innerText = "Your weight is standard"
    }else{
        interpret.innerText = "You're overweight"
    }
}

function dateDiffInHours(a, b) {
    const utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate(), a.getHours(), a.getMinutes());
    const utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate(), b.getHours(), b.getMinutes());

    return Math.floor((utc2 - utc1) / (1000*60*60));
}
/**
 * Metoda do obliczania stanu upojenia alkoholowego
 * @var gender - płeć osoby (0 - mężczyzna, 1 - kobieta)
 * @var alcohols - tablica zawierająca wypite alkohole (
 *      alc.percentage - zawartość samego alkoholu (5% = 0.05)
 *      alc.volume - ilość spożytego napoju (ml)
 * @var weight - waga osoby (kg)
 * @var hours - czas który upłynął od rozpoczęcia spożycia (h)
 *
 * @return (float) - promile alkoholu we krwi
 */
function calculateBAC(gender, alcohols, weight, hours){
    let overall = 0.0;
    for(let i=0; i<alcohols.length; i++){
        overall += alcohols[i].percentage * alcohols[i].volume * MIL_TO_GRAM
    }
    let bac = ((WATER_IN_BLOOD * overall * 0.12)/(BODY_WATER[gender] * weight) - (METABOLISM[gender] * hours))*10;
    return bac >= 0.0 ? bac : 0.0
}

/**
 * Metoda do obliczania procesu trzeźwienia
 *
 * @var gender - płeć osoby (0 - mężczyzna, 1 - kobieta)
 * @var bac - ilość alkoholu we krwi (promile)
 * @var date_time @optional - dokładna data dla której znamy @bac (obiekt datetime)
 *
 * @return Date - data wytrzeźwienia
 */

function calculateSoberingTime(gender, bac, dateTime=new Date()){
    let end = dateTime;
    while(bac > 0.0){
        end.setMinutes(end.getMinutes() + 15);
        bac -= METABOLISM[gender] * 2.5
    }
    return end
}

/**
 * Metoda do obliczania jakie może być maksymalne stężenie alkoholi we krwi
 * aby wytrzeźwieć (albo raczej osiągnąć podany poziom)
 *
 * @var gender - płeć osoby (0 - mężczyzna, 1 - kobieta)
 * @var date_finish - data do której chcemy wytrzeźwieć (obiekt datetime)
 * @var date_now @optional - data od której zaczynamy trzeźwieć (obiekt datetime, domyślnie teraz)
 * @var start_bac @optional - początkowe stężenie alkoholu we krwi (promile, domyślnie 0)
 * @var end_bac @optional - dopuszczalne końcowe stężenie alkoholu we krwi (promile, domyślnie 0)
 *
 * @return (float) - maksymalne stążenie początkowe, żeby organizm zdążył zejść do stężenia końcowego (promile)
 */
function calculateMaxAlcoholIntake(gender, finishDate, nowDate=new Date(), startBAC=0.0, endBAC=0.0){
    startBAC += endBAC;
    let time = dateDiffInHours(nowDate, finishDate);
    console.log(time)
    return startBAC + (METABOLISM[gender] * time * 10)
}

/**
 * Metoda do obliczania ile jakiego alkoholu powinniśmy spożyć, żeby otrzymać
 * dane stężenie alkoholu we krwi
 *
 * @var gender - płeć osoby (0 - mężczyzna, 1 - kobieta)
 * @var weight - waga osoby (kg)
 * @var bac - stężenie alkoholu we krwi (promile)
 * @var alcohols - słownik/lista/tablica z róznymi alkoholami dla których chemy wykonać obliczenia
 *
 * @return (dictionary) - słownik postaci: nazwa_alkoholu -> ilość do wypicia (ml)
 */
function calculateWhichAlcohols(gender, weight, bac, alcohols){
    let amounts = {};
    let grams = (bac * BODY_WATER[gender] * weight)/(1.2 * WATER_IN_BLOOD);
    for(let i=0; i<alcohols.length; i++){
        amounts[alcohols[i].name] = Math.floor(grams/(alcohols[i].percentage * MIL_TO_GRAM));
    }
    return amounts
}

/**
 * Metoda do obliczania współczynnika BMI
 *
 * @param weight - waga osoby (kg)
 * @param height - wzrost osoby (cm)
 * @returns {number} - indywidualny współczynnik bmi
 */
function calculateBMI(weight, height){
    return weight/Math.pow(height/100, 2)
}

let classicAlcohols = [
    new Alcohol('beer', 500, 0.05),
    new Alcohol('wine', 500, 0.116),
    new Alcohol('vodka', 50, 0.4)
]
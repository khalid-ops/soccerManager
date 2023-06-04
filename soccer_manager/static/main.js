
let apiUrl = "http://127.0.0.1:8000"
let userName = document.getElementById("name")
let userEmail = document.getElementById("email")
let userPassword = document.getElementById("password")
let userPhone = document.getElementById("phonenumber")
let signupSubmit = document.getElementById("registerSubmitButton")
let playerTableId = document.getElementById("homeplayerstable")
let marketPlayerTableId = document.getElementById("marketplayerstable")

$(document).ready(function(){

    let accountStatus = localStorage.getItem("accountStatus");
    if (accountStatus == "true") {
      $("#NavTitle").text("SoccerFantasy - Welcome, " + localStorage.getItem("userName"));
      $("#userLogoutButton").show();
      $("#userLoginLink").hide();
      $("#homecontainerafterlogin").show();
      $("#homecontainerbeforelogin").hide();
      $("#marketcontainerafterlogin").show();
      $("#marketcontainerbeforelogin").hide();
      getTeamsPlayers().then((response) =>{
        populatePlayers(response);
      });
      getMarketPlayers().then((response) => {
        populateMarketPlayers(response.playersData);
      })
    }
    else{
      $("#NavTitle").text("SoccerFantasy");
      $("#userLogoutButton").hide();
      $("#userLoginLink").show();
      $("#homecontainerafterlogin").hide();
      $("#homecontainerbeforelogin").show();
      $("#marketcontainerafterlogin").hide();
      $("#marketcontainerbeforelogin").show();
    }

  })

function userRegister(){
        
    let sendData = {
        "name": userName.value,
        "email": userEmail.value,
        "password": userPassword.value,
        "phone" : userPhone.value
    }
    jQuery.ajax({
        type: "POST",   
        url: apiUrl+"/app/user-register",
        data: JSON.stringify(sendData),
        contentType: "application/json",
        success: function(response) {
            console.log(response)
            jQuery("#userRegisterModal").hide();
            jQuery("#userRegisterModal").trigger('reset');
            alert(response.status)
            window.location.href = apiUrl+"/sign-in"
        },
        error: function(response){
            jQuery("#userRegisterModal").hide();
            jQuery("#userRegisterModal").trigger('reset');
            alert(response.status)
            window.location.href = apiUrl+"/sign-in"
        }
    })

}

function userLogin(){

    let loginInfo = {
        "userEmail" : document.getElementById("userEmail").value,
        "userPassword" : document.getElementById("userPassword").value
    }

    jQuery.ajax({
        type: "POST",   
        url: apiUrl+"/app/user-login",
        data: JSON.stringify(loginInfo),
        contentType: "application/json",
        success: function(response) {
            if(response.status === "Login Successful"){
                let user = response.userData
                // alert(response.status)
                afterLogin(user).then(()=>{
                    location.assign(apiUrl+"/home")
                })

            }
            else{
                document.getElementById("userEmail").value = "";
                document.getElementById("userPassword").value =  "";
                alert(response.status)
            }

        },
        error: function(response){
            alert(response.status)
        }
    })
}

function userLogout(){

    let Data = {
        "userId" : localStorage.getItem("accountId")
    }
    jQuery.ajax({
        type: "GET",
        url: apiUrl+"/app/user-logout",
        data: Data,
        success: function(response){
            alert(response.status)
            localStorage.setItem("accountStatus", "false")
            localStorage.removeItem("accountId")
            localStorage.removeItem("userName")
            window.location.href = apiUrl+"/home"
        },
        error: function(){
            alert(response.status)
        }


    })

}


function getTeamsPlayers(){

    if(localStorage.getItem("accountStatus") !== "true"){
        alert("Kindly Login to proceed!")
        return
    }
    if(localStorage.getItem("accountId") === null){
        alert("Kindly Login to proceed!")
        return
    }
    let userData = {
        'userId' : localStorage.getItem("accountId")
    }
    return jQuery.ajax({
        type : "GET",
        url : apiUrl+"/app/get-teams-data",
        data : userData,
        success : function(response){
        },
        error : function(){
            alert(response.status)
        }
    })
}

async function afterLogin(user){
    let task = new Promise (async (resolve, reject) =>{
        localStorage.setItem("accountStatus",  user.accountStatus);
        localStorage.setItem("userName", user.name);
        localStorage.setItem("accountId",  user.id);
        document.getElementById("userEmail").value = "";
        document.getElementById("userPassword").value =  "";
        resolve(true)
    })
    await task;
}

function populatePlayers(teamData){
    $("#initialhometext").text("Your Team")
    let team = teamData.teams_data.teams_details
    let players = teamData.players_data
    let teamList = document.getElementById("hometeamdetails")
    let teamcomponents = `
    <li>
    <p>Team - ${team.team_name} | Country - ${team.team_country} | Value - $${team.team_value} | Budget - $${team.team_budget}</p>
    </li>
    `
    if (teamList !== null){
        teamList.innerHTML = teamcomponents;
    }

    for(let player in players){
        let id = players[player].id
        let playerDetails = players[player].player_details
        if (playerTableId !== null){
        let row = playerTableId.insertRow();
        let player_firstnameCell = row.insertCell();
        let player_lastnameCell = row.insertCell();
        let playerAge = row.insertCell();
        let playerCountry = row.insertCell();
        let playerValue = row.insertCell();
        let todoCell = row.insertCell();
        player_firstnameCell.innerHTML = playerDetails.player_firstname;
        player_lastnameCell.innerHTML = playerDetails.player_lastname;
        playerAge.innerHTML = playerDetails.player_age;
        playerCountry.innerHTML = playerDetails.player_country;
        playerValue.innerHTML = playerDetails.player_value;
        let updatebutton = document.createElement("button")
        updatebutton.id = "updateplayer"+id
        updatebutton.innerHTML = "Update"
        updatebutton.className = "btn btn-info"
        updatebutton.setAttribute("onclick", "perPlayerUpdateModal("+JSON.stringify(playerDetails)+", "+id+")")
        let transferbutton = document.createElement("button")
        transferbutton.id = "transferplayer"+id
        transferbutton.innerHTML = "Transfer"
        transferbutton.className = "btn btn-danger"
        transferbutton.style.marginLeft = "5px"
        transferbutton.setAttribute("onclick", "perPlayerTransfer("+playerDetails.player_value+", "+id+")")
        todoCell.appendChild(updatebutton)
        todoCell.appendChild(transferbutton)
        }
    }

}

function populateTeamsUpdateForm(){

    $("#teamUpdateModal").trigger('reset')
    $("#teamUpdateModal").modal('show');
    getTeamsPlayers().then((response)=>{
        let teamData = response.teams_data.teams_details
        $("#updateteamname").val(teamData.team_name)
        $("#updateteamcountry").val(teamData.team_country)
        
    })
    
       
}

function perPlayerUpdateModal(playerData, id){

    $("#playerUpdateModal").trigger('reset')
    $("#updateplayerfirstname").val(playerData.player_firstname)
    $("#updateplayerlastname").val(playerData.player_lastname)
    $("#updateplayercountry").val(playerData.player_country)
    $("#playerUpdateModal").modal('show');

    let updateModalSubmit = document.getElementById("playersDataUpdatebutton")
    updateModalSubmit.setAttribute("onclick", "updatePlayersData("+id+")")

}

function updateTeamsData(){
    
    if(localStorage.getItem("accountStatus") !== "true"){
        alert("Kindly Login to proceed!")
        return
    }
    if(localStorage.getItem("accountId") === null){
        alert("Kindly Login to proceed!")
        return
    }
    teamsNewData = {
        'teamName' : $("#updateteamname").val(),
        'teamCountry' :  $("#updateteamcountry").val()
    }
    let sendData = {
        'userId' : localStorage.getItem("accountId"),
        'teamData' : teamsNewData

    }

    jQuery.ajax({
        type: "POST",   
        url: apiUrl+"/app/update-teams",
        data: JSON.stringify(sendData),
        contentType: "application/json",
        success: function(response) {
            alert(response.status)
            location.assign(apiUrl+"/home")
        },
        error: function(response){
            alert(response.status)
        }
    })


}

function updatePlayersData(playerid){
    console.log("update players", playerid)
    if(localStorage.getItem("accountStatus")!== "true"){
        alert("Kindly Login to proceed!")
        return
    }
    if(localStorage.getItem("accountId") === null){
        alert("Kindly Login to proceed!")
        return
    }
    let sendData = {
        'userId' : localStorage.getItem("accountId"),
        'playerId' : playerid,
        'playerFirstName' : $("#updateplayerfirstname").val(),
        'playerLastName' : $("#updateplayerlastname").val(),
        'playerCountry' : $("#updateplayercountry").val()
    }
    jQuery.ajax({
        type: "POST",
        url: apiUrl+"/app/update-players",
        data: JSON.stringify(sendData),
        contentType : "application/json",
        success: function(response) {
            alert(response.status)
            location.assign(apiUrl+"/home")
        },
        error: function(response){
            alert(response.status)
        }
    })
}

function perPlayerTransfer(playerValue, id){
    $("#playerTransferModal").trigger('reset')
    $("#playertransfervalue").val(playerValue)
    $("#playerTransferModal").modal('show');

    let updateModalSubmit = document.getElementById("transferSubmitButton")
    updateModalSubmit.setAttribute("onclick", "transferPlayer("+id+")")

}

function transferPlayer(playerId){

    if(localStorage.getItem("accountStatus") !== "true"){
        alert("Kindly Login to proceed!")
        return
    }
    if(localStorage.getItem("accountId") === null){
        alert("Kindly Login to proceed!")
        return
    }
    transferData = {
        'playerId' : playerId,
        'playerNewValue' : $("#playertransfervalue").val()
    }
    let sendData = {
        'userId' : localStorage.getItem("accountId"),
        'transferData' : transferData
    }

    jQuery.ajax({
        type: "POST",   
        url: apiUrl+"/app/transfer-players",
        data: JSON.stringify(sendData),
        contentType: "application/json",
        success: function(response) {
            alert(response.status)
            location.assign(apiUrl+"/home")
        },
        error: function(response){
            alert(response.status)
        }
    })

}

function getMarketPlayers(){

    if(localStorage.getItem("accountStatus") !== "true"){
        alert("Kindly Login to proceed!")
        return
    }
    let userData = {
        'userId' : localStorage.getItem("accountId")
    }
    return jQuery.ajax({
        type : "GET",
        url : apiUrl+"/app/get/market-players",
        data : userData,
        success : function(response){
            console.log(response)
        },
        error : function(){
            alert(response.status)
        }
    })

}

function populateMarketPlayers(players){

    for(let player in players){
        let id = players[player].id
        let playerDetails = players[player].players_details
        if(marketPlayerTableId !== null){
        let row = marketPlayerTableId.insertRow();
        let player_firstnameCell = row.insertCell();
        let player_lastnameCell = row.insertCell();
        let playerAge = row.insertCell();
        let playerCountry = row.insertCell();
        let playerValue = row.insertCell();
        let todoCell = row.insertCell();
        player_firstnameCell.innerHTML = playerDetails.player_firstname;
        player_lastnameCell.innerHTML = playerDetails.player_lastname;
        playerAge.innerHTML = playerDetails.player_age;
        playerCountry.innerHTML = playerDetails.player_country;
        playerValue.innerHTML = playerDetails.player_value;
        let buybutton = document.createElement("button")
        buybutton.id = "buyplayer"+id
        buybutton.innerHTML = "Buy"
        buybutton.className = "btn btn-info"
        buybutton.setAttribute("onclick", "playerBuying("+id+")")

        todoCell.appendChild(buybutton)
        }
    }
}

function playerBuying(playerId){
    if(localStorage.getItem("accountStatus") !== "true"){
        alert("Kindly Login to proceed!")
        return
    }
    if(localStorage.getItem("accountId") === null){
        alert("Kindly Login to proceed!")
        return
    }
    let sendData = {
        'userId' : localStorage.getItem("accountId"),
        'playerId' : playerId
    }

    jQuery.ajax({
        type: "POST",   
        url: apiUrl+"/app/buy/players",
        data: JSON.stringify(sendData),
        contentType: "application/json",
        success: function(response) {
            alert(response.status)
            console.log(response)
            location.assign(apiUrl+"/home")
        },
        error: function(response){
            console.log(response)
            alert(response.status)
        }
    })

}